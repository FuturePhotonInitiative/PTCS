import os
import datetime
from threading import Thread

from src import Prober
from src.GUI.Util import Globals
from src.GUI.Util.Functions import clean_name_for_file

from src.GUI.Model.ExperimentModel import Experiment


class QueueRunner(Thread):
    """
    Thread class to run a provided queue
    """

    def __init__(self, queue, working_directory, queue_result):
        """
        Create a new QueueRunner that will run the provided queue using the provided temporary directory
        :param queue:
            The queue to run with Prober
        :param working_directory:
            The directory to store the temporary json file for the experiment on which we will call Prober
        """
        Thread.__init__(self)
        self.queue = queue
        self.queue_result = queue_result
        self.tmp_dir = working_directory
        # Initialize the status of all of the experiments in the queue to "not yet run"
        self.experiment_status = {}
        for i in range(len(queue)):
            self.experiment_status[queue.get_ith_experiment(i)] = -1
        self.current_experiment = None


    def run_standard(self):
        """
        Run the provided queue
        :return:
            Nothing
        """
        print "\n====================\nStarting the Queue\n====================\n"
        self.queue_result.start_queue()
        # TODO catch any exceptions run by prober and try to continue, but only if a flag in the __init__ has been
        # set
        self.queue.schedule_experiments()
        for i in range(len(self.queue)):
            self.current_experiment = self.queue.get_ith_experiment(i)
            self.experiment_status[self.current_experiment] = 0
            # The file to store the json to call prober on to run the experiment

            tmp_file_name = self.tmp_dir + "/tmp" + self.current_experiment.get_name().replace(" ", "_") + ".json"
            self.current_experiment.export_to_json(tmp_file_name)
            Prober.main(["Prober.py", tmp_file_name], config_manager=Globals.systemConfigManager, queue_result=self.queue_result)
            self.experiment_status[self.current_experiment] = 1
            os.remove(tmp_file_name)
        self.current_experiment = None
        self.queue_result.end_queue()
        self.queue_result.save()
        print "\n====================\nQueue has finished\n====================\n"

    def run_tcl_tests(self, target_location="C:\\Users\\ofs9424\\SPAE\\TCL\\combined.tcl"):
        """
                Run the provided queue
                :return:
                    Nothing
                """
        print "\n====================\nStarting the Queue\n====================\n"
        self.queue_result.start_queue()
        # TODO catch any exceptions run by prober and try to continue, but only if a flag in the __init__ has been
        # set
        self.queue.schedule_experiments()
        now = datetime.datetime.today()

        name = "Tcl_Experiment" + str(now)
        name = clean_name_for_file(name)
        result_dir = Globals.systemConfigManager.get_results_manager().results_root
        master_tcl = ""
        for i in range(len(self.queue)):
            with open(self.queue.get_ith_experiment(i).tcl_file, "r") as f:
                done_sets = False
                master_tcl += "set output \"" + result_dir + "/" + name + "/Collected_Data" + str(i+1) + ".csv\"\n"
                for line in f.readlines():
                    if not done_sets:
                        if not line.startswith("set"):
                            done_sets = True
                        else:
                            words = line.split(' ')
                            val = words[1]
                            for k in self.queue.get_ith_experiment(i).config_dict['Data'].keys():
                                if k == val:
                                    line = words[0]+" "+words[1]+" "+str(self.queue.get_ith_experiment(i).config_dict['Data'][k]) + "\n"
                    master_tcl += line
        with open(target_location, "w") as f:
            f.writelines(master_tcl)

        master_experiment = Experiment("..\\..\\template.json")
        for i in range(len(self.queue)):
            if self.queue.get_ith_experiment(i).config_dict.get('Devices', None) is not None:
                for key in self.queue.get_ith_experiment(i).config_dict['Devices']:
                    if key not in master_experiment.config_dict['Devices']:
                        master_experiment.config_dict['Devices'].append(key)
        tmp_file_name = self.tmp_dir + "\\tmp\\" + master_experiment.get_name().replace(" ", "_") + ".json"
        pyLoc = self.tmp_dir + "\\..\\..\\src\\Scripts\\script.py"
        exp = dict()
        exp['Type'] = 'PY_SCRIPT'
        exp['Source'] = 'script.py'
        exp['Order'] = 1
        with open(pyLoc, "w") as f:
            f.write(("import os\ndef main(data_map, experiment_result):\n\tos.system('C:\\Xilinx\\Vivado\\2017.4\\bin\\vivado -mode tcl < ' + '" + target_location + "')").replace('\\', '\\\\'))
        master_experiment.config_dict['Experiment'].append(exp)
        print "exporting to " + tmp_file_name
        master_experiment.export_to_json(tmp_file_name)
        Prober.main(["Prober.py", tmp_file_name], config_manager=Globals.systemConfigManager,
                    queue_result=self.queue_result)

        # for i in range(len(self.queue)):
        #     self.current_experiment = self.queue.get_ith_experiment(i)
        #     self.experiment_status[self.current_experiment] = 0
        #     # The file to store the json to call prober on to run the experiment
        #     if self.current_experiment.config_dict.get('Experiment', None) is not None:
        #         self.current_experiment.config_dict['Data']['Tcl_Script_Location'] = target_location
        #         tmp_file_name = self.tmp_dir + "/tmp" + self.current_experiment.get_name().replace(" ", "_") + ".json"
        #         self.current_experiment.export_to_json(tmp_file_name)
        #         Prober.main(["Prober.py", tmp_file_name], config_manager=Globals.systemConfigManager, queue_result=self.queue_result)
        #         self.experiment_status[self.current_experiment] = 1
        #         os.remove(tmp_file_name)
        # self.current_experiment = None

        self.queue_result.end_queue()
        self.queue_result.save()
        print "\n====================\nQueue has finished\n====================\n"

    def run(self):
        self.run_tcl_tests()
        #self.run_standard()

    def get_current_experiment(self):
        """
        :return:
            The experiment this class is currently running, or None if the thread has not yet been started or
            has finished
        """
        return self.current_experiment

    def get_run_status(self, experiment):
        """
        :param experiment:
            The experiment object to get the run status of
        :return:
            The current run status of the provided experiment in the currently running queue
        """
        return self.experiment_status[experiment]