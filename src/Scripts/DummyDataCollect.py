import random
import time


def main(data_map):
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

        data_map['Data']['Collect'][str(i)] = [random.randint(0, 100), random.randint(0, 100), random.randint(0, 100),
                                               random.randint(0, 100), random.randint(0, 100), random.randint(0, 100),
                                               random.randint(0, 100), random.randint(0, 100), random.randint(0, 100),
                                               random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)
                                               ]

    print "Collection took: " + str(time.time() - start_time) + " seconds"
    # sys.exit("Done")
    return
