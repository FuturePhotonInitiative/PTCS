from ExperimentModel import Experiment


class TclExperiment(Experiment):
    def __init__(self, config_file, dependencies=None, priority=1, tcl_location=None):
        self.tcl_file = tcl_location
        super.__init__(config_file, dependencies, priority)