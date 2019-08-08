set Horizontal_Step 1
set Vertical_Step 1

if {[info exists eyescan_ct] == 0} {set eyescan_ct -1}
incr eyescan_ct

# Running an Eyescan on a link

# set properties that form the best link. these could be edited by user. 
set_property TX_PATTERN {PRBS 31-bit} [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]
commit_hw_sio [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]

set_property RX_PATTERN {PRBS 31-bit} [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]
commit_hw_sio [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]

set_property TXPOST {0.00 dB (00000)} [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]
commit_hw_sio [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]

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
set xil_newScan [create_hw_sio_scan -description "Eye Scan Id $index" 2d_full_eye  [lindex [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX] 0 ]]
set_property HORIZONTAL_INCREMENT "$Horizontal_Step" [get_hw_sio_scans $xil_newScan]
set_property VERTICAL_INCREMENT "$Vertical_Step" [get_hw_sio_scans $xil_newScan]

# Run the scan, wait for completion, then export the data
after [expr {int(5*1000)}] 
run_hw_sio_scan [get_hw_sio_scans $xil_newScan]
wait_on_hw_sio_scan [get_hw_sio_scans $xil_newScan]
write_hw_sio_scan -force $output [get_hw_sio_scans "SCAN_$eyescan_ct"] 
