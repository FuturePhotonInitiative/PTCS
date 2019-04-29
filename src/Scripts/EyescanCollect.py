def main(data_map, experiment_result):
    """
    This stage runs the eyescan through the VCU108
    :param data_map: The dictionary to store data between tasks
    :param experiment_result: ExperimentResultsModel object
    :return: None
    """
    vcu108 = data_map['Devices']['VCU 108']
    data_map['Data']['Collect'] = [[]]
    range = int(data_map['Data']['Initial']["Range"])
    scale = int(data_map['Data']['Initial']["Scale"])
    horizontal = int(data_map['Data']['Initial']["Horizontal_Boundary"])
    vertical = int(data_map['Data']['Initial']["Vertical_Boundary"])
    drp = int(data_map['Data']['Initial']["DRP"])
    step = int(data_map['Data']['Initial']["Step"])

    vcu108.device.baud_rate = 115200
    vcu108.device.read_termination = '\n'

    experiment_result.start_experiment()
    data_map['Data']['Collect'] = vcu108.run_eyescan(range_value=range, scale_factor=scale, horizontal=horizontal,
                                                     vertical=vertical, drp=drp, step=step)
    experiment_result.end_experiment()
    return
