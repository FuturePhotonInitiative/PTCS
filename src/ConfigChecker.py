# This file is intended to check the config files
# Save this for my last week, document it
# Check expected fields in config file
# Function should return True/False for Pass/Fail


def check_config_file(config):
	"""
	Checks the config file to ensure that information is properly input in json configuration
	:param config: json dictionary containing all information
	:return: True/False: depending on pass or fail of configuration check
	"""
	if config:
		return True
	return False
