//////////////////////////////////////////////////////////////////////
// Created by SmartDesign Wed Nov 14 19:24:54 2018
// Version: PolarFire v2.3 12.200.35.9
//////////////////////////////////////////////////////////////////////

`timescale 1ns / 100ps

// osc
module osc(
    // Outputs
    RCOSC_160MHZ_GL
);

//--------------------------------------------------------------------
// Output
//--------------------------------------------------------------------
output RCOSC_160MHZ_GL;
//--------------------------------------------------------------------
// Nets
//--------------------------------------------------------------------
wire   RCOSC_160MHZ_GL_net_0;
wire   RCOSC_160MHZ_GL_net_1;
//--------------------------------------------------------------------
// Top level output port assignments
//--------------------------------------------------------------------
assign RCOSC_160MHZ_GL_net_1 = RCOSC_160MHZ_GL_net_0;
assign RCOSC_160MHZ_GL       = RCOSC_160MHZ_GL_net_1;
//--------------------------------------------------------------------
// Component instances
//--------------------------------------------------------------------
//--------osc_osc_0_PF_OSC   -   Actel:SgCore:PF_OSC:1.0.102
osc_osc_0_PF_OSC osc_0(
        // Outputs
        .RCOSC_160MHZ_GL ( RCOSC_160MHZ_GL_net_0 ) 
        );


endmodule