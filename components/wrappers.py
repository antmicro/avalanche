import os

from migen import *


class JTAG(Module):
    def __init__(self):
        self.tdo = Signal()
        self.tdi = Signal()
        self.tms = Signal()
        self.tck = Signal()
        self.trstb = Signal()

        self.tgt_tdo = Signal()
        self.tgt_tdi = Signal()
        self.tgt_tms = Signal()
        self.tgt_tck = Signal()
        self.tgt_trstb = Signal()

        # # #

        self.specials += Instance("jtag",
                o_TDO = self.tdo,
                i_TCK = self.tck,
                i_TDI = self.tdi,
                i_TMS = self.tms,
                i_TRSTB = self.trstb,

                i_TGT_TDO_0 = self.tgt_tdo,
                o_TGT_TCK_0 = self.tgt_tck,
                o_TGT_TDI_0 = self.tgt_tdi,
                o_TGT_TMS_0 = self.tgt_tms,
                o_TGT_TRSTB_0 = self.tgt_trstb,
        )

    @staticmethod
    def add_sources(platform):
        path = os.path.abspath(os.path.dirname(__file__))
        platform.add_source_dir(os.path.join(path, "jtag"))


class Monitor(Module):
    def __init__(self):
        self.USRAM_INIT_DONE = Signal()
        self.DEVICE_INIT_DONE = Signal()
        self.BANK_0_CALIB_STATUS = Signal()
        self.FABRIC_POR_N = Signal()
        self.SRAM_INIT_FROM_SPI_DONE = Signal()
        self.SRAM_INIT_FROM_SNVM_DONE = Signal()
        self.AUTOCALIB_DONE = Signal()
        self.SRAM_INIT_FROM_UPROM_DONE = Signal()
        self.USRAM_INIT_FROM_SPI_DONE = Signal()
        self.XCVR_INIT_DONE = Signal()
        self.BANK_1_CALIB_STATUS = Signal()
        self.SRAM_INIT_DONE = Signal()
        self.USRAM_INIT_FROM_UPROM_DONE = Signal()
        self.USRAM_INIT_FROM_SNVM_DONE = Signal()
        self.PCIE_INIT_DONE = Signal()

        # # #

        self.specials += Instance("monitor",
            o_USRAM_INIT_DONE=self.USRAM_INIT_DONE,
            o_DEVICE_INIT_DONE=self.DEVICE_INIT_DONE,
            o_BANK_0_CALIB_STATUS=self.BANK_0_CALIB_STATUS,
            o_FABRIC_POR_N=self.FABRIC_POR_N,
            o_SRAM_INIT_FROM_SPI_DONE=self.SRAM_INIT_FROM_SPI_DONE,
            o_SRAM_INIT_FROM_SNVM_DONE=self.SRAM_INIT_FROM_SNVM_DONE,
            o_AUTOCALIB_DONE=self.AUTOCALIB_DONE,
            o_SRAM_INIT_FROM_UPROM_DONE=self.SRAM_INIT_FROM_UPROM_DONE,
            o_USRAM_INIT_FROM_SPI_DONE=self.USRAM_INIT_FROM_SPI_DONE,
            o_XCVR_INIT_DONE=self.XCVR_INIT_DONE,
            o_BANK_1_CALIB_STATUS=self.BANK_1_CALIB_STATUS,
            o_SRAM_INIT_DONE=self.SRAM_INIT_DONE,
            o_USRAM_INIT_FROM_UPROM_DONE=self.USRAM_INIT_FROM_UPROM_DONE,
            o_USRAM_INIT_FROM_SNVM_DONE=self.USRAM_INIT_FROM_SNVM_DONE,
            o_PCIE_INIT_DONE=self.PCIE_INIT_DONE,
        )

    @staticmethod
    def add_sources(platform):
        path = os.path.abspath(os.path.dirname(__file__))
        platform.add_source_dir(os.path.join(path, "monitor"))
        platform.add_source_dir(os.path.join(path, "monitor", "monitor_0"))


