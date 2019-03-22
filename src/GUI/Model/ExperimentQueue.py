import json
import os

from src.GUI.Model.ExperimentModel import Experiment


class ExperimentQueue:

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
                self.system_config[os.path.basename(sysfile).replace('.json', "")] = json.load(f)

        self.experiment_cache = {}
        self.cache_is_valid = False
        self.rebuild_experiment_cache()

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

    def get_default_experiment_root(self):
        return self.system_config['Files']['Experiment_Roots'][0]

    def get_experiment_roots(self):
        return self.system_config['Files']['Experiment_Roots']

    def add_experiment_root(self, path_to_root):
        self.system_config['Files']['Experiment_Roots'].append(path_to_root)
        self.cache_is_valid = False

    def schedule_experiments(self):
        """
        Re-order the experiment queue according to the dependencies and priorities of the Experiments in the queue.
        :return:
            None
        """
        # Method stub to be implemented if and when we decide to parallelize experiments
        pass

    def get_experiment_from_name(self, name):
        """
        Get an Experiment object as described by the filename <name> in any of the experiment roots
        :param name:
            The filename of the experiment to search for
        :return:
            The experiment if it exists, None if it does not
        """
        if not self.cache_is_valid:
            self.rebuild_experiment_cache()
        if name in self.experiment_cache:
            return Experiment(self.experiment_cache[name])
        return None

    def rebuild_experiment_cache(self):
        self.experiment_cache = {}
        # TODO recursively search
        for exp_dir in self.system_config['Files']['Experiment_Roots']:
            for exp_file in os.listdir(exp_dir):
                self.experiment_cache[os.path.basename(exp_file)] = exp_dir + "/" + os.path.basename(exp_file)
        self.cache_is_valid = True

    def get_experiment_names(self):
        name_list = []
        for experiment in self.queue:
            name_list.append(experiment.get_name())
        return name_list

if __name__ == '__main__':
    model = ExperimentQueue(['../../System/Devices.json'])
    # Add five experiments and make sure they are added to the queue in order
    print "Testing experiment add order"
    model.add_to_queue(Experiment('../../Configs/Dummy_Test1.json'))
    model.add_to_queue(Experiment('../../Configs/Dummy_Test2.json'))
    model.add_to_queue(Experiment('../../Configs/Dummy_Test3.json'))
    model.add_to_queue(Experiment('../../Configs/Dummy_Test4.json'))
    model.add_to_queue(Experiment('../../Configs/Dummy_Test5.json'))
    print("Experiment 1: " + model.queue[0].get_name())
    print("Experiment 2: " + model.queue[1].get_name())
    print("Experiment 3: " + model.queue[2].get_name())
    print("Experiment 4: " + model.queue[3].get_name())
    print("Experiment 5: " + model.queue[4].get_name())
    print ""

    print "Testing experiment reorder (sift up)"
    model.move_ith_experiment_up(4)
    model.move_ith_experiment_up(3)
    model.move_ith_experiment_up(2)
    model.move_ith_experiment_up(1)
    model.move_ith_experiment_up(0)
    model.move_ith_experiment_up(-1)
    print "Experiment 5: " + model.queue[0].get_name()
    print "Experiment 1: " + model.queue[1].get_name()
    print "Experiment 2: " + model.queue[2].get_name()
    print "Experiment 3: " + model.queue[3].get_name()
    print "Experiment 4: " + model.queue[4].get_name()
    print ""

    print "Testing experiment reorder (sift down)"
    model.move_ith_experiment_down(0)
    model.move_ith_experiment_down(1)
    model.move_ith_experiment_down(2)
    model.move_ith_experiment_down(3)
    model.move_ith_experiment_down(4)
    model.move_ith_experiment_down(5)
    print("Experiment 1: " + model.queue[0].get_name())
    print("Experiment 2: " + model.queue[1].get_name())
    print("Experiment 3: " + model.queue[2].get_name())
    print("Experiment 4: " + model.queue[3].get_name())
    print("Experiment 5: " + model.queue[4].get_name())
    print ''

    print "Testing experiment remove order"
    print("Experiment 1: " + model.get_next_experiment().get_name())
    print("Experiment 2: " + model.get_next_experiment().get_name())
    print("Experiment 3: " + model.get_next_experiment().get_name())
    print("Experiment 4: " + model.get_next_experiment().get_name())
    print("Experiment 5: " + model.get_next_experiment().get_name())
