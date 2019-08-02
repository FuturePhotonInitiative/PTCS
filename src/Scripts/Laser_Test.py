import time
def main(data_map, experiment_result):
	data_map['Data']['Collect'] = {}
	pd = data_map['Devices']['Newport OPM']
	ls = data_map['Devices']['Laser Source']
	pd.make_outputs_unverbose()
	ls.run_sweep_step(1520, 1530, 1, 2)
	start_time = time.time()
	t = (time.time() - start_time)
	ct = 5
	while t <= 25:
		if t >= ct:
			pwr = pd.get_power_reading()
			data_map['Data']['Collect'][str(ct)] = pwr
			ct = ct+1
		t = (time.time() - start_time)
