# Running a BERT on all four links

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

# ---------------------------- Can be repeated depending on number of errors desired to inject ----------------------------

# Injecting Error into Link 12
set_property LOGIC.ERR_INJECT_CTRL 1 [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX}]
commit_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX}]
set_property LOGIC.ERR_INJECT_CTRL 0 [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX}]
commit_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX}]

# Injecting Error into Link 13
set_property LOGIC.ERR_INJECT_CTRL 1 [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/RX}]
commit_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/RX}]
set_property LOGIC.ERR_INJECT_CTRL 0 [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/RX}]
commit_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/RX}]

# Injecting Error into Link 14
set_property LOGIC.ERR_INJECT_CTRL 1 [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/RX}]
commit_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/RX}]
set_property LOGIC.ERR_INJECT_CTRL 0 [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/RX}]
commit_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/RX}]

# Injecting Error into Link 15
set_property LOGIC.ERR_INJECT_CTRL 1 [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/RX}]
commit_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/RX}]
set_property LOGIC.ERR_INJECT_CTRL 0 [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/RX}]
commit_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/RX}]

# ---------------------------- End of repeatable code ----------------------------

# force refresh before saving in file 
refresh_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX}]
refresh_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/RX}]
refresh_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/RX}]
refresh_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/RX}]

# Write errors and BERs to a CSV file
set errorcount12 [get_property LOGIC.ERRBIT_COUNT [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX}]]
set errorcount13 [get_property LOGIC.ERRBIT_COUNT [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/RX}]]
set errorcount14 [get_property LOGIC.ERRBIT_COUNT [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/RX}]]
set errorcount15 [get_property LOGIC.ERRBIT_COUNT [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/RX}]]

set ber12 [get_property RX_BER [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX}]]
set ber13 [get_property RX_BER [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/RX}]]
set ber14 [get_property RX_BER [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/RX}]]
set ber15 [get_property RX_BER [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/RX}]]

set csvfile [open $output w]
puts $csvfile "$errorcount12,$errorcount13,$errorcount14,$errorcount15"
puts $csvfile "$ber12,$ber13,$ber14,$ber15"
close $csvfile
