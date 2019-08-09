import os.path as op
import matplotlib.pyplot as plt
import numpy as np


def write_to_file(file_name, data):
    with open(file_name, "w") as out_file:
        out_file.write("\n".join(data))


def main(data_map, results):

    save_dir = results.experiment_results_directory
    collected_data = data_map["Data"]["Collect"]["sweep"]
    reduced_data = data_map["Data"]["Reduce"]
    sweep_start = data_map["Data"]["Initial"]["sweep_wavelen_start"]
    sweep_end = data_map["Data"]["Initial"]["sweep_wavelen_stop"]

    collect_data_name = op.join(save_dir, "collected-sweep-data.txt")
    write_to_file(collect_data_name, collected_data)
    results.add_result_file(collect_data_name)

    reduced_data_name = op.join(save_dir, "reduced-sweep-data.txt")
    write_to_file(reduced_data_name, [str(i) for i in reduced_data])
    results.add_result_file(reduced_data_name)

    plot_path = op.join(save_dir, "pyplot.png")

    plt.figure()

    x_axis = np.arange(sweep_start, sweep_end, float(abs(sweep_end - sweep_start)) / len(reduced_data))
    plt.plot(x_axis, reduced_data, color="y", label="Sweep from {}nm to {}nm".format(sweep_start, sweep_end))
    plt.legend()
    plt.xlabel("Wavelength")
    plt.ylabel("Optical Power (W)")
    plt.savefig(plot_path, bbox_inches="tight")

    results.add_result_file(plot_path)
