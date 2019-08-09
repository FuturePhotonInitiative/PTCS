import time
import os

TEST_PRINT_HEADER = "BERTWave-> "


def main(data_map, experiment_result):
    bertwave = data_map["Devices"]["BERT Analyzer"]

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
    bertwave.set_bitrate(bitrate)
    bertwave.set_amplitude(amplitude)
    bertwave.turn_on_error_addition()
    bertwave.set_error_addition_repeat()
    bertwave.set_error_addition_rate(7)

    bertwave.set_gating_cycle_type(gating_cycle_type)
    bertwave.set_gating_cycle_period(0, 0, 0, 1)
    bertwave.set_realtime_measurement_results_on()

    # Eye/Pulse Scope Graph Configuration
    bertwave.set_scale(graph_scale)
    bertwave.set_vertical_offset(graph_vertical_offset)
    bertwave.set_view_number_bits(graph_bit_view_number)
    bertwave.set_time_ps_offset(graph_time_offset)

    # Eye/Pulse Scope Setup
    bertwave.set_display_type(sampling_mode_display_type)
    bertwave.set_sample_limit(million_sample_limit)

    # Eye/Pulse Scope Time
    bertwave.turn_on_data_clock_tracking_rate()
    bertwave.turn_on_data_clock_master_ppg1()

    # Turn things on
    bertwave.set_channel_b_off()
    bertwave.set_channel_a_on()
    bertwave.turn_on_output()
    time.sleep(1)  # give things a little time to settle themselves

    bertwave.run_all_measurements()

    while bertwave.is_eye_sampling():
        pass

    bertwave.stop_all_measurements()    # the eye has already stopped, but this turns off the error detection
                                        # at the next measurement pass
    bertwave.turn_off_output()

    print(TEST_PRINT_HEADER + "Test completed.")
    print(TEST_PRINT_HEADER + "Saving Data...")

    ber = dict()

    ber["total error rate"] = bertwave.get_error_rate_total()
    ber["inserted error rate"] = bertwave.get_error_rate_inserted()
    ber["omitted error rate"] = bertwave.get_error_rate_omitted()
    ber["total error count"] = bertwave.get_error_count_total()
    ber["inserted error count"] = bertwave.get_error_count_inserted()
    ber["omitted error count"] = bertwave.get_error_count_omitted()

    experiment_result.add_csv_dict("error_rate_data", ber, ber.keys())

    bertwave.save_eye_screenshot_to_instrument()
    png_bytes = bertwave.get_last_screenshot_from_instrument()
    experiment_result.add_image_file(png_bytes, eyescan_image_name)

    print(TEST_PRINT_HEADER + "Eye diagram output path: " + os.path.join(experiment_result.experiment_results_directory, eyescan_image_name))

    print
