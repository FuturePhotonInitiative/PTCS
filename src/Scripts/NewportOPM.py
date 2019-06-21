
def main(data_map, experiment_result):
    print
    opm = data_map["Devices"]["Newport OPM"]

    print(opm.what_can_i())

    print(opm.get_wavelength())
    opm.turn_on_attenuator()
    opm.set_wavelength(890)

    opm.make_outputs_verbose()
    reading = opm.get_power_reading()
    print(reading)
    opm.change_reading_units("200nW")
    print(opm.get_power_reading())

    print