class Osc(Module):
    def __init__(self):
        self.RCOSC_160MHZ_GL = Signal()

        # # #

        self.specials += Instance("osc",
            o_RCOSC_160MHZ_GL=self.RCOSC_160MHZ_GL,
        )

    @staticmethod
    def add_sources(platform):
        path = os.path.abspath(os.path.dirname(__file__))
        platform.add_source_dir(os.path.join(path, "osc"))
        platform.add_source_dir(os.path.join(path, "osc", "osc_0"))


class CCC(Module):
    def __init__(self):
        self.REF_CLK_0 = Signal()
        self.PLL_LOCK_0 = Signal()
        self.OUT0_FABCLK_0 = Signal()

        # # #

        self.specials += Instance("ccc",
            i_REF_CLK_0=self.REF_CLK_0,
            o_PLL_LOCK_0=self.PLL_LOCK_0,
            o_OUT0_FABCLK_0=self.OUT0_FABCLK_0,
        )

    @staticmethod
    def add_sources(platform):
        path = os.path.abspath(os.path.dirname(__file__))
        platform.add_source_dir(os.path.join(path, "ccc"))
        platform.add_source_dir(os.path.join(path, "ccc", "ccc_0"))

    @staticmethod
    def add_timing_constraints(platform):
        platform.toolchain.additional_timing_constraints += [
            # ccc
            "create_clock -period 6.25 [ get_pins { ccc/ccc_0/pll_inst_0/REF_CLK_0 } ]",
            "create_generated_clock -multiply_by 5 -divide_by 8 -source [ get_pins { ccc/ccc_0/pll_inst_0/REF_CLK_0 } ] -phase 0 [ get_pins { ccc/ccc_0/pll_inst_0/OUT0 } ]",
        ]


