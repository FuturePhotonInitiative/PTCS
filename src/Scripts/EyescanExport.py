def main(data_map, experiment_result):
    """
    This stage exports the eyescan through the VCU108
    :param data_map: The dictionary to store data between tasks
    :param experiment_result: ExperimentResultsModel object
    :return: None
    """
    # Ensure data points are float, not unicode as they are when sent through the data_map
    reduced_data = []
    collected_data = []
    for list_points in data_map['Data']['Collect']:
        new_list = []
        for point in list_points:
            new_list.append(float(point))
        collected_data.append(new_list)
    for list_points in data_map['Data']['Reduce']:
        new_list = []
        for point in list_points:
            new_list.append(float(point))
        reduced_data.append(new_list)

    # Create csv file for Collected Data
    experiment_result.add_csv("Collected_Data", collected_data)
    # Create csv file for Reduced Data
    experiment_result.add_csv("Reduced_Data", reduced_data)
    # Create json file for Config used in experiment
    experiment_result.add_json_file_dict("Config", data_map['Config'])
    # Create Eyescan heat map
    experiment_result.add_eyescan_heat_map(reduced_data)



