import os.path as op
import matplotlib.pyplot as plt


def write_to_file(file_name, data):
    with open(file_name, "w") as out_file:
        out_file.write("\n".join(data))


def main(data_map, results):

    save_dir = results.experiment_results_directory
    sweep_data = data_map["Data"]["Collect"]["sweep"]
    sweep_data_name = op.join(save_dir, "collected-sweep-data.txt")
    write_to_file(sweep_data_name, sweep_data)
    results.add_result_file(sweep_data_name)

    plot_path = op.join(save_dir, "pyplot.png")

    plt.figure(1)
    plt.plot(sweep_data, color="y", label="sweep")
    plt.savefig(plot_path)

    results.add_result_file(plot_path)
