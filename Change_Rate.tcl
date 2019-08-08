set Speed_Index 1

# Change the Rate of the Transceiver Speed before running BERT or Eyescan

# These two numbers on rxrate and txrate control the speed, and must match
#						*v*
set_property PORT.RXRATE "$Speed_Index" [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX] 

set_property PORT.TXRATE "$Speed_Index" [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1C5BE/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX] 

# 0: Default speed (25 Gbps)
# 1: Speed Divided by 1
# 2: Speed Divided by 2
# 3: Speed Divided by 4
# 4: Speed Divided by 8
# 5: Speed Divided by 16
# 6: Speed Divided by 32
# 7: Speed Diveded by 1 (don't ask me why)

# reset transmission & receiver after affecting the rate
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
