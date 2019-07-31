import os

from QueueRunner import QueueRunner
from src.GUI.Model.ExperimentQueue import ExperimentQueue
from src.GUI.Model.ExperimentModel import Experiment


class QueueManager:
    def __init__(self, temp_dir, results_config_manager):
        self.results_config_manager = results_config_manager
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        self.runner = None
        self.experiment_queue = ExperimentQueue()

    def remove_from_queue(self, experiment):
        self.experiment_queue.remove_from_queue(experiment)

    def get_ith_experiment(self, index):
        return self.experiment_queue.get_ith_experiment(index)

    def run_queue(self, to_run):
        """
            Starts the thread that runs the queue.
        :param to_run:
            The queue to be run
        :return:
            None, immediately
        """
        if self.runner is None:
            queue_result = self.results_config_manager.get_results_manager().make_new_queue_result()
            runner = QueueRunner(to_run, queue_result)
            runner.start()

    def queue_is_running(self):
        """
        :return:
            True if the runner thread has been started and has not yet terminated,
            false otherwise
        """
        return (self.runner is not None) and (self.runner.isAlive())

    def join_on_running_queue(self, timeout=None):
        """
        Block until the runner thread finishes, and join on that thread
        :param timeout:
            The amount of time to wait to join. If not present or None, this call will block until successfully joined.
            Otherwise function will return on a successful join or after <timeout> seconds have passed.  If a timeout
            is specified, queue_is_running() be called to check if there was a successful join or if the timeout was
            reached.  If queue_is_running() returns true, the timeout was reached, otherwise the join was successful.
        :return:
            None, once the runner thread has finished
        """
        if self.runner is not None:
            self.runner.join(timeout)

    def get_experiment_status(self, experiment):
        """
        Gets the status of the provided experiment
        :param experiment:
            The experiment to check the status of
        :return:
            -1 if the experiment has not yet been run, 0 if the experiment is currently running, or 1 if the experiment
            has finished running.
        """
        if self.runner is not None:
            return self.runner.get_run_status(experiment)
        # Return not yet run if the runner has not yet been started
        return -1

    def get_current_experiment(self):
        """
        :return:
            The experiment that the runner thread is currently running, or None if no experiments are running
        """
        if self.runner is not None:
            return self.runner.get_current_experiment()
        return None

    def get_experiment_names(self):
        return self.experiment_queue.get_experiment_names()

    def add_to_queue(self, experiment):
        self.experiment_queue.add_to_queue(experiment)

    def run(self):
        self.run_queue(self.experiment_queue)

    def clear_queue(self):
        self.experiment_queue.clear_queue()

    def save_queue_to_file(self, folder_path, name):
        """
        Save the queue to a file
        :param folder_path:
            The folder to save it in.
        :return:
            The index of the saved queue
        """
        index = len(os.listdir(folder_path)) + 1
        output = ""
        for i in range(len(self.experiment_queue)):
            exp = self.experiment_queue.get_ith_experiment(i)
            output += "*" + exp.config_file_name.split("/")[-1][:-5] + "\n"
            for field in (exp.config.data.keys() if exp.config.data else dict()):
                output += str(exp.config.data[field]) + " // " + str(field) + "\n"

        with open(folder_path + "/Saved_Experiment_" + name, "w") as f:
            f.write(output)
        return index

    def read_queue_from_file(self, file_path, config_root):
        """
        Construct a queue from a file
        :param file_path:
            The file to read from.
        :param config_root:
            The folder to read config files from.
        :return:
            The constructed queue.
        """
        rqueue = []
        if not os.path.isfile(file_path):
            return False
        with open(file_path) as f:
            exp = None
            for line in f.readlines():
                if line.startswith('*'):
                    if exp is not None:
                        rqueue.append(exp)
                    exp = Experiment(line[1:-1] + ".json")
                else:
                    ind = line.find(' // ')
                    if ind > -1:
                        val = line[:ind]
                        if len(val) > 0 and ('0' <= val[0] <= '9' or val[0] == '.'):
                            try:
                                val = int(val)
                            except ValueError:
                                ux = 0
                                while val[ux] in ' .0123456789':
                                    ux += 1
                                uv = QueueManager.parse_units(line[ux:])
                                if exp.config.data.get('Units', None) is not None:
                                    uv /= QueueManager.parse_units(exp.config.data['Units'])
                                val = float(line[:ux].replace(" ", ""))*uv
                            if float(int(val)) == val:
                                val = int(val)
                        exp.config.data[line[ind+4:-1]] = val
            rqueue.append(exp)
        self.experiment_queue.queue.extend(rqueue)
        return True

    @staticmethod
    def parse_units(s):
        """
        Determine the multiplier for a given unit string.
        :param s: Unit string.
        :return: Multiplier.
        """
        units = {"T": 1000000000000, "G": 1000000000, "M": 1000000, "K": 1000, "k": 1000,
                 "m": .001, "u": .000001, "n": .000000001, "p": .000000000001}
        if len(s) > 1:
            for u in units:
                if s.startswith(u):
                    return units[u]
        return 1
