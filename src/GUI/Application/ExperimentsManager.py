import os

from src.GUI.Model.ExperimentModel import Experiment


class ExperimentsManager:
    def __init__(self, experiment_roots, script_root, results_config_manager):
        self.results_config_manager = results_config_manager
        self.experiment_roots = experiment_roots
        self.script_root = script_root

        self.available_experiments = {}
        self.available_scripts = []
        for root in experiment_roots:
            for experiment_file in os.listdir(root):
                tmp = Experiment(root + "/" + experiment_file)
                self.available_experiments[str(tmp)] = tmp
        for script in script_root:
            self.available_scripts.append(script)
        self.cache_is_valid = True

    def get_available_experiments_names(self):
        names = self.available_experiments.keys()
        names.sort()
        return names

    # def get_default_experiment_root(self):
    #     return self.system_config['Files']['Experiment_Roots'][0]
    #
    # def get_experiment_roots(self):
    #     return self.system_config['Files']['Experiment_Roots']
    #
    # def add_experiment_root(self, path_to_root):
    #     self.system_config['Files']['Experiment_Roots'].append(path_to_root)
    #     self.cache_is_valid = False

    def rebuild_available_experiments(self):
        self.available_experiments = {}
        self.available_scripts = []
        for root in self.experiment_roots:
            for experiment_file in os.listdir(root):
                tmp = Experiment(experiment_file)
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
