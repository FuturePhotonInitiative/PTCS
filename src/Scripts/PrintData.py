def main(data_map, experiment_result):
    print
    print(data_map["Data"]["Initial"])
    print(data_map["Devices"])
    yolo = data_map["Devices"]["BERT Analyzer"]
    print(yolo.run_identify())
