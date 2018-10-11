import visa
import VCU108_IPI

resourceManager = visa.ResourceManager()

device = resourceManager.open_resource("COM5", write_termination='\n', read_termination='\n', baud_rate='115200',
                                       data_bits=8, flow_control=0, parity=visa.constants.Parity.none,
                                       stop_bits=visa.constants.StopBits.one)

board = VCU108_IPI.VCU108(device)
print board.who_am_i()
print board.run_LED()