class DDR3Controller(Module):
    def __init__(self):
        self.axi0_awsize = Signal(3)
        self.DQS = Signal(2)
        self.axi0_arsize = Signal(3)
        self.SHIELD0 = Signal()
        self.axi0_arlock = Signal(2)
        self.axi0_awid = Signal(4)
        self.axi0_rresp = Signal(2)
        self.axi0_wvalid = Signal()
        self.axi0_arvalid = Signal()
        self.axi0_awburst = Signal(2)
        self.axi0_bvalid = Signal()
        self.axi0_arready = Signal()
        self.axi0_awlen = Signal(8)
        self.SYS_CLK = Signal()
        self.axi0_awcache = Signal(4)
        self.axi0_araddr = Signal(32)
        self.SYS_RESET_N = Signal()
        self.axi0_awaddr = Signal(32)
        self.CTRLR_READY = Signal()
        self.RESET_N = Signal()
        self.CAS_N = Signal()
        self.CKE = Signal()
        self.CK0 = Signal()
        self.axi0_arburst = Signal(2)
        self.SHIELD1 = Signal()
        self.BA = Signal(3)
        self.axi0_rvalid = Signal()
        self.axi0_wdata = Signal(64)
        self.axi0_awlock = Signal(2)
        self.PLL_REF_CLK = Signal()
        self.axi0_rid = Signal(4)
        self.A = Signal(15)
        self.axi0_arprot = Signal(3)
        self.axi0_bid = Signal(4)
        self.CK0_N = Signal()
        self.PLL_LOCK = Signal()
        self.WE_N = Signal()
        self.CS_N = Signal()
        self.axi0_awready = Signal()
        self.axi0_bready = Signal()
        self.RAS_N = Signal()
        self.axi0_wstrb = Signal(8)
        self.DM = Signal(2)
        self.axi0_awvalid = Signal()
        self.axi0_bresp = Signal(2)
        self.DQ = Signal(16)
        self.DQS_N = Signal(2)
        self.axi0_wlast = Signal()
        self.ODT = Signal()
        self.axi0_arid = Signal(4)
        self.axi0_rdata = Signal(64)
        self.axi0_wready = Signal()
        self.axi0_rready = Signal()
        self.axi0_arlen = Signal(8)
        self.axi0_rlast = Signal()
        self.axi0_arcache = Signal(4)
        self.axi0_awprot = Signal(3)

        # # #

        self.specials += Instance("ddr3",
            i_axi0_awsize=self.axi0_awsize,
            io_DQS=self.DQS,
            i_axi0_arsize=self.axi0_arsize,
            o_SHIELD0=self.SHIELD0,
            i_axi0_arlock=self.axi0_arlock,
            i_axi0_awid=self.axi0_awid,
            o_axi0_rresp=self.axi0_rresp,
            i_axi0_wvalid=self.axi0_wvalid,
            i_axi0_arvalid=self.axi0_arvalid,
            i_axi0_awburst=self.axi0_awburst,
            o_axi0_bvalid=self.axi0_bvalid,
            o_axi0_arready=self.axi0_arready,
            i_axi0_awlen=self.axi0_awlen,
            o_SYS_CLK=self.SYS_CLK,
            i_axi0_awcache=self.axi0_awcache,
            i_axi0_araddr=self.axi0_araddr,
            i_SYS_RESET_N=self.SYS_RESET_N,
            i_axi0_awaddr=self.axi0_awaddr,
            o_CTRLR_READY=self.CTRLR_READY,
            o_RESET_N=self.RESET_N,
            o_CAS_N=self.CAS_N,
            o_CKE=self.CKE,
            o_CK0=self.CK0,
            i_axi0_arburst=self.axi0_arburst,
            o_SHIELD1=self.SHIELD1,
            o_BA=self.BA,
            o_axi0_rvalid=self.axi0_rvalid,
            i_axi0_wdata=self.axi0_wdata,
            i_axi0_awlock=self.axi0_awlock,
            i_PLL_REF_CLK=self.PLL_REF_CLK,
            o_axi0_rid=self.axi0_rid,
            o_A=self.A,
            i_axi0_arprot=self.axi0_arprot,
            o_axi0_bid=self.axi0_bid,
            o_CK0_N=self.CK0_N,
            o_PLL_LOCK=self.PLL_LOCK,
            o_WE_N=self.WE_N,
            o_CS_N=self.CS_N,
            o_axi0_awready=self.axi0_awready,
            i_axi0_bready=self.axi0_bready,
            o_RAS_N=self.RAS_N,
            i_axi0_wstrb=self.axi0_wstrb,
            o_DM=self.DM,
            i_axi0_awvalid=self.axi0_awvalid,
            o_axi0_bresp=self.axi0_bresp,
            io_DQ=self.DQ,
            io_DQS_N=self.DQS_N,
            i_axi0_wlast=self.axi0_wlast,
            o_ODT=self.ODT,
            i_axi0_arid=self.axi0_arid,
            o_axi0_rdata=self.axi0_rdata,
            o_axi0_wready=self.axi0_wready,
            i_axi0_rready=self.axi0_rready,
            i_axi0_arlen=self.axi0_arlen,
            o_axi0_rlast=self.axi0_rlast,
            i_axi0_arcache=self.axi0_arcache,
            i_axi0_awprot=self.axi0_awprot,
        )

    @staticmethod
    def add_sources(platform):
        path = os.path.abspath(os.path.dirname(__file__))

        # ddr3
        platform.add_source_dir(os.path.join(path, "ddr3"))
        platform.add_source_dir(os.path.join(path, "ddr3", "CCC_0"))
        platform.add_source_dir(os.path.join(path, "ddr3", "DDRCTRL_0"))
        platform.add_source_dir(os.path.join(path, "ddr3", "DLL_0"))
        
        # ddr3_ddrphy_blk
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "IOD_A_11_0"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "IOD_A_12"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "IOD_A_13"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "IOD_A_14"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "IOD_BA"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "IOD_BCLK_TRAINING"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "IOD_CAS_N"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "IOD_CKE"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "IOD_CS_N"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "IOD_ODT"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "IOD_RAS_N"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "IOD_REF_CLK_TRAINING"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "IOD_RESET_N"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "IOD_WE_N"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "LANE_0_CTRL"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "LANE_0_IOD_DM"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "LANE_0_IOD_DQ"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "LANE_0_IOD_DQS"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "LANE_0_IOD_DQSW_TRAINING"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "LANE_0_IOD_READ_TRAINING"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "LANE_1_CTRL"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "LANE_1_IOD_DM"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "LANE_1_IOD_DQ"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "LANE_1_IOD_DQS"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "LANE_1_IOD_DQSW_TRAINING"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "LANE_1_IOD_READ_TRAINING"))
        platform.add_source_dir(os.path.join(path, "ddr3_DDRPHY_BLK", "LANECTRL_ADDR_CMD_0"))
        
        # coreddr_tip
        platform.add_source_dir(os.path.join(path, "COREDDR_TIP", "1.6.106"))
        platform.add_source_dir(os.path.join(path, "COREDDR_TIP", "1.6.106", "rtl", "vlog", "core"))
        
        # pf_ddr_cfg_init
        platform.add_source_dir(os.path.join(path, "PF_DDR_CFG_INIT", "1.0.100"))

    @staticmethod
    def add_floorplanning_constraints(platform):
        platform.toolchain.additional_fp_constraints += [
            "set_location -inst_name ddr3/DLL_0/dll_inst_0 -fixed true -x 3 -y 377",
            "set_location -inst_name ddr3/DDRPHY_BLK_0/LANE_1_IOD_READ_TRAINING/I_IOD_0 -fixed true -x 1812 -y 378",
            "set_location -inst_name ddr3/DDRPHY_BLK_0/LANE_0_IOD_READ_TRAINING/I_IOD_0 -fixed true -x 648 -y 378",
            "set_location -inst_name ddr3/CCC_0/pll_inst_0 -fixed true -x 1 -y 377",
            "set_location -inst_name ddr3/DDRPHY_BLK_0/LANE_0_CTRL/I_LANECTRL -fixed true -x 659 -y 378",
            "set_location -inst_name ddr3/DDRPHY_BLK_0/LANE_1_CTRL/I_LANECTRL -fixed true -x 1823 -y 378",
            "set_location -inst_name ddr3/DDRPHY_BLK_0/IOD_BCLK_TRAINING/I_IOD_0 -fixed true -x 60 -y 378"
        ]

    @staticmethod
    def add_timing_constraints(platform):
        platform.toolchain.additional_timing_constraints += [
            # ddr3/ccc
            "create_clock -period 10 [ get_pins { ddr3/CCC_0/pll_inst_0/REF_CLK_0 } ]",
            "create_generated_clock -multiply_by 4 -source [ get_pins { ddr3/CCC_0/pll_inst_0/REF_CLK_0 } ] -phase 0 [ get_pins { ddr3/CCC_0/pll_inst_0/OUT0 } ]",
            "create_generated_clock -divide_by 1 -source [ get_pins { ddr3/CCC_0/pll_inst_0/REF_CLK_0 } ] -phase 0 [ get_pins { ddr3/CCC_0/pll_inst_0/OUT1 } ]",
            "create_generated_clock -multiply_by 4 -source [ get_pins { ddr3/CCC_0/pll_inst_0/REF_CLK_0 } ] -phase 0 [ get_pins { ddr3/CCC_0/pll_inst_0/OUT2 } ]",
            "create_generated_clock -multiply_by 4 -source [ get_pins { ddr3/CCC_0/pll_inst_0/REF_CLK_0 } ] -phase 0 [ get_pins { ddr3/CCC_0/pll_inst_0/OUT3 } ]",

            # ddr3/phy
            "set_false_path -to [get_pins { ddr3/DDRPHY_BLK_0/*/I_IOD_*/ARST_N }]",
            "set_false_path -to [get_pins { ddr3/DDRPHY_BLK_0/LANE_*_CTRL/I_LANECTRL/HS_IO_CLK_PAUSE } ]",
            "set_false_path -through [get_pins { ddr3/DDRPHY_BLK_0/*/I_*FEEDBACK*/Y }]",
            "set_false_path -through [get_pins { ddr3/DDRPHY_BLK_0/OB_A_12/Y }]",
            "set_false_path -through [get_pins { ddr3/DDRPHY_BLK_0/OB_DIFF_CK0/Y }]",
            "set_false_path -to [get_pins { ddr3/DDRPHY_BLK_0/LANE_*_CTRL/I_LANECTRL/DDR_READ } ]",
            "set_false_path -to [get_pins { ddr3/DDRPHY_BLK_0/LANE_*_CTRL/I_LANECTRL/RESET } ]",
            "set_false_path -to [get_pins { ddr3/DDRPHY_BLK_0/LANE_*_CTRL/I_LANECTRL/DELAY_LINE_DIRECTION } ]",
            "set_false_path -to [get_pins { ddr3/DDRPHY_BLK_0/LANE_*_CTRL/I_LANECTRL/DELAY_LINE_MOVE } ]",
            "set_false_path -through [ get_pins { ddr3/DDRPHY_BLK_0/*/I_IOD_*/DELAY_LINE_OUT_OF_RANGE } ]",
            "set_false_path -to [ get_pins { ddr3/DDRPHY_BLK_0/LANE_*_CTRL/I_LANECTRL/DELAY_LINE_LOAD DDRPHY_BLK_0/LANE_*_CTRL/I_LANECTRL/DELAY_LINE_SEL } ]",
            "set_false_path -to [ get_pins { ddr3/DDRPHY_BLK_0/LANE_*_CTRL/I_LANECTRL/SWITCH } ]",
            "set_false_path -to [ get_pins { ddr3/DDRPHY_BLK_0/LANE_*_CTRL/I_LANECTRL/READ_CLK_SEL[2] } ]",
            "set_false_path -through [get_pins { ddr3/DDRPHY_BLK_0/*/I_TRIBUFF_*/D } ]",
            "set_false_path -through [get_pins { ddr3/DDRPHY_BLK_0/*/I_TRIBUFF_*/E } ]",
            "set_false_path -through [get_pins { ddr3/DDRPHY_BLK_0/*/I_BIBUF*/D } ]",
            "set_false_path -through [get_pins { ddr3/DDRPHY_BLK_0/*/I_BIBUF*/E } ]",
            "set_false_path -through [get_pins { ddr3/DDRPHY_BLK_0/*/I_BIBUF*/Y } ]",
            "set_false_path -through [ get_pins { ddr3/DDRPHY_BLK_0/*/I_BIBUF_DIFF_DQS_*/YN } ]",
            "set_false_path -to [get_pins { ddr3/DDRPHY_BLK_0/*/I_IOD_*/FIFO_RD_PTR* } ]",
            "set_false_path -to [get_pins { ddr3/DDRPHY_BLK_0/*/I_IOD_*/RX_SYNC_RST* } ]",
            "set_false_path -to [get_pins { ddr3/DDRPHY_BLK_0/*/I_IOD_*/FIFO_WR_PTR* } ]",
            "set_false_path -to [get_pins { ddr3/DDRPHY_BLK_0/*/I_IOD_*/TX_SYNC_RST* } ]",
            "set_false_path -to [get_pins { ddr3/DDRPHY_BLK_0/*/I_IOD_*/DELAY_LINE_MOVE } ]",
            "set_multicycle_path -setup_only 2 -from [ get_cells { ddr3/DDRPHY_BLK_0/IOD_TRAINING_0/COREDDR_TIP_INT_U/TIP_CTRL_BLK/u_write_callibrator/select* } ]",
            "set_multicycle_path -setup_only 2 -from [ get_cells { ddr3/*/*/*/*/*al_init_mr_add* } ]  -to [ get_clocks { ddr3/CCC_0/pll_inst_0/OUT1 } ]",
            "set_multicycle_path -setup_only 2 -from [ get_cells { ddr3/*/*/*/*/*cal_init_mr_addr* } ] -to [ get_clocks { ddr3/CCC_0/pll_inst_0/OUT1 } ]",
        ]
