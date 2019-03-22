from threading import Thread
import os

from src import Prober
from src.GUI.Model.ExperimentModel import Experiment
from src.GUI.Model.ExperimentQueue import ExperimentQueue


class QueueManager:
    def __init__(self):
        self.runner = None
        self.experiment_queue = ExperimentQueue()
        pass

    def run_queue(self, toRun):
        if self.runner is not None:
            # TODO temp dir needs to be in config
            runner = QueueManager.QueueRunner(toRun, ".")
            runner.start()

    def queue_is_running(self):
        return (self.runner is not None) and (self.runner.isAlive())

    def join_on_running_queue(self):
        if self.runner is not None:
            self.runner.join()

    def get_experiment_status(self, experiment):
        pass

    class QueueRunner(Thread):
        def __init__(self, queue, tmp_dir):
            super.__init__(self)
            self.queue = queue
            self.tmp_dir = tmp_dir
            self.experiment_status = {}
            for i in range(len(queue)):
                self.experiment_status[queue.get_ith_experiment(i)] = -1
            self.current_experiment = None

        def run(self):
            self.queue.schedule_experiments()
            for i in range(len(self.queue)):
                self.current_experiment = self.queue.get_ith_experiment(i)
                self.experiment_status[self.current_experiment] = 0
                self.current_experiment.export_to_json(self.tmp_dir + "/tmp.json")
                Prober.main(self.tmp_dir + "/tmp.json")
                self.experiment_status[self.current_experiment] = 1
                os.remove(self.tmp_dir + "/tmp.json")

        def get_current_experiment(self):
            return self.current_experiment

        def get_run_status(self, experiment):
            return self.experiment_status[experiment]

    def get_experiment_names(self):
        self.experiment_queue.get_experiment_names()