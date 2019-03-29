import os

from src.GUI.Model import QueueResultModel


class ResultsManager:
    def __init__(self, results_root, results_config_root):
        self.results_root = results_root
        self.results_config_root = results_config_root
        self.queue_result_list = []
        for config in os.listdir(results_config_root):
            self.queue_result_list.append(QueueResultModel.QueueResultsModel())


    def get_list_of_queue_results(self):
        pass