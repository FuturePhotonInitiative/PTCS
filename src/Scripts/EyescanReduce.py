import re

def main(data_map, experiment_result):
    """
    This stage reduces the data provided by the eyescan. No reduction needed for this test
    :param data_map: The dictionary to store data between tasks
    :param experiment_result: ExperimentResultsModel object
    :return: None
    """
    # parse date that was provided
    data = data_map['Data']['Collect']
    data_map['Data']['Reduce'] = []
    data_match = re.compile(r'^(?P<data>[0-9,]+);')
    for d in data:
        match = data_match.match(d)
        if match is not None:
            data_map['Data']['Reduce'].append(match.group('data').split(","))
    return
