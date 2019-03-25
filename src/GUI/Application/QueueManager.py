import os

from src.GUI.Application.QueueRunner import QueueRunner
from src.GUI.Model.ExperimentQueue import ExperimentQueue


class QueueManager:
    # TODO temp dir needs to be in config
    def __init__(self, working_directory):
        self.working_directory = working_directory + "/temp"
        if not os.path.exists(self.working_directory):
            os.makedirs(self.working_directory)
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
        if self.runner is None:
            runner = QueueRunner(to_run, self.working_directory)
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
