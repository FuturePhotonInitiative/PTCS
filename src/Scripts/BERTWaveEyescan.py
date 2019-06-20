import time

BITRATE = "\"INF10G\""
NO_OFFSET = 0
AMPLITUDE = .32
SCALE = 11.2
TIME_OFFSET = 0
BIT_VIEW_NUMBER = 2
DISPLAY_TYPE = "EYE"
SAMPLE_LIMIT = 10  # million
GATING_CYCLE = "REPeat"
PNG_FILE_LOCATION = r"C:\Users\mdn4993\Downloads\yolo.png"
TEST_HEADER = "BERTWave-> "


def main(data_map, experiment_result):
    print
    device = data_map["Devices"]["BERT Analyzer"]

    print(TEST_HEADER + "Running the test. This will take 10 seconds...")

    # PPG/ED
    device.run_change_bitrate(BITRATE)
    device.run_set_amplitude(AMPLITUDE)
    device.run_turn_on_error_addition()
    device.run_set_error_addition_repeat()
    device.run_set_error_addition_rate(7)

    device.run_set_gating_cycle_type(GATING_CYCLE)
    device.run_set_gating_cycle_period(0, 0, 0, 1)
    device.run_set_realtime_measurement_results_on()

    # Eye/Pulse Scope Graph Configuration
    device.run_set_scale(SCALE)
    device.run_set_amplitude_offset(NO_OFFSET)
    device.run_set_bit_view_number(BIT_VIEW_NUMBER)
    device.run_set_time_offset(TIME_OFFSET)

    # Eye/Pulse Scope Setup
    device.run_set_display_type(DISPLAY_TYPE)
    device.run_set_sample_limit(SAMPLE_LIMIT)

    # Eye/Pulse Scope Time
    device.run_turn_on_data_clock_tracking_rate()
    device.run_turn_on_data_clock_master_ppg1()

    # Turn things on
    device.run_turn_off_channel_b()
    device.run_turn_on_channel_a()
    device.run_turn_on_output()
    time.sleep(1)  # give things a little time to settle themselves

    device.run_run_all_measurements()

    time.sleep(10)

    device.run_stop_all_measurements()

    print(TEST_HEADER + "Test completed.")

    print(TEST_HEADER + "total error rate:\t\t" + str(device.run_query_error_count_total()))
    print(TEST_HEADER + "inserted error rate:\t\t" + str(device.run_query_error_count_inserted()))
    print(TEST_HEADER + "omitted error rate:\t\t" + str(device.run_query_error_count_omitted()))
    print(TEST_HEADER + "total error count:\t\t" + str(device.run_query_error_rate_total()))
    print(TEST_HEADER + "inserted error count:\t" + str(device.run_query_error_rate_inserted()))
    print(TEST_HEADER + "omitted error count:\t" + str(device.run_query_error_rate_omitted()))

    png_bytes = device.run_obtain_last_screenshot()
    fil = open(PNG_FILE_LOCATION, "wb")
    fil.write(png_bytes)
    fil.close()

    print(TEST_HEADER + "Eye diagram output path: " + PNG_FILE_LOCATION)

    print
