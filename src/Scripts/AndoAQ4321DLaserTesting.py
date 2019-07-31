import time


def main(data_map, two):
    device = data_map["Devices"]["Laser Source"]
    # device.enter_password()

    device.set_optical_power(0)
    device.set_wavelength(1600)
    
    device.run_sweep_step(1520, 1525, .05, .1)
    device.run_sweep_continuous(1520, 1525, 3.1)

    device.turn_laser_off()
    device.unlock_screen()
