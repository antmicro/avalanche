//////////////////////////////////////////////////////////////////////
// Created by SmartDesign Wed Nov 14 19:25:14 2018
// Version: PolarFire v2.3 12.200.35.9
//////////////////////////////////////////////////////////////////////

`timescale 1ns / 100ps

// ccc
module ccc(
    // Inputs
    REF_CLK_0,
    // Outputs
    OUT0_FABCLK_0,
    PLL_LOCK_0
);

//--------------------------------------------------------------------
// Input
//--------------------------------------------------------------------
input  REF_CLK_0;
//--------------------------------------------------------------------
// Output
//--------------------------------------------------------------------
output OUT0_FABCLK_0;
output PLL_LOCK_0;
//--------------------------------------------------------------------
// Nets
//--------------------------------------------------------------------
wire   OUT0_FABCLK_0_net_0;
wire   PLL_LOCK_0_net_0;
wire   REF_CLK_0;
wire   OUT0_FABCLK_0_net_1;
wire   PLL_LOCK_0_net_1;
//--------------------------------------------------------------------
// TiedOff Nets
//--------------------------------------------------------------------
wire   GND_net;
wire   [10:0]DRI_CTRL_0_const_net_0;
wire   [32:0]DRI_WDATA_0_const_net_0;
wire   [10:0]DRI_CTRL_1_const_net_0;
wire   [32:0]DRI_WDATA_1_const_net_0;
wire   [10:0]DLL_DRI_CTRL_const_net_0;
wire   [32:0]DLL_DRI_WDATA_const_net_0;
//--------------------------------------------------------------------
// Constant assignments
//--------------------------------------------------------------------
assign GND_net                   = 1'b0;
assign DRI_CTRL_0_const_net_0    = 11'h000;
assign DRI_WDATA_0_const_net_0   = 33'h000000000;
assign DRI_CTRL_1_const_net_0    = 11'h000;
assign DRI_WDATA_1_const_net_0   = 33'h000000000;
assign DLL_DRI_CTRL_const_net_0  = 11'h000;
assign DLL_DRI_WDATA_const_net_0 = 33'h000000000;
//--------------------------------------------------------------------
// Top level output port assignments
//--------------------------------------------------------------------
assign OUT0_FABCLK_0_net_1 = OUT0_FABCLK_0_net_0;
assign OUT0_FABCLK_0       = OUT0_FABCLK_0_net_1;
assign PLL_LOCK_0_net_1    = PLL_LOCK_0_net_0;
assign PLL_LOCK_0          = PLL_LOCK_0_net_1;
//--------------------------------------------------------------------
// Component instances
//--------------------------------------------------------------------
//--------ccc_ccc_0_PF_CCC   -   Actel:SgCore:PF_CCC:1.0.115
ccc_ccc_0_PF_CCC ccc_0(
        // Inputs
        .REF_CLK_0     ( REF_CLK_0 ),
        // Outputs
        .OUT0_FABCLK_0 ( OUT0_FABCLK_0_net_0 ),
        .PLL_LOCK_0    ( PLL_LOCK_0_net_0 ) 
        );


endmodule
