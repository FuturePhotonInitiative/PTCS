class ExperimentQueue:

    def __init__(self):
        self.queue = []

    def __len__(self):
        return len(self.queue)

    def add_to_queue(self, experiment):
        """
        Adds an experiment to the queue to run
        :param experiment:
            An Experiment object
        :return:
            None
        """
        self.queue.append(experiment)

    def remove_from_queue(self, experiment):
        """
        Removes an exact experiment object from the queue
        :param experiment:
            The experiment to remove
        :return:
            None
        """
        self.queue.remove(experiment)

    def clear_queue(self):
        """
        Clears the queue
        :return:
            None
        """
        self.queue = []

    def get_next_experiment(self):
        """
        :return:
            The next experiment in the queue and remove it from the queue
        """
        return self.queue.pop(0)

    def get_ith_experiment(self, i):
        """
        :param i:
            The 0-based position of the experiment in the list
        :return:
            The ith experiment (Aren't I good at naming methods?)
        """
        return self.queue[i]

    def schedule_experiments(self):
        """
        Re-order the experiment queue according to the dependencies and priorities of the Experiments in the queue.
        :return:
            None
        """
        # Method stub to be implemented if and when we decide to parallelize experiments
        pass

    def get_experiment_names(self):
        name_list = []
        for experiment in self.queue:
            name_list.append(experiment.get_name())
        return name_list
