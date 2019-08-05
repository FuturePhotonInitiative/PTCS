import time
def main(data_map, experiment_result):
	data_map['Data']['Collect'] = {}
	Laser_Source = data_map['Devices']['Laser Source']
	Laser_Source.turn_laser_off()
