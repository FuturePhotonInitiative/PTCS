set link 12
set pattern "Fast Clk"
set horz_incr 1
set vert_incr 1

if {[info exists eyescan_ct] == 0} {set eyescan_ct -1}
incr eyescan_ct

# 'link' valid values
# 12: perform eyescan on channel 1
# 13: perform eyescan on channel 2
# 14: perform eyescan on channel 3
# 15: perform eyescan on channel 4

# 'pattern' valid strings
# "PRBS 7-bit"
# "PRBS 9-bit"
# "PRBS 15-bit"
# "PRBS 23-bit"
# "PRBS 31-bit"
# "Fast Clk"
# "Slow Clk"

# 'horz/vert_incr valid values
# any decimal from 1 to 16
# low incr: high accuracy & slow speed
# high incr: low accuracy & high speed

set_property TX_PATTERN {$pattern} [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]

set_property RX_PATTERN {$pattern} [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]

set_property TXPRE {0.00 dB (00000)} [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]

set_property TXPOST {0.00 dB (00000)} [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]

set_property LOGIC.TX_RESET_DATAPATH 1 [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]
commit_hw_sio [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]
set_property LOGIC.TX_RESET_DATAPATH 0 [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]
commit_hw_sio [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]

set_property LOGIC.RX_RESET_DATAPATH 1 [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]
commit_hw_sio [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]
set_property LOGIC.RX_RESET_DATAPATH 0 [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]
commit_hw_sio [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]

set_property LOGIC.MGT_ERRCNT_RESET_CTRL 1 [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]
commit_hw_sio [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]
set_property LOGIC.MGT_ERRCNT_RESET_CTRL 0 [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]
commit_hw_sio [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]

# Create the Eyescan
set xil_newScan [create_hw_sio_scan -description {Scan 0} 2d_full_eye  [lindex [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX] 0 ]]
set_property HORIZONTAL_INCREMENT $horz_incr [get_hw_sio_scans $xil_newScan]
set_property VERTICAL_INCREMENT $vert_incr [get_hw_sio_scans $xil_newScan]

# Run the scan, wait for completion, then export the data
after [expr {int(5*1000)}] 
puts "The Eye Scan has begun..."
run_hw_sio_scan [get_hw_sio_scans $xil_newScan]
wait_on_hw_sio_scan [get_hw_sio_scans $xil_newScan]
write_hw_sio_scan -force $output [get_hw_sio_scans "SCAN_$eyescan_ct"] 

puts "The data has been recorded in the file:"
puts $output
