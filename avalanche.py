#!/usr/bin/env python3

import argparse

from migen import *
from migen.genlib.resetsync import AsyncResetSynchronizer

from litex.build.generic_platform import *

from litex.soc.interconnect import wishbone
from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.cores.uart import UARTWishboneBridge
from litex.soc.cores.clock import period_ns

from litex.boards.platforms import avalanche

from litedram.frontend.axi import *
from litedram.frontend.wishbone import *

from components.wrappers import *

from litex.soc.interconnect.csr import AutoCSR

from litex.soc.cores.spi import SPIMaster
from litex.soc.cores.i2c import I2C
from litex.soc.cores.gpio import GPIOOut


_ddram_specific_ios = [
    ("ddram_shield", 0, Pins("R9")),
    ("ddram_shield", 1, Pins("V15")),
]

class _CRG(Module):
    def __init__(self, platform):
        self.clock_domains.cd_ccc = ClockDomain()
        self.clock_domains.cd_sys = ClockDomain()
        self.cd_sys_pll_lock = Signal()
        self.cd_sys_ddram_ready = Signal()

        # # #

        # Initialization Monitor
        monitor = Monitor()
        monitor.add_sources(platform)
        self.submodules += monitor

        # RC oscillator (160MHz)
        osc = Osc()
        osc.add_sources(platform)
        self.submodules += osc

        # Conditioning Circuitry (160MHz --> 100MHz)
        ccc = CCC()
        ccc.add_sources(platform)
        ccc.add_timing_constraints(platform)
        self.submodules += ccc
        monitor_rst = ~(monitor.DEVICE_INIT_DONE &     # Keep reset asserted
                        monitor.BANK_0_CALIB_STATUS &  # until device is fully
                        monitor.BANK_1_CALIB_STATUS &  # initialized and PLL
                        ccc.PLL_LOCK_0)                # is locked.
        self.comb += [
            ccc.REF_CLK_0.eq(osc.RCOSC_160MHZ_GL),
            self.cd_ccc.clk.eq(ccc.OUT0_FABCLK_0),
        ]
        rst = ~platform.request("rst_n")
        self.specials += AsyncResetSynchronizer(self.cd_ccc, rst | monitor_rst)

        # System Clock (100MHz)
        self.specials += AsyncResetSynchronizer(self.cd_sys, ~self.cd_sys_pll_lock | ~self.cd_sys_ddram_ready)
        platform.add_period_constraint(self.cd_sys.clk, period_ns(100e6))


class ArduinoGPIO(Module, AutoCSR):
    def __init__(self, platform):
        outputs = Signal(3)

        self.submodules.outputs = GPIOOut(outputs)
        self.comb += [
            platform.request("mux_sel", 0).eq(outputs[0]),
            platform.request("mux_sel", 1).eq(outputs[1]),
            platform.request("mux_sel", 2).eq(outputs[2]),
        ]


