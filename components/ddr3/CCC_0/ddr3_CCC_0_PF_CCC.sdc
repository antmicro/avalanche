set_component ddr3_CCC_0_PF_CCC
# Microsemi Corp.
# Date: 2018-Nov-14 19:20:26
#

# Base clock for PLL #0
create_clock -period 10 [ get_pins { pll_inst_0/REF_CLK_0 } ]
create_generated_clock -multiply_by 4 -source [ get_pins { pll_inst_0/REF_CLK_0 } ] -phase 0 [ get_pins { pll_inst_0/OUT0 } ]
create_generated_clock -divide_by 1 -source [ get_pins { pll_inst_0/REF_CLK_0 } ] -phase 0 [ get_pins { pll_inst_0/OUT1 } ]
create_generated_clock -multiply_by 4 -source [ get_pins { pll_inst_0/REF_CLK_0 } ] -phase 0 [ get_pins { pll_inst_0/OUT2 } ]
create_generated_clock -multiply_by 4 -source [ get_pins { pll_inst_0/REF_CLK_0 } ] -phase 0 [ get_pins { pll_inst_0/OUT3 } ]
