import time
import json
import os
import matplotlib.pyplot as plt


def main(data_map):
    """
    This stage exports the reduced data into plots
    :param data_map: The dictionary to store data between tasks
    :return: None
    """
    results_reduce = data_map['Data']['Reduce']
    results_collect = data_map['Data']['Collect']
    config = data_map['Config']
    # create unique file with time stamp and name of experiment
    identifier = time.strftime("%m%d%Y_%H%M%S", time.gmtime()) + "_" + str(data_map['Config']['Name'].replace(' ', '_'))

    return_path = os.getcwd()

    # create path for results if not existent
    if not os.path.exists("Results"):
        os.mkdir("Results")
    os.chdir("Results")

    # create path for unique identifier for experiment
    if not os.path.exists(identifier):
        os.mkdir(identifier)
    os.chdir(identifier)

    # Writing the config file in json format for future use
    with open("config.json", "w+") as config_file:
        # config_file.write(str(config).replace('}, ', '}, \n').replace('], ', '], \n').replace("\'", "\""))
        config_file.write(json.dumps(config, separators=(',', ": "), indent=4))

    # arrays for plotting x and y axis
    x_axis = []
    y_axis = []
    # Writing out collect results to csv
    with open("collect_results.csv", "w+") as collect_csv:
        collect_csv.write('VoltageSource,VoltageRead\n')
        for voltage in sorted(results_collect.keys()):
            collect_csv.write(str(voltage))
            for logic in results_collect[voltage]:
                collect_csv.write(',' + str(logic))
            collect_csv.write('\n')

    # Writing out and plotting reduce results to csv
    with open("reduce_results.csv", "w+") as reduce_csv:
        reduce_csv.write('Voltage,PercentError\n')
        for voltage in sorted(results_reduce.keys()):
            reduce_csv.write(str(voltage) + ',' + str(results_reduce[voltage]) + '\n')
            x_axis.append(float(voltage))
            y_axis.append(results_reduce[voltage])

    # Plot out Reduced Results
    plt.scatter(x_axis, y_axis)
    plt.autoscale()
    plt.xlabel("Voltage\n" + str(os.path) + "Voltage_vs_PercentError.png")
    plt.text(0, 0, str(os.path) + "Voltage_vs_PercentError.png")
    plt.ylabel('Percent Error')
    plt.savefig("Voltage_vs_PercentError")
    plt.show()

    os.chdir(return_path)

    return
