import time
def main(data_map, experiment_result):
	data_map['Data']['Collect'] = {}
	ls = data_map['Devices']['Laser Source']
	ls.enter_password()
