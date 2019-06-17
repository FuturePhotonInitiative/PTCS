def main(data_map, experiment_result):
    print
    print(data_map["Data"]["Initial"])
    device = data_map["Devices"]["Newport OPM"]

    print(device.run_get_wavelength())
    #print(device.run_get_power())





