set speed "2_5"
set IBERT_directory "C:/EVT/PIC Test Control Software/PTCS3/IBERT_bitstreams"
# Program an IBERT into the VCU108

# 'speed' valid strings
#  "25": program 25  Gbps IBERT
#  "20": program 20  Gbps IBERT
#  "15": program 15  Gbps IBERT
#  "10": program 10  Gbps IBERT
#  "5": program 5   Gbps IBERT
#  "2_5": program 2.5 Gbps IBERT

# Locate files to program
set probe_file "C:/EVT/PIC Test Control Software/PTCS3/IBERT_bitstreams/example_ibert_"
set progm_file "C:/EVT/PIC Test Control Software/PTCS3/IBERT_bitstreams/example_ibert_"
append probe_file $speed "Gbps.ltx"
append progm_file  $speed "Gbps.bit"

# Program VCU108
set_property PROBES.FILE 		$probe_file [get_hw_devices xcvu095_0]
set_property FULL_PROBES.FILE 	$probe_file [get_hw_devices xcvu095_0]
set_property PROGRAM.FILE 		$progm_file [get_hw_devices xcvu095_0]
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
