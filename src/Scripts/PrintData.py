def main(data_map, experiment_result):
    print
    print(data_map["Data"]["Initial"])
    power_source = data_map["Devices"]["Voltage_Source"]
    print(power_source.who_am_i())
    print(power_source.what_can_i())
    print(power_source.check_connected())
