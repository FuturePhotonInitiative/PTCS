import time
def main(data_map, experiment_result):
	data_map['Data']['Collect'] = {}
	VCU_108 = data_map['Devices']['VCU 108']
	VCU_108.vcu108_gpio_toggle(1)
