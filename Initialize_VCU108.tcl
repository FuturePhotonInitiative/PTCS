# Initialize VCU108: This script opens the hardware manager, which will search for & discover
# any IBERT that has been programmed onto the VCU108

# No Parameters

# connect to VCU108
open_hw
connect_hw_server -url localhost:3121
current_hw_target [get_hw_targets */xilinx_tcf/Digilent/210308A1D0A7]
set_property PARAM.FREQUENCY 15000000 [get_hw_targets */xilinx_tcf/Digilent/210308A1D0A7]
open_hw_target
current_hw_device [get_hw_devices xcvu095_0]
refresh_hw_device -update_hw_probes false [lindex [get_hw_devices xcvu095_0] 0]

# create a link-group containing the 4 transmitter/receiver pairs on the QSFP
#set xil_newLinks [list]
#set xil_newLink [create_hw_sio_link -description {Link 0} [lindex [get_hw_sio_txs localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX] 0] [lindex [get_hw_sio_rxs localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX] 0] ]
#lappend xil_newLinks $xil_newLink
#set xil_newLink [create_hw_sio_link -description {Link 1} [lindex [get_hw_sio_txs localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/TX] 0] [lindex [get_hw_sio_rxs localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/RX] 0] ]
#lappend xil_newLinks $xil_newLink
#set xil_newLink [create_hw_sio_link -description {Link 2} [lindex [get_hw_sio_txs localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/TX] 0] [lindex [get_hw_sio_rxs localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/RX] 0] ]
#lappend xil_newLinks $xil_newLink
#set xil_newLink [create_hw_sio_link -description {Link 3} [lindex [get_hw_sio_txs localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/TX] 0] [lindex [get_hw_sio_rxs localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/RX] 0] ]
#lappend xil_newLinks $xil_newLink
#set xil_newLinkGroup [create_hw_sio_linkgroup -description {Link Group 0} [get_hw_sio_links $xil_newLinks]]
#unset xil_newLinks
