# Open the Main Project File & Program the Board with the PETB hardware & software

# Opening the Project 
#open_project C:/EVT/PETB/Summer_2019/Vivado/PETB_R_v2.0/PETB_R_v2.0.xpr
#update_compile_order -fileset sources_1

# Connecting to the device
#open_hw
#connect_hw_server -url localhost:3121
#current_hw_target [get_hw_targets */xilinx_tcf/Digilent/210308A1C5BE]
#set_property PARAM.FREQUENCY 15000000 [get_hw_targets */xilinx_tcf/Digilent/210308A1C5BE]
#open_hw_target

# Program the device
#set_property PROBES.FILE {C:/EVT/PETB/Summer_2019/Vivado/PETB_R_v2.0/PETB_R_v2.0.runs/impl_1/system_wrapper.ltx} [get_hw_devices xcvu095_0]
#set_property FULL_PROBES.FILE {C:/EVT/PETB/Summer_2019/Vivado/PETB_R_v2.0/PETB_R_v2.0.runs/impl_1/system_wrapper.ltx} [get_hw_devices xcvu095_0]
#set_property PROGRAM.FILE {C:/EVT/PETB/Summer_2019/Vivado/PETB_R_v2.0/PETB_R_v2.0.runs/impl_1/system_wrapper.bit} [get_hw_devices xcvu095_0]
#program_hw_devices [get_hw_devices xcvu095_0]
#refresh_hw_device [lindex [get_hw_devices xcvu095_0] 0]

#refresh_hw_device -update_hw_probes false [lindex [get_hw_devices xcvu095_0] 0]

open_hw
connect_hw_server -url localhost:3121
current_hw_target [get_hw_targets */xilinx_tcf/Digilent/210308A1C5BE]
set_property PARAM.FREQUENCY 15000000 [get_hw_targets */xilinx_tcf/Digilent/210308A1C5BE]
open_hw_target
current_hw_device [get_hw_devices xcvu095_0]
refresh_hw_device -update_hw_probes false [lindex [get_hw_devices xcvu095_0] 0]

set xil_newLinks [list]
set xil_newLink [create_hw_sio_link -description {Link 0} [lindex [get_hw_sio_txs localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX] 0] [lindex [get_hw_sio_rxs localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX] 0] ]
lappend xil_newLinks $xil_newLink
set xil_newLink [create_hw_sio_link -description {Link 1} [lindex [get_hw_sio_txs localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/TX] 0] [lindex [get_hw_sio_rxs localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/RX] 0] ]
lappend xil_newLinks $xil_newLink
set xil_newLink [create_hw_sio_link -description {Link 2} [lindex [get_hw_sio_txs localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/TX] 0] [lindex [get_hw_sio_rxs localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/RX] 0] ]
lappend xil_newLinks $xil_newLink
set xil_newLink [create_hw_sio_link -description {Link 3} [lindex [get_hw_sio_txs localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/TX] 0] [lindex [get_hw_sio_rxs localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/RX] 0] ]
lappend xil_newLinks $xil_newLink
set xil_newLinkGroup [create_hw_sio_linkgroup -description {Link Group 0} [get_hw_sio_links $xil_newLinks]]
unset xil_newLinks
