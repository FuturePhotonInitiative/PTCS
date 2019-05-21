from matplotlib.colors import LinearSegmentedColormap


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
    # for list_points in data_map['Data']['Collect']:
    #     new_list = []
    #     for point in list_points:
    #         new_list.append(float(point))
    #     collected_data.append(new_list)
    # for list_points in data_map['Data']['Reduce']:
    #     new_list = []
    #     print list_points
    #     for point in list_points:
    #         new_list.append(float(point))
    #     reduced_data.append(new_list)

    collected_data.append(data_map['Data']['Collect'])
    for lst in data_map['Data']['Reduce']:
        reduced_data.append(lst)

    # Create colormap for heatmaps
    colors = [(0, 0, 0.8), (0, 0, 0.95), (0, 0, 1), (0, 0.5, 1), (0, 0.85, 1),
              (0, 1, 1), (0, 1, 0.3), (0, 1, 0), (0.7, 1, 0), (1, 1, 0),
              (1, 0.65, 0), (1, 0.5, 0), (1, 0.15, 0), (1, 0, 0), (0.65, 0, 0)]
    n = len(colors)
    colormap = LinearSegmentedColormap.from_list('Eye_Scan_Map', colors, N=n)

    # Edit points to send only center eye
    new_graph_points = []
    for d in reduced_data:
        new_graph_points.append(d[len(d) / 2 - len(d) / 10:len(d) / 2 + len(d) / 10])

    # Create csv file for Collected Data
    experiment_result.add_csv("Collected_Data", collected_data, row_labels=[])
    # Create csv file for Reduced Data
    experiment_result.add_csv("Reduced_Data", reduced_data, row_labels=[])
    # Create json file for Config used in experiment
    experiment_result.add_json_file_dict("Config", data_map['Config'])
    # Create Eyescan heat map
    experiment_result.add_heat_map(reduced_data, "Eye Scan Heat Map", colormap)
    experiment_result.add_heat_map(new_graph_points, "Eye Scan Heat Map Center Eye", colormap,
                                   graph_extent=(-1, 1, -127, 127), aspect=0.00035)



