
def main(data_map, experiment_result):
    print
    opm = data_map["Devices"]["Newport OPM"]

    print(opm.get_wavelength())
    opm.turn_on_attenuator()
    opm.set_wavelength(890)

    print(opm.get_power_reading())
    opm.change_reading_units("auto")
    print(opm.get_power_reading())

    print
