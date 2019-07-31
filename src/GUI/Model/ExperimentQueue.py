class ExperimentQueue:

    def __init__(self):
        """
        :param system_config:
            A list of filenames which hold the application configuration, they are opened, parsed,
            and stored in the order they are provided in in the list.
        """
        self.queue = []
        # self.system_config_files = system_config
        # self.system_config = {}
        # for sysfile in self.system_config_files:
        #     with open(sysfile) as f:
        #         self.system_config[os.path.basename(sysfile).replace('.json', "")] = json.load(f)
        #
        # self.experiment_cache = {}
        # self.cache_is_valid = False
        # self.rebuild_experiment_cache()

        pass

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

    def move_ith_experiment_up(self, i):
        """
        Safely moves the experiment currently in the ith position to the i-1th position.
        (0 i the highest position)
        :param i:
            The position in the queue of the experiment to sift up
        :return:
            None
        """
        if i > 0:
            self.queue[i], self.queue[i-1] = self.queue[i-1], self.queue[i]

    def move_ith_experiment_down(self, i):
        """
        Safely moves the experiment currently in the ith position to the i+1th position.
        (0 is the highest position)
        :param i:
            The position in the queue of the experiment to sift down
        :return:
            None
        """
        if i < len(self.queue)-1:
            self.queue[i], self.queue[i+1] = self.queue[i+1], self.queue[i]

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
