
class Experiment:

	def __init__(self):
		self.config = {}
		self.dependencies = []
		pass

	def read_from_json(self, json_file):
		"""
		Reads the configuration of the experiment from the specified json file
		:param json_file:
		:return:
		"""
		pass

	def write_to_json(self, file_name):
		"""
		Writes the configuration of the experiment to the specified file path
		:param file_name:
		:return:
		"""
		pass

	def run_experiment(self):
		"""
		Runs the experiment via Prober.py
		:return:
		"""
		pass

	# Need to store JSON data
	# Need to store Dependencies
	# Need to have "Run Experiment" methods
	# Need read from JSON method
	# Need write to JSON method
