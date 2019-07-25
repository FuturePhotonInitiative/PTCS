
def main(data_map, experiment_result):
    laser = data_map["Devices"]["Laser Source"]
    opm = data_map["Devices"]["Newport OPM"]

    opm_wavelength = data_map["Data"]["Initial"]["opm_wavelength"]
    reading_units = data_map["Data"]["Initial"]["reading_units"]
    sweep_start = data_map["Data"]["Initial"]["sweep_wavelen_start"]
    sweep_end = data_map["Data"]["Initial"]["sweep_wavelen_stop"]
    sweep_step = data_map["Data"]["Initial"]["sweep_wavelen_step"]
    time_per_step = data_map["Data"]["Initial"]["time_per_step"]

    data_map["Data"]["Collect"] = {}

    opm.make_outputs_unverbose()
    opm.turn_off_attenuator()
    opm.set_wavelength(opm_wavelength)
    opm.change_reading_units(reading_units)

    laser.run_sweep_step(sweep_start, sweep_end, sweep_step, time_per_step)

    data_map["Data"]["Collect"]["sweep"] = []

    for i in range(100):
        data_map["Data"]["Collect"]["sweep"].append(opm.get_power_reading())

    laser.turn_laser_off()
