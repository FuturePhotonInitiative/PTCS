# Open the Main Project File & Program the Board with the PETB hardware & software

# Opening the Project 
open_project C:/EVT/PETB/Summer_2019/Vivado/PETB_R_v2.0/PETB_R_v2.0.xpr
update_compile_order -fileset sources_1

# Connecting to the device
open_hw
connect_hw_server -url localhost:3121
current_hw_target [get_hw_targets */xilinx_tcf/Digilent/210308A1C5BE]
set_property PARAM.FREQUENCY 15000000 [get_hw_targets */xilinx_tcf/Digilent/210308A1C5BE]
open_hw_target

# Program the device
set_property PROBES.FILE {C:/EVT/PETB/Summer_2019/Vivado/PETB_R_v2.0/PETB_R_v2.0.runs/impl_1/system_wrapper.ltx} [get_hw_devices xcvu095_0]
set_property FULL_PROBES.FILE {C:/EVT/PETB/Summer_2019/Vivado/PETB_R_v2.0/PETB_R_v2.0.runs/impl_1/system_wrapper.ltx} [get_hw_devices xcvu095_0]
set_property PROGRAM.FILE {C:/EVT/PETB/Summer_2019/Vivado/PETB_R_v2.0/PETB_R_v2.0.runs/impl_1/system_wrapper.bit} [get_hw_devices xcvu095_0]
program_hw_devices [get_hw_devices xcvu095_0]
refresh_hw_device [lindex [get_hw_devices xcvu095_0] 0]
