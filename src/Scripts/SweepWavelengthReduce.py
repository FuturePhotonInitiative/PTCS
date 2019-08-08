def filter_results(test_lst):
    """
    makes zero all of the entries that are more than a tenth away from the last group of values. This is useful to
    get rid of the noisy data at the beginning of the test
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

    lst_start = 0
    while return_lst[lst_start] == 0:
        lst_start += 1

    return return_lst[lst_start:]


def main(data_map, results):
    sweep_data = data_map["Data"]["Collect"]["sweep"]
    data_map["Data"]["Reduce"] = filter_results([float(i) for i in sweep_data])
