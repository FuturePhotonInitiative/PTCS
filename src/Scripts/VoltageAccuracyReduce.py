def main(data_map):
    """
    This stage reduces the collected voltage and reduces it to a percent error
    :param data_map: The dictionary to store data between tasks
    :return: None
    """
    samples = data_map['Data']['Collect']
    data_map['Data']['Reduce'] = {}

    for voltage in samples.keys():
        data_map['Data']['Reduce'][voltage] = 100.0 * (abs(voltage - samples[voltage])/voltage)
    return
