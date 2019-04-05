import datetime
import os

from src.GUI.Model import QueueResultModel
from src.GUI.Model.ExperimentModel import Experiment
from src.GUI.Model.ExperimentResultModel import ExperimentResultsModel
from src.GUI.Util.Functions import clean_name_for_file
from src.GUI.Util.GUI_CONSTANTS import QUEUE_FILE_TITLE


class ResultsManager:
    def __init__(self, results_root, results_config_root, results_config_manager):
        self.results_config_manager = results_config_manager
        self.results_root = results_root
        self.results_config_root = results_config_root
        self.queue_result_list = []
        self.experiment_result_dict = {}
        if not os.path.exists(results_config_root):
            os.mkdir(results_config_root)
        for config in os.listdir(results_config_root):
            if QUEUE_FILE_TITLE in config:
                self.queue_result_list.append(QueueResultModel.QueueResultsModel(results_config_root,queue_result_config=results_config_root + "/" + config))
            else:
                self.experiment_result_dict[config] = (ExperimentResultsModel(results_root,
                                                                              experiment_result_config=results_config_root + "/" + config))


    def get_list_of_queue_results(self):
        pass

    def get_list_of_experiment_result(self, key):
        return self.experiment_result_dict[key]

    def get_list_of_experiment_result_names(self):
        return self.experiment_result_dict.keys()

    def make_new_experiment_result(self, exeriment_config_location, queue_result):
        now = datetime.datetime.today()
        exp = Experiment(exeriment_config_location)

        name = exp.get_name() + str(now)
        name = clean_name_for_file(name)

        if not os.path.exists(self.results_root):
            os.mkdir(self.results_root)
        if not os.path.exists(self.results_root + "/" + name):
            os.mkdir(self.results_root + "/" + name)

        result = ExperimentResultsModel(self.results_root + "/" + name, exeriment_config_location)
        result.set_start(now)
        self.experiment_result_dict[name] = result
        queue_result.add_experiment_result(name)
        return [result, name]

    def make_new_queue_result(self):
        result = QueueResultModel.QueueResultsModel(self.results_config_root)
        self.queue_result_list.append(result)
        # print "STUFF HAPPENS HERE", len(self.queue_result_list)
        return result

    def save_experiment_results(self):
        for name in self.experiment_result_dict.keys():
            self.save_experiment_result(name, self.experiment_result_dict[name])

    def save_queue_results(self):
        for queue_result in self.queue_result_list:
            queue_result.save()

    def save_experiment_result(self, name, experiment_result):
        experiment_result.export_to_json(self.results_config_root + "/" + name + ".json")

    def get_queue_results(self):
        return self.queue_result_list