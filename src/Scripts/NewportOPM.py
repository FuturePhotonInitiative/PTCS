
def main(data_map, experiment_result):
    print
    opm = data_map["Devices"]["Newport OPM"]

    print(opm.run_get_wavelength())

    opm.run_turn_on_attenuator()
    opm.run_set_wavelength(890)

    opm.run_make_outputs_verbose()
    reading = opm.run_get_power_reading()
    print(reading)
    opm.run_change_reading_units("200nW")
    print(opm.run_get_power_reading())

    print
