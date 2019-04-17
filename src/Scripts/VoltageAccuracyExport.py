import time
import json
import os
import matplotlib.pyplot as plt


def main(data_map, experiment_result):
    """
    This stage exports the reduced data into plots
    :param data_map: The dictionary to store data between tasks
    :param experiment_result: ExperimentResultsModel object
    :return: None
    """
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

    # Create json file for Config used in experiment
    experiment_result.add_json_file_dict("Config", data_map['Config'])
    # Writing out collected data to csv
    experiment_result.add_csv("Collected_Data", collected_data)
    # Writing out reduced data to csv
    experiment_result.add_csv("Reduced_Data", reduced_data)

    x_axis = []
    y_axis = []
    for voltage in sorted(reduced_data):
        x_axis.append(float(voltage))
        y_axis.append(reduced_data[voltage])

    # Plot out Reduced Results
    experiment_result.add_scatter_chart("Voltage_vs_PercentError", x_axis, y_axis,
                                        title="Voltage vs Percent Error", x_label="Voltage",
                                        y_label="Percent Error")
    return
