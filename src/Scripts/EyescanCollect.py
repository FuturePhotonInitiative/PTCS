def main(data_map, experiment_result):
    """
    This stage runs the eyescan through the VCU108
    :param data_map: The dictionary to store data between tasks
    :param experiment_result: ExperimentResultsModel object
    :return: None
    """
    vcu108 = data_map['Devices']['Voltage_Source']
    data_map['Data']['Collect'] = [[]]
    scale_factor = float(data_map['Data']['Initial']["Scale_Factor"])
    points = float(data_map['Data']['Initial']["Points"])
    drp = float(data_map['Data']['Initial']["DRP"])

    experiment_result.start_experiment()
    data_map['Data']['Collect'] = vcu108.run_eyescan(scale_factor, points, drp)
    experiment_result.end_experiment()
    return
