import time
import os

TEST_PRINT_HEADER = "BERTWave-> "


def main(data_map, experiment_result):
    device = data_map["Devices"]["BERT Analyzer"]
    bitrate = data_map["Config"]["data"]["bitrate"]
    graph_vertical_offset = data_map["Config"]["data"]["graph_vertical_offset"]
    amplitude = data_map["Config"]["data"]["amplitude"]
    graph_scale = data_map["Config"]["data"]["graph_scale"]
    graph_time_offset = data_map["Config"]["data"]["graph_time_offset"]
    graph_bit_view_number = data_map["Config"]["data"]["graph_bit_view_number"]
    sampling_mode_display_type = data_map["Config"]["data"]["sampling_mode_display_type"]
    million_sample_limit = data_map["Config"]["data"]["million_sample_limit"]
    gating_cycle_type = data_map["Config"]["data"]["gating_cycle_type"]
    eyescan_image_name = data_map["Config"]["data"]["eyescan_image_name"]

    print(TEST_PRINT_HEADER + "Running the test. This will take 10 seconds...")

    # PPG/ED
    device.set_bitrate(bitrate)
    device.set_amplitude(amplitude)
    device.turn_on_error_addition()
    device.set_error_addition_repeat()
    device.set_error_addition_rate(7)

    device.set_gating_cycle_type(gating_cycle_type)
    device.set_gating_cycle_period(0, 0, 0, 1)
    device.set_realtime_measurement_results_on()

    # Eye/Pulse Scope Graph Configuration
    device.set_scale(graph_scale)
    device.set_vertical_offset(graph_vertical_offset)
    device.set_view_number_bits(graph_bit_view_number)
    device.set_time_ps_offset(graph_time_offset)

    # Eye/Pulse Scope Setup
    device.set_display_type(sampling_mode_display_type)
    device.set_sample_limit(million_sample_limit)

    # Eye/Pulse Scope Time
    device.turn_on_data_clock_tracking_rate()
    device.turn_on_data_clock_master_ppg1()

    # Turn things on
    device.set_channel_b_off()
    device.set_channel_a_on()
    device.turn_on_output()
    time.sleep(1)  # give things a little time to settle themselves

    device.run_all_measurements()

    time.sleep(10)

    device.stop_all_measurements()

    print(TEST_PRINT_HEADER + "Test completed.")

    print(TEST_PRINT_HEADER + "total error rate:\t\t" + str(device.get_error_count_total()))
    print(TEST_PRINT_HEADER + "inserted error rate:\t\t" + str(device.get_error_count_inserted()))
    print(TEST_PRINT_HEADER + "omitted error rate:\t\t" + str(device.get_error_count_omitted()))
    print(TEST_PRINT_HEADER + "total error count:\t\t" + str(device.get_error_rate_total()))
    print(TEST_PRINT_HEADER + "inserted error count:\t" + str(device.get_error_rate_inserted()))
    print(TEST_PRINT_HEADER + "omitted error count:\t" + str(device.get_error_rate_omitted()))

    png_bytes = device.get_last_screenshot()
    experiment_result.add_image_file(png_bytes, eyescan_image_name)

    print(TEST_PRINT_HEADER + "Eye diagram output path: " + os.path.join(experiment_result.experiment_results_directory, eyescan_image_name))

    print
