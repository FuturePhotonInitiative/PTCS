def run(dev):
	import SPAE.src.Instruments.AgilentE3643A as Agilent
	with Agilent.AgilentE3643A(dev['VoltageSource']) as device:
		print device.run_identify()
		# print device.run_get_voltage()

		device.set_output_switch(1)
		print("Output on")

		if device.run_get_voltage() > 0:
			device.run_set_voltage(0)

		device.run_set_over_voltage(50)
		print("Over voltage set to 50")
		# voltage = 5.0
		# while voltage > 0:
		# 	device.run_set_voltage(voltage)
		# 	voltage = voltage - 0.05
		# 	time.sleep(0.5)
		device.run_set_voltage(5)

		print device.run_get_voltage()
		device.run_set_voltage(2)
		print device.run_get_voltage()

		device.set_output_switch(0)
		print("Output off")
