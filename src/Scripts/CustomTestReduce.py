
def main(data_map, experiment_result):
    red_func = data_map['Data'].get('Reduce Function', lambda vl, r: r)
    graph_title = data_map['Data'].get('Title', 'Collected Data')
    x_label = data_map['Data'].get('X Label', 'X Label')
    x_lower = data_map['Data'].get('X Lower', -10)
    x_upper = data_map['Data'].get('X Upper', 10)
    y_label = data_map['Data'].get('Y Label', 'Y Label')
    y_lower = data_map['Data'].get('Y Lower', -10)
    y_upper = data_map['Data'].get('Y Upper', 10)
    data_map['Data']['Reduce'] = {}

    samples = data_map['Data']['Collect']
    for val in samples.keys():
        data_map['Data']['Reduce'][val] = red_func(val, samples[val])

    reduced_data = []
    collected_data = []

    for val in samples.keys():
        new_list = [float(val), float(samples[val])]
        collected_data.append(new_list)
    reduced = data_map['Data']['Reduce']
    for val in reduced.keys():
        new_list = [float(val), float(reduced[val])]
        reduced_data.append(new_list)

    # Writing out collected data to csv
    experiment_result.add_csv("Collected_Data", collected_data, row_labels=[])
    # Writing out reduced data to csv
    experiment_result.add_csv("Reduced_Data", reduced_data, row_labels=[])

    x_axis = []
    y_axis = []
    for v in sorted(reduced_data):
        x_axis.append(float(v[0]))
        y_axis.append(float(v[1]))

    experiment_result.add_scatter_chart(graph_title.replace(" ", "_"), x_axis, y_axis,
                                        title=graph_title, x_label=x_label, y_label=y_label,
                                        x_lim=(x_lower, x_upper), y_lim=(y_lower, y_upper))
    return
