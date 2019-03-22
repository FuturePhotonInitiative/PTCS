import os

from src.GUI.Model.ExperimentModel import Experiment


class ExperimentsManager:
    def __init__(self, experiment_roots, script_root):
        self.available_experiments = {}
        self.available_scripts = []
        for root in experiment_roots:
            for experiment_file in os.listdir(root):
                tmp = Experiment(experiment_file)
                self.available_experiments[str(tmp)] = tmp
        for script in script_root:
            self.available_scripts.append(script)

    def get_available_experiments_names(self):
        return self.available_experiments.keys()
