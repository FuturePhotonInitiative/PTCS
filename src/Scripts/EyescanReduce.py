def main(data_map, experiment_result):
    """
    This stage reduces the data provided by the eyescan. No reduction needed for this test
    :param data_map: The dictionary to store data between tasks
    :param experiment_result: ExperimentResultsModel object
    :return: None
    """
    # data = data_map['Data']['Collect']
    data_map['Data']['Reduce'] = data_map['Data']['Collect']

    return
