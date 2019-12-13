set link 12 
set speed 0

# Change the Rate of the Transceiver Speed before running BERT or Eyescan

# 'link' valid values
# 12: change speed on channel 1
# 13: change speed on channel 2
# 14: change speed on channel 3
# 15: change speed on channel 4

# 'speed' valid values
# 0: Default speed 
# 1: Speed Divided by 1
# 2: Speed Divided by 2
# 3: Speed Divided by 4
# 4: Speed Divided by 8
# 5: Speed Divided by 16
# 6: Speed Divided by 32
# 7: Speed Diveded by 1 (don't ask me why)

# set txrate & rxrate speeds
set_property PORT.RXRATE $speed [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]

set_property PORT.TXRATE $speed [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]

# reset transmission & receiver after affecting the rate
set_property LOGIC.TX_RESET_DATAPATH 1 [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]
set_property LOGIC.TX_RESET_DATAPATH 0 [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]

set_property LOGIC.RX_RESET_DATAPATH 1 [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]
set_property LOGIC.RX_RESET_DATAPATH 0 [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]

set_property LOGIC.MGT_ERRCNT_RESET_CTRL 1 [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]
set_property LOGIC.MGT_ERRCNT_RESET_CTRL 0 [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y$link/RX]
