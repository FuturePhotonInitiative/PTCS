import time
import os

BITRATE = "\"INF10G\""
NO_OFFSET = 0
AMPLITUDE = .32
SCALE = 11.2
TIME_OFFSET = 0
BIT_VIEW_NUMBER = 2
DISPLAY_TYPE = "EYE"
SAMPLE_LIMIT = 10  # million
GATING_CYCLE = "REPeat"
PNG_FILE_LOCATION = "yolo.png"
TEST_HEADER = "BERTWave-> "


def main(data_map, experiment_result):
    print
    device = data_map["Devices"]["BERT Analyzer"]

    print(TEST_HEADER + "Running the test. This will take 10 seconds...")

    # PPG/ED
    device.set_bitrate(BITRATE)
    device.set_amplitude(AMPLITUDE)
    device.turn_on_error_addition()
    device.set_error_addition_repeat()
    device.set_error_addition_rate(7)

    device.set_gating_cycle_type(GATING_CYCLE)
    device.set_gating_cycle_period(0, 0, 0, 1)
    device.set_realtime_measurement_results_on()

    # Eye/Pulse Scope Graph Configuration
    device.set_scale(SCALE)
    device.set_vertical_offset(NO_OFFSET)
    device.set_view_number_bits(BIT_VIEW_NUMBER)
    device.set_time_ps_offset(TIME_OFFSET)

    # Eye/Pulse Scope Setup
    device.set_display_type(DISPLAY_TYPE)
    device.set_sample_limit(SAMPLE_LIMIT)

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

    print(TEST_HEADER + "Test completed.")

    print(TEST_HEADER + "total error rate:\t\t" + str(device.get_error_count_total()))
    print(TEST_HEADER + "inserted error rate:\t\t" + str(device.get_error_count_inserted()))
    print(TEST_HEADER + "omitted error rate:\t\t" + str(device.get_error_count_omitted()))
    print(TEST_HEADER + "total error count:\t\t" + str(device.get_error_rate_total()))
    print(TEST_HEADER + "inserted error count:\t" + str(device.get_error_rate_inserted()))
    print(TEST_HEADER + "omitted error count:\t" + str(device.get_error_rate_omitted()))

    png_bytes = device.get_last_screenshot()
    experiment_result.add_image_file(png_bytes, PNG_FILE_LOCATION)

    print(TEST_HEADER + "Eye diagram output path: " + os.path.join(experiment_result.experiment_results_directory, PNG_FILE_LOCATION))

    print
