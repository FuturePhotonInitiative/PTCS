import os

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