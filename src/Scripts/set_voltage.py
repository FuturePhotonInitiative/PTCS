import time
def main(data_map, experiment_result):
	data_map['Data']['Collect'] = {}
	Voltage_Source = data_map['Devices']['Voltage_Source']
	print "old voltage:",
	print(Voltage_Source.get_voltage())
	Voltage_Source.set_voltage(3.20)
	print "new voltage:",
	print(Voltage_Source.get_voltage())
