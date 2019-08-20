set pattern "PRBS 31-bit"
set error_injections 0
set trigger_link 12
set bit_count 10000000
set timer 0

# 'pattern' valid strings
# "PRBS 7-bit"
# "PRBS 9-bit"
# "PRBS 15-bit"
# "PRBS 23-bit"
# "PRBS 31-bit"
# "Fast Clk"
# "Slow Clk"

# 'error_injections' valid range
# [0,inf) 

# 'trigger_link' valid range
# 12, 13, 14, 15
# which link to count bits on?

# 'bit_count' valid range
# if == 0: dependant on timer
# if >  0: waits until number of bits have been received to record BER

# 'timer' valid range
# if bit_count != 0: ignored
# if bit_count == 0: waits 'timer' seconds before recording BER

# Set channel properties
set_property TX_PATTERN {$pattern} [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]
commit_hw_sio [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]

set_property RX_PATTERN {$pattern} [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]
commit_hw_sio [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]

set_property TXPRE {0.00 dB (00000)} [get_hw_sio_links -of_objects [get_hw_sio_linkgroups {LINKGROUP_0}]]
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

refresh_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX}]
refresh_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/RX}]
refresh_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/RX}]
refresh_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/RX}]

# Inject errors
for { set i 0 } { $i < $error_injections } { incr i } {
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

	refresh_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX}]
	refresh_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/RX}]
	refresh_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/RX}]
	refresh_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/RX}]
}

if { $bit_count > 0 } then {
	# refresh links until the words received >= the bit_count requested based on trigger_link
	while { $bit_count > [expr 0x[get_property LOGIC.RXWORD_COUNT [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y$trigger_link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y$trigger_link/RX]]] } {
		refresh_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX}]
		refresh_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/RX}]
		refresh_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/RX}]
		refresh_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/RX}]
	}
} else {
	# wait number of seconds before recording
	after [expr {int($timer*1000)}]
	refresh_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX}]
	refresh_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/RX}]
	refresh_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/RX}]
	refresh_hw_sio [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/RX}]
}

# Write bitcount, errors, and BERs to a CSV file
set bitcount12 [get_property LOGIC.RXWORD_COUNT [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX}]]
set bitcount13 [get_property LOGIC.RXWORD_COUNT [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/RX}]]
set bitcount14 [get_property LOGIC.RXWORD_COUNT [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/RX}]]
set bitcount15 [get_property LOGIC.RXWORD_COUNT [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/RX}]]

set errorcount12 [get_property LOGIC.ERRBIT_COUNT [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX}]]
set errorcount13 [get_property LOGIC.ERRBIT_COUNT [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/RX}]]
set errorcount14 [get_property LOGIC.ERRBIT_COUNT [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/RX}]]
set errorcount15 [get_property LOGIC.ERRBIT_COUNT [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/RX}]]

set ber12 [get_property RX_BER [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX}]]
set ber13 [get_property RX_BER [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/RX}]]
set ber14 [get_property RX_BER [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/RX}]]
set ber15 [get_property RX_BER [get_hw_sio_links {localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/RX}]]

set csvfile [open $output w]
puts $csvfile " ,Channel 1, Channel 2, Channel 3, Channel 4"
puts $csvfile "Word Count,$bitcount12,$bitcount13,$bitcount14,$bitcount15"
puts $csvfile "Error Count,$errorcount12,$errorcount13,$errorcount14,$errorcount15"
puts $csvfile "Bit-Error Ratio,$ber12,$ber13,$ber14,$ber15"
close $csvfile

puts "The data has been recorded in the file:"
puts $output
