import math
import random
import time


def main(data_map, experiment_result):
    """
	This stage varies an applied voltage to a logic analyzer and collects the resulting samples
	:param data_map: The dictionary to store data between tasks
	:return: None
	"""

    data_map['Data']['Collect'] = {}
    levels = float(data_map['Data']['Initial']["Levels"])

    start_time = time.time()
    for i in range(int(levels)):
        # time.sleep(0.25)
        if i % 1 == 0:
            print "Applying " + str(i) + " fake volts"
        exp_base = 1.2 ** i
        data_map['Data']['Collect'][str(i)] = [exp_base - exp_base / 2.0 + exp_base*random.random(),
                                               exp_base - exp_base / 2.0 + exp_base*random.random(),
                                               exp_base - exp_base / 2.0 + exp_base*random.random(),
                                               exp_base - exp_base / 2.0 + exp_base*random.random(),
                                               exp_base - exp_base / 2.0 + exp_base*random.random(),
                                               exp_base - exp_base / 2.0 + exp_base*random.random(),
                                               exp_base - exp_base / 2.0 + exp_base*random.random(),
                                               exp_base - exp_base / 2.0 + exp_base*random.random(),
                                               exp_base - exp_base / 2.0 + exp_base*random.random(),
                                               exp_base - exp_base / 2.0 + exp_base*random.random(),
                                               exp_base - exp_base / 2.0 + exp_base*random.random(),
                                               exp_base - exp_base / 2.0 + exp_base*random.random(),
                                               ]

    print "Collection took: " + str(time.time() - start_time) + " seconds"
    # sys.exit("Done")
    return
