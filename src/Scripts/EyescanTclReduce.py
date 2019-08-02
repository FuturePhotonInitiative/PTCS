from matplotlib.colors import LinearSegmentedColormap
import os
import csv


def main(data_map, experiment_result):
    # Create colormap for heatmaps
    colors = [(0, 0, 0.8), (0, 0, 0.95), (0, 0, 1), (0, 0.5, 1), (0, 0.85, 1),
              (0, 1, 1), (0, 1, 0.3), (0, 1, 0), (0.7, 1, 0), (1, 1, 0),
              (1, 0.65, 0), (1, 0.5, 0), (1, 0.15, 0), (1, 0, 0), (0.65, 0, 0)]
    n = len(colors)

    colormap = LinearSegmentedColormap.from_list('Eye_Scan_Map', colors, N=n)

    dr = experiment_result.experiment_results_directory

    for test in os.listdir(dr):
        if test.startswith("Eyescan__Tcl__"):
            index = test[14:]
            reduced = []
            with open(dr + "/" + test + "/Collected_Data.csv") as data:
                reader = csv.reader(data, delimiter=',')
                ind = 0
                for row in reader:
                    ind += 1
                    if ind >= 23:
                        lyst = row[1:]
                        if len(lyst) > 0:
                            floatrow = []
                            for v in lyst:
                                floatrow.append(float(v) * 200.0)
                            reduced.append(floatrow)

            experiment_result.add_heat_map(reduced, "Eye Scan Heat Map",
                                           colormap, path=test + "/Eye Scan Heat Map", vmax=25)
