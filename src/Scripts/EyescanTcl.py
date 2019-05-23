import os
from matplotlib.colors import LinearSegmentedColormap
import csv

def main(data_map, experiment_result):
    vcu108 = data_map['Devices']['VCU 108']
    data_map['Data']['Collect'] = [[]]
    range = int(data_map['Data']['Initial']["Range"])
    scale = int(data_map['Data']['Initial']["Scale"])
    horizontal = int(data_map['Data']['Initial']["Horizontal_Boundary"])
    vertical = int(data_map['Data']['Initial']["Vertical_Boundary"])
    drp = int(data_map['Data']['Initial']["DRP"])
    horiz_step = int(data_map['Data']['Initial']["Horizontal_Step"])
    vert_step = int(data_map['Data']['Initial']["Vertical_Step"])
    tcl_location = str(data_map['Data']['Initial']["Tcl_Script_Location"])
    os.chdir(experiment_result.experiment_results_directory)
    with open(tcl_location, "r") as file:
        script = file.readlines()
    if horiz_step > 0:
        script[0] = "set horiz " + str(horiz_step) + "\n"
    if vert_step > 0:
        script[1] = "set vert " + str(vert_step) + "\n"
    script[2] = "set output " + experiment_result.experiment_results_directory + "/Collected_Data.csv\n"
    newscript = experiment_result.experiment_results_directory + "\\" + tcl_location.split("\\")[-1]
    with open(newscript, "w") as newfile:
        newfile.writelines(script)
    os.system('C:\\Xilinx\\Vivado\\2017.4\\bin\\vivado -mode tcl < ' + newscript)

    # Create colormap for heatmaps
    colors = [(0, 0, 0.8), (0, 0, 0.95), (0, 0, 1), (0, 0.5, 1), (0, 0.85, 1),
              (0, 1, 1), (0, 1, 0.3), (0, 1, 0), (0.7, 1, 0), (1, 1, 0),
              (1, 0.65, 0), (1, 0.5, 0), (1, 0.15, 0), (1, 0, 0), (0.65, 0, 0)]
    n = len(colors)
    colormap = LinearSegmentedColormap.from_list('Eye_Scan_Map', colors, N=n)

    reduced = []
    with open(experiment_result.experiment_results_directory + "/Collected_Data.csv") as data:
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

    experiment_result.add_heat_map(reduced, "Eye Scan Heat Map", colormap, vmax=25)