import os.path as op
import matplotlib.pyplot as plt


def write_to_file(file_name, data):
    with open(file_name, "w") as out_file:
        out_file.write("\n".join(data))


def main(data_map, results):
    """
    Saves the four data groupings and plots the reduced data on a graph, saves the graph
    """
    laser_power1 = str(data_map["Data"]["Initial"]["laser_power1"])
    laser_power2 = str(data_map["Data"]["Initial"]["laser_power2"])

    raw1 = data_map["Data"]["Collect"][laser_power1]
    raw2 = data_map["Data"]["Collect"][laser_power2]
    reduced1 = data_map["Data"]["Reduce"][laser_power1]
    reduced2 = data_map["Data"]["Reduce"][laser_power2]

    save_dir = results.experiment_results_directory

    raw1_name = op.join(save_dir, "Raw data {}dBm.txt".format(laser_power1))
    raw2_name = op.join(save_dir, "Raw data {}dBm.txt".format(laser_power2))
    reduced1_name = op.join(save_dir, "Reduced data {}dBm.txt".format(laser_power1))
    reduced2_name = op.join(save_dir, "Reduced data {}dBm.txt".format(laser_power2))

    write_to_file(raw1_name, raw1)
    write_to_file(raw2_name, raw2)
    write_to_file(reduced1_name, [str(i) for i in reduced1])
    write_to_file(reduced2_name, [str(i) for i in reduced2])

    results.add_result_file(raw1_name)
    results.add_result_file(raw2_name)
    results.add_result_file(reduced1_name)
    results.add_result_file(reduced2_name)

    plot_path = op.join(save_dir, "pyplot.png")

    plt.figure(1)
    plt.plot(reduced1, color="y", label="{}dBm".format(laser_power1))
    plt.plot(reduced2, color="k", label="{}dBm".format(laser_power2))
    plt.legend()
    plt.xlabel("Sample Number (sequential)")
    plt.ylabel("Optical Power (W)")
    plt.savefig(plot_path)

    results.add_result_file(plot_path)
