from threading import Thread
import os

from src import Prober
from src.GUI.Model.ExperimentModel import Experiment
from src.GUI.Model.ExperimentQueue import ExperimentQueue


class QueueManager:
    # TODO temp dir needs to be in config
    def __init__(self, tmp_dir):
        self.tmp_dir = tmp_dir
        self.runner = None
        self.experiment_queue = ExperimentQueue()

    def run_queue(self, to_run):
        """
            Starts the thread that runs the queue.
        :param to_run:
            The queue to be run
        :return:
            None, immediately
        """
        if self.runner is not None:
            runner = QueueManager.QueueRunner(to_run, self.tmp_dir)
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

    class QueueRunner(Thread):
        """
        Thread class to run a provided queue
        """
        def __init__(self, queue, tmp_dir):
            """
            Create a new QueueRunner that will run the provided queue using the provided temporary directory
            :param queue:
                The queue to run with Prober
            :param tmp_dir:
                The directory to store the temporary json file for the experiment on which we will call Prober
            """
            Thread.__init__(self)
            self.queue = queue
            self.tmp_dir = tmp_dir
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
            # TODO catch any exceptions run by prober and try to continue, but only if a flag in the __init__ has been
            # set
            self.queue.schedule_experiments()
            for i in range(len(self.queue)):
                self.current_experiment = self.queue.get_ith_experiment(i)
                self.experiment_status[self.current_experiment] = 0
                # The file to store the json to call prober on to run the experiment
                tmp_file_name = self.tmp_dir + "/tmp" + self.current_experiment.get_name() + ".json"
                self.current_experiment.export_to_json(tmp_file_name)
                Prober.main(tmp_file_name)
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

    def get_experiment_names(self):
        self.experiment_queue.get_experiment_names()