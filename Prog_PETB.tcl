set speed "2_5"

# Program the VCU108 with the PETB bit file & create link group

# 'speed' valid strings
#  "25": program 25  Gbps IBERT
#  "20": program 20  Gbps IBERT
#  "15": program 15  Gbps IBERT
#  "10": program 10  Gbps IBERT
#  "5": program 5   Gbps IBERT
#  "2_5": program 2.5 Gbps IBERT

# Locate files to program
set probe_file "C:/EVT/PIC Test Control Software/PTCS3/PETB_bitstreams/petb_"
set progm_file "C:/EVT/PIC Test Control Software/PTCS3/PETB_bitstreams/petb_"
append probe_file $speed "Gbps.ltx"
append progm_file  $speed "Gbps.bit"

# connect to VCU108
#open_hw
#connect_hw_server -url localhost:3121
#current_hw_target [get_hw_targets */xilinx_tcf/Digilent/210308A1D0A7]
#set_property PARAM.FREQUENCY 15000000 [get_hw_targets */xilinx_tcf/Digilent/210308A1D0A7]
#open_hw_target
#set_property PROGRAM.FILE {C:/EVT/PETB/PETB_R_Versions/PETB_R_v3.x/PETB_R_v3.0_5/PETB_R_v3.0_5.runs/impl_1/system_wrapper.bit} [get_hw_devices xcvu095_0]
#set_property PROBES.FILE {C:/EVT/PETB/PETB_R_Versions/PETB_R_v3.x/PETB_R_v3.0_5/PETB_R_v3.0_5.runs/impl_1/system_wrapper.ltx} [get_hw_devices xcvu095_0]
#set_property FULL_PROBES.FILE {C:/EVT/PETB/PETB_R_Versions/PETB_R_v3.x/PETB_R_v3.0_5/PETB_R_v3.0_5.runs/impl_1/system_wrapper.ltx} [get_hw_devices xcvu095_0]
#current_hw_device [get_hw_devices xcvu095_0]
#refresh_hw_device [lindex [get_hw_devices xcvu095_0] 0]


#Program PETB
set_property PROBES.FILE {C:/EVT/PETB/PETB_R_Versions/PETB_R_v3.x/PETB_R_v3.0_5/PETB_R_v3.0_5.runs/impl_1/system_wrapper.ltx} [get_hw_devices xcvu095_0]
set_property FULL_PROBES.FILE {C:/EVT/PETB/PETB_R_Versions/PETB_R_v3.x/PETB_R_v3.0_5/PETB_R_v3.0_5.runs/impl_1/system_wrapper.ltx} [get_hw_devices xcvu095_0]
set_property PROGRAM.FILE {C:/EVT/PETB/PETB_R_Versions/PETB_R_v3.x/PETB_R_v3.0_5/PETB_R_v3.0_5.runs/impl_1/system_wrapper.bit} [get_hw_devices xcvu095_0]
program_hw_devices [get_hw_devices xcvu095_0]
refresh_hw_device [lindex [get_hw_devices xcvu095_0] 0]


# create a link-group containing the 4 transmitter/receiver pairs on the QSFP
set xil_newLinks [list]
set xil_newLink [create_hw_sio_link -description {Link 0} [lindex [get_hw_sio_txs localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX] 0] [lindex [get_hw_sio_rxs localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX] 0] ]
lappend xil_newLinks $xil_newLink
set xil_newLink [create_hw_sio_link -description {Link 1} [lindex [get_hw_sio_txs localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/TX] 0] [lindex [get_hw_sio_rxs localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/RX] 0] ]
lappend xil_newLinks $xil_newLink
set xil_newLink [create_hw_sio_link -description {Link 2} [lindex [get_hw_sio_txs localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/TX] 0] [lindex [get_hw_sio_rxs localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/RX] 0] ]
lappend xil_newLinks $xil_newLink
set xil_newLink [create_hw_sio_link -description {Link 3} [lindex [get_hw_sio_txs localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/TX] 0] [lindex [get_hw_sio_rxs localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/RX] 0] ]
lappend xil_newLinks $xil_newLink
set xil_newLinkGroup [create_hw_sio_linkgroup -description {Link Group 0} [get_hw_sio_links $xil_newLinks]]
unset xil_newLinks