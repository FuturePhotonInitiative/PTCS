import os

from src.GUI.Model.ExperimentModel import Experiment


class ExperimentsManager:
    def __init__(self, experiment_root, script_root):
        self.experiment_root = experiment_root
        self.script_root = script_root

        self.available_experiments = {}
        self.available_scripts = []
        for experiment_file in os.listdir(self.experiment_root):
            tmp = Experiment(os.path.join(self.experiment_root, experiment_file))
            self.available_experiments[str(tmp)] = tmp
        for script in script_root:
            self.available_scripts.append(script)
        self.cache_is_valid = True

    def get_available_experiments_names(self):
        if not self.cache_is_valid:
            self.rebuild_available_experiments()
        names = self.available_experiments.keys()
        names.sort()
        return names

    def rebuild_available_experiments(self):
        self.available_experiments = {}
        self.available_scripts = []
        for experiment_file in os.listdir(self.experiment_root):
            tmp = Experiment(os.path.join(self.experiment_root, experiment_file))
            self.available_experiments[str(tmp)] = tmp
        for script in self.script_root:
            self.available_scripts.append(script)
        self.cache_is_valid = True

    def get_experiment_from_name(self, name):
        """
        Get an Experiment object as described by the filename <name> in any of the experiment roots
        :param name:
            The filename of the experiment to search for
        :return:
            The experiment if it exists, None if it does not
        """
        if not self.cache_is_valid:
            self.rebuild_available_experiments()
        if name in self.available_experiments:
            return self.available_experiments[name].copy()
        return None

    def get_available_experiments(self):
        return self.available_experiments
