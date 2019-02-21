import json


class SPAEModel:

    def __init__(self, system_config):
        """
        Create a new SPAEModel for the SPAE GUI
        :param system_config:
            A list of filenames which hold the application configuration, they are opened, parsed,
            and stored in the order they are provided in in the list.
        """
        self.queue = []
        self.system_config_files = system_config
        self.system_config = {}
        for sysfile in self.system_config_files:
            with open(sysfile) as f:
                self.system_config[sysfile] = json.load(f)
        pass

    def add_to_queue(self, experiment):
        """
        Adds an experiment to the queue to run
        :param experiment:
            An Experiment object
        :return:
            None
        """
        self.queue.append(experiment)

    def get_next_experiment(self):
        """
        :return:
            The next experiment in the queue and remove it from the queue
        """
        return self.queue.pop(0)

    def schedule_experiments(self):
        """
        Re-order the experiment queue according to the dependencies and priorities of the Experiments in the queue.
        :return:
            None
        """
        # Method stub to be implemented if and when we decide to parallelize experiments
        pass
