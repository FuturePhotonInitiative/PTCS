BITRATE = "\"INF10G\""
NO_OFFSET = 0
AMPLITUDE = .32
SCALE = 11.2
TIME_OFFSET = 0
BIT_VIEW_NUMBER = 2
DISPLAY_TYPE = "EYE"
SAMPLE_LIMIT = 10  # million
# EYESCAN_FILE_NAME = "Eyescan-to-be-exported"
# EYESCAN_FILE_DIRECTORY = r"C:\Program Files\Anritsu\MP2100A\MX210000A\UserData\Screen Copy"
# EYESCAN_FILE_FORMAT = "PNG"


def main(data_map, experiment_result):
    print
    device = data_map["Devices"]["BERT Analyzer"]

    # device.run_change_bitrate(BITRATE)
    # device.run_set_scale(SCALE)
    # device.run_amplitude_offset(NO_OFFSET)
    # device.run_set_bit_view_number(BIT_VIEW_NUMBER)
    # device.run_set_time_offset(TIME_OFFSET)
    # device.run_set_display_type(DISPLAY_TYPE)
    # device.run_set_sample_limit(SAMPLE_LIMIT)
    # device.run_set_amplitude(AMPLITUDE)

    # device.run_turn_on_output()
    # device.run_run_sample()

    device.run_save_eye_screenshot_to_file()



    print
