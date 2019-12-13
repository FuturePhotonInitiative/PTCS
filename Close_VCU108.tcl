# Reset all links to default speed, then exit the hardware manager

# No Parameters

# the rate should be set to the default value before closing, else it will start will the non-default speed on startup
set_property PORT.RXRATE 0 [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX]
set_property PORT.TXRATE 0 [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y12/RX]

set_property PORT.RXRATE 0 [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/RX]
set_property PORT.TXRATE 0 [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y13/RX]

set_property PORT.RXRATE 0 [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/RX]
set_property PORT.TXRATE 0 [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y14/RX]

set_property PORT.RXRATE 0 [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/RX]
set_property PORT.TXRATE 0 [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/RX]
commit_hw_sio [get_hw_sio_links localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/TX->localhost:3121/xilinx_tcf/Digilent/210308A1D0A7/0_1_0_0/IBERT/Quad_127/MGT_X0Y15/RX]

close_hw
