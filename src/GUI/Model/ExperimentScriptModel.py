class ExperimentScript:
    def __init__(self, script_dict):
        self.type = script_dict['Type']
        self.source = script_dict['Source']
        self.order = script_dict['Order']