class BaseSoC(SoCCore):
    csr_map = {
        "spi" : 20,
        "i2c" : 21,
        "gpio" : 22,
    }
    csr_map.update(SoCCore.csr_map)
    def __init__(self, platform, l2_size=8192, **kwargs):
        sys_clk_freq = int(100e6)
        platform.add_extension(_ddram_specific_ios)
        SoCCore.__init__(self, platform, clk_freq=sys_clk_freq,
            cpu_type="vexriscv",
            cpu_variant="jtag",
            integrated_rom_size=0x8000,
            integrated_sram_size=0x8000,
            ident="Avalanche PolarFire LiteX SoC", ident_version=True,
            **kwargs)

        # crg
        self.submodules.crg = _CRG(platform)

        # peripherals
        self.submodules.spi = SPIMaster(platform.request("pmodspi"))
        self.submodules.i2c = I2C(platform.request("i2c"))
        self.submodules.gpio = ArduinoGPIO(platform)

        # jtag

        jtag_if = platform.request("jtag")

        self.comb += self.cpu.jtag_tdi.eq(jtag_if.tdi)
        self.comb += self.cpu.jtag_tms.eq(jtag_if.tms)
        self.comb += self.cpu.jtag_tck.eq(jtag_if.tck)

        self.comb += jtag_if.tdo.eq(self.cpu.jtag_tdo)

        # ddram controller
        ddram_ready = Signal()
        axi_port = LiteDRAMAXIPort(data_width=64, address_width=32, id_width=4)
        ddram_pads = platform.request("ddram")
        self.specials += Instance("ddr3",
            # control / status
            i_PLL_REF_CLK=self.crg.cd_ccc.clk,
            i_SYS_RESET_N=~self.crg.cd_ccc.rst,
            o_SYS_CLK=self.crg.cd_sys.clk,
            o_PLL_LOCK=self.crg.cd_sys_pll_lock,
            o_SHIELD0=platform.request("ddram_shield", 0),
            o_SHIELD1=platform.request("ddram_shield", 1),
            o_CTRLR_READY=self.crg.cd_sys_ddram_ready,

            # ddram pads
            o_A=ddram_pads.a,
            o_BA=ddram_pads.ba,
            o_RAS_N=ddram_pads.ras_n,
            o_CAS_N=ddram_pads.cas_n,
            o_WE_N=ddram_pads.we_n,
            o_CS_N=ddram_pads.cs_n,
            o_DM=ddram_pads.dm,
            io_DQ=ddram_pads.dq,
            io_DQS=ddram_pads.dqs_p,
            io_DQS_N=ddram_pads.dqs_n,
            o_CK0=ddram_pads.clk_p,
            o_CK0_N=ddram_pads.clk_n,
            o_CKE=ddram_pads.cke,
            o_ODT=ddram_pads.odt,
            o_RESET_N=ddram_pads.reset_n,

            # axi aw
            i_axi0_awvalid=axi_port.aw.valid,
            o_axi0_awready=axi_port.aw.ready,
            i_axi0_awaddr=axi_port.aw.addr,
            i_axi0_awburst=axi_port.aw.burst,
            i_axi0_awlen=axi_port.aw.len,
            i_axi0_awsize=axi_port.aw.size,
            i_axi0_awid=axi_port.aw.id,
            i_axi0_awprot=0,
            i_axi0_awcache=0,
            i_axi0_awlock=0,

            # axi b
            o_axi0_bvalid=axi_port.b.valid,
            i_axi0_bready=axi_port.b.ready,
            o_axi0_bid=axi_port.b.id,
            o_axi0_bresp=axi_port.b.resp,

            # axi w
            i_axi0_wvalid=axi_port.w.valid,
            o_axi0_wready=axi_port.w.ready,
            i_axi0_wlast=axi_port.w.last,
            i_axi0_wstrb=axi_port.w.strb,
            i_axi0_wdata=axi_port.w.data,

            # axi ar
            i_axi0_arvalid=axi_port.ar.valid,
            o_axi0_arready=axi_port.ar.ready,
            i_axi0_araddr=axi_port.ar.addr,
            i_axi0_arburst=axi_port.ar.burst,
            i_axi0_arlen=axi_port.ar.len,
            i_axi0_arsize=axi_port.ar.size,
            i_axi0_arid=axi_port.ar.id,
            i_axi0_arprot=0,
            i_axi0_arcache=0,
            i_axi0_arlock=0,

            # axi r
            o_axi0_rvalid=axi_port.r.valid,
            i_axi0_rready=axi_port.r.ready,
            o_axi0_rlast=axi_port.r.last,
            o_axi0_rresp=axi_port.r.resp,
            o_axi0_rdata=axi_port.r.data,
            o_axi0_rid=axi_port.r.id,
        )
        DDR3Controller.add_sources(platform)
        DDR3Controller.add_floorplanning_constraints(platform)
        DDR3Controller.add_timing_constraints(platform)
        self.add_constant("MAIN_RAM_TEST", None)


        # wishbone to axi
        wb_sdram = wishbone.Interface()
        l2_cache = wishbone.Cache(l2_size//4, wb_sdram, wishbone.Interface(axi_port.data_width))
        self.add_constant("L2_SIZE", l2_size)
        wishbone2axi = LiteDRAMWishbone2AXI(l2_cache.slave, axi_port)
        self.submodules += l2_cache, wishbone2axi
        self.add_wb_slave(mem_decoder(self.mem_map["main_ram"]), wb_sdram)
        self.add_memory_region("main_ram", self.mem_map["main_ram"], 0x10000000)

        # led0: led blink
        counter = Signal(32)
        self.sync += counter.eq(counter + 1)
        self.comb += platform.request("user_led", 0).eq(counter[26])

        # led2: ddram_ready
        self.comb += platform.request("user_led", 2).eq(~self.crg.cd_sys_ddram_ready) # led is active low


def main():
    parser = argparse.ArgumentParser(description="LiteX SoC port to Avalanche")
    builder_args(parser)
    soc_core_args(parser)
    args = parser.parse_args()

    platform = avalanche.Platform()
    soc = BaseSoC(platform)
    builder = Builder(soc, output_dir="build")
    builder.build()

if __name__ == "__main__":
    main()
