import os
from threading import Thread

from src import Prober
from src.GUI.Util import Globals


class QueueRunner(Thread):
    """
    Thread class to run a provided queue
    """

    def __init__(self, queue, working_directory):
        """
        Create a new QueueRunner that will run the provided queue using the provided temporary directory
        :param queue:
            The queue to run with Prober
        :param working_directory:
            The directory to store the temporary json file for the experiment on which we will call Prober
        """
        Thread.__init__(self)
        self.queue = queue
        self.tmp_dir = working_directory
        # Initialize the status of all of the experiments in the queue to "not yet run"
        self.experiment_status = {}
        for i in range(len(queue)):
            self.experiment_status[queue.get_ith_experiment(i)] = -1
        self.current_experiment = None

    def run(self):
        """
        Run the provided queue
        :return:
            Nothing
        """
        print "Starting the Queue"
        # TODO catch any exceptions run by prober and try to continue, but only if a flag in the __init__ has been
        # set
        self.queue.schedule_experiments()
        for i in range(len(self.queue)):
            self.current_experiment = self.queue.get_ith_experiment(i)
            self.experiment_status[self.current_experiment] = 0
            # The file to store the json to call prober on to run the experiment

            tmp_file_name = self.tmp_dir + "/tmp" + self.current_experiment.get_name().replace(" ", "_") + ".json"
            self.current_experiment.export_to_json(tmp_file_name)
            Prober.main(["Prober.py", tmp_file_name], config_manager=Globals.systemConfigManager)
            self.experiment_status[self.current_experiment] = 1
            os.remove(tmp_file_name)
        self.current_experiment = None

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