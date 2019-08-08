
def main(data_map, experiment_result):
    laser = data_map["Devices"]["Laser Source"]
    opm = data_map["Devices"]["Newport OPM"]

    opm_wavelength = data_map["Data"]["Initial"]["opm_wavelength"]
    reading_units = data_map["Data"]["Initial"]["reading_units"]
    sweep_start = data_map["Data"]["Initial"]["sweep_wavelen_start"]
    sweep_end = data_map["Data"]["Initial"]["sweep_wavelen_stop"]
    total_sweep_time = data_map["Data"]["Initial"]["total_sweep_time"]

    data_map["Data"]["Collect"] = {}

    opm.make_outputs_unverbose()
    opm.turn_off_attenuator()
    opm.set_wavelength(opm_wavelength)
    opm.change_reading_units(reading_units)

    data_map["Data"]["Collect"]["sweep"] = []

    laser.turn_laser_on()
    laser.run_sweep_continuous(sweep_start, sweep_end, total_sweep_time)

    while laser.sweep_in_progress():
        data_map["Data"]["Collect"]["sweep"].append(opm.get_power_reading())

    laser.turn_laser_off()
