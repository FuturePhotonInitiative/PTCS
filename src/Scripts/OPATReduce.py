def filter_results(test_lst):
    """
    gets rid of entries that are more than a tenth away from the last group of values
    :param test_lst: the list to filter
    :return: a copy of the list but modified in the said way
    """
    return_lst = []
    for i in range(1, len(test_lst)):
        prev = test_lst[i - 1]
        curr = test_lst[i]
        tenth = curr / 100
        if not(curr - tenth < prev < curr + tenth):
            return_lst.append(0)
        else:
            return_lst.append(prev)
    return_lst.append(test_lst[-1])

    flag = False
    for i in range(0, len(return_lst)):
        i = len(return_lst) - i - 1
        if not flag:
            if return_lst[i] == 0:
                flag = True
        else:
            return_lst[i] = 0
    return return_lst


def main(data_map, experiment_result):
    """
    filters both lists to get rid of invalid measurement points
    """
    laser_power1 = str(data_map["Data"]["Initial"]["laser_power1"])
    laser_power2 = str(data_map["Data"]["Initial"]["laser_power2"])
    test1 = data_map["Data"]["Collect"][laser_power1]
    test2 = data_map["Data"]["Collect"][laser_power2]

    data_map["Data"]["Reduce"] = {
        laser_power1: filter_results([float(i) for i in test1]),
        laser_power2: filter_results([float(i) for i in test2])
    }
