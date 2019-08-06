
def main(data_map, experiment_result):
    osc = data_map["Devices"]["Oscilloscope"]
    print(osc.measure_vaverage(channel_num=2))
