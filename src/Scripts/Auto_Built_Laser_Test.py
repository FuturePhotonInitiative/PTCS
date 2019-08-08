import time
def main(data_map, experiment_result):
	data_map['Data']['Collect'] = {}
	pd = data_map['Devices']['Newport OPM']
	ls = data_map['Devices']['Laser Source']
	start = data_map['Data']['Initial']['start_wavelength']
	end = data_map['Data']['Initial']['end_wavelength']
	w_step = data_map['Data']['Initial']['step_wavelength']
	t_step = data_map['Data']['Initial']['time_step']
	
	pd.make_outputs_unverbose()
	ls.run_sweep_step(start, end, w_step, t_step)
	start_time = time.time()
	t = (time.time() - start_time)
	ct = 5
	while t <= 25:
		if t >= ct:
			pwr = pd.get_power_reading()
			data_map['Data']['Collect'][str(ct)] = pwr
			ct = ct+1
		t = (time.time() - start_time)
