import os

def main(data_map, experiment_result):
    os.system('C:/Xilinx/Vivado/2017.4/bin/vivado' + ' -mode tcl < ' + '"C:/Users/mdn4993/PycharmProjects/PTCS/Results/Tcl_Experiment_y2020_m02_d18_h14_m46_s29_us580500\combined.tcl"' + ' > ' + 'C:/Users/mdn4993/PycharmProjects/PTCS/Results/Tcl_Experiment_y2020_m02_d18_h14_m46_s29_us580500/vivado_output.txt')