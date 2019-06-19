# coding=UTF-8

from src.Instruments.IEEE_488_2 import IEEE_488_2
import time

# channel numbers
PPG_ED_CH1 = 1
SFP = 3
EYE_PULSE_SCOPE = 5
JITTER_ANALYSIS = 6
TRANSMISSION_ANALYSIS = 7

TERMINATION_CHARACTER = '\n'
ON = "ON"
OFF = "OFF"
REPEAT = "REP"
SINGLE = "SING"


# test if it is possible to do stuff while output and measure is on
# set vs query
# get vs change
class AnritsuMP2100A(IEEE_488_2):

    def __init__(self, device):
        IEEE_488_2.__init__(self, device, "Anritsu MP2100A BERT Analyzer")
        self.device.read_termination = TERMINATION_CHARACTER

    def run_run_all_measurements(self):
        self.device.write("*TRG")

    def run_stop_all_measurements(self):
        self.device.write(":SENSe:MEASure:ASTP")

    def run_get_device_option_codes(self):
        return self.device.query("*OPT?")

    def run_measurement_is_running(self):
        return self.device.query(":SENSe:MEASure:ASTate?") == 1

    def run_change_bitrate(self, bitrate):
        self.channel(PPG_ED_CH1)
        self.device.write(":SENSe:PARam:TRACking 1")
        self.device.write(":OUTPut:BITRate:STANdard " + bitrate)

    def run_query_bitrate(self):
        self.channel(PPG_ED_CH1)
        return self.device.query(":OUTPut:BITRate:STANdard?")

    def run_clear_display(self):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":DISPlay:WINDow:GRAPhics:CLEar")

    def run_query_amplitude(self):
        self.channel(PPG_ED_CH1)
        return self.device.query(":OUTPut:DATA:AMPLitude? DATA")

    def run_set_amplitude(self, amplitude):
        self.channel(PPG_ED_CH1)
        self.device.write(":OUTPut:DATA:AMPLitude DATA," + str(amplitude))

    def run_set_scale(self, scale):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":DISPlay:WINDow:Y:DIVision:CHA " + str(scale))

    def run_query_scale(self):
        self.channel(EYE_PULSE_SCOPE)
        return self.device.query(":DISPlay:WINDow:Y:DIVision:CHA?")

    def run_set_amplitude_offset(self, offset):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":DISPlay:WINDow:Y:OFFSets:CHA " + str(offset))

    def run_query_amplitude_offset(self):
        self.channel(EYE_PULSE_SCOPE)
        return self.device.query(":DISPlay:WINDow:Y:OFFSets:CHA?")

    # the file will not save unless the connection stays open a little
    def run_save_eye_screenshot_to_file(self):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":EYEPulse:PRINt:COPY")
        time.sleep(5)

    # the file will not save unless the connection stays open a little
    def run_save_full_screen_screenshot_to_file(self):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":SYSTem:PRINt:COPY")
        time.sleep(5)

    def run_turn_on_output(self):
        self.device.write(":SOURce:OUTPut:ASET " + ON)

    def run_turn_off_output(self):
        self.device.write(":SOURce:OUTPut:ASET " + OFF)

    def run_query_sample_run_state(self):
        self.channel(EYE_PULSE_SCOPE)
        return self.device.query(":SAMPling:STATus?")

    def run_run_sample(self):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":SAMPling:STATus RUN")

    def run_hold_sample(self):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":SAMPling:STATus HOLD")

    def run_set_bit_view_number(self, bits):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":DISPlay:WINDow:X:BITs " + str(bits))

    def run_get_bit_view_number(self):
        self.channel(EYE_PULSE_SCOPE)
        return self.device.query(":DISPlay:WINDow:X:BITs?")

    def run_get_time_offset(self):
        self.channel(EYE_PULSE_SCOPE)
        return self.device.query(":DISPlay:WINDow:X:OFFSets?")

    def run_set_time_offset(self, offset):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":DISPlay:WINDow:X:OFFSets " + str(offset))

    def run_set_display_type(self, display_type):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":DISPlay:MODE " + str(display_type))

    def run_get_display_type(self):
        self.channel(EYE_PULSE_SCOPE)
        return self.device.query(":DISPlay:MODE?")

    def run_get_sample_limit(self):
        self.channel(EYE_PULSE_SCOPE)
        return self.device.query(":ACCUmulation:LIMit?")

    def run_set_sample_limit(self, sample_limit):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":ACCUmulation:TYPe LIMited")
        self.device.write(":ACCUmulation:LIMit SAMPLe," + str(sample_limit))

    def run_turn_on_channel_a(self):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":INPut:CHA " + ON)

    def run_turn_off_channel_a(self):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":INPut:CHA " + OFF)

    def run_query_channel_a_on(self):
        self.channel(EYE_PULSE_SCOPE)
        return self.device.query(":INPut:CHA?") == ON

    def run_query_channel_a_off(self):
        return not self.run_query_channel_a_on()

    def run_turn_on_channel_b(self):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":INPut:CHB " + ON)

    def run_turn_off_channel_b(self):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":INPut:CHB " + OFF)

    def run_query_channel_b_on(self):
        self.channel(EYE_PULSE_SCOPE)
        return self.device.query(":INPut:CHB?") == ON

    def run_query_channel_b_off(self):
        return not self.run_query_channel_b_on()

    def run_turn_on_data_clock_tracking_rate(self):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":CONFigure:TRACking:DRATe " + ON)

    def run_query_data_clock_tracking_rate(self):
        self.channel(EYE_PULSE_SCOPE)
        return self.device.query(":CONFigure:TRACking:DRATe?") == "1"

    def run_turn_on_data_clock_master_ppg1(self):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":CONFigure:TRACking:DRATe:MASTer " + "0")

    def run_query_data_clock_master(self):
        self.channel(EYE_PULSE_SCOPE)
        return self.device.query(":CONFigure:TRACking:DRATe:MASTer?") == "0"

    def run_turn_on_error_addition(self):
        self.channel(PPG_ED_CH1)
        self.device.write(":SOURce:PATTern:EADDition:SET " + ON)

    def run_turn_off_error_addition(self):
        self.channel(PPG_ED_CH1)
        self.device.write(":SOURce:PATTern:EADDition:SET " + OFF)

    def run_query_error_addition_on(self):
        self.channel(PPG_ED_CH1)
        return self.device.query(":SOURce:PATTern:EADDition:SET?") == "1"

    def run_query_error_addition_variation_repeat(self):
        self.channel(PPG_ED_CH1)
        return self.device.query(":SOURce:PATTern:EADDition:VARiation?") == REPEAT

    def run_query_error_addition_variation_single(self):
        self.channel(PPG_ED_CH1)
        return self.device.query(":SOURce:PATTern:EADDition:VARiation?") == SINGLE

    def run_set_error_addition_repeat(self):
        self.channel(PPG_ED_CH1)
        self.device.write(":SOURce:PATTern:EADDition:VARiation " + REPEAT)

    def run_set_error_addition_single(self):
        self.channel(PPG_ED_CH1)
        self.device.write(":SOURce:PATTern:EADDition:VARiation " + SINGLE)

    def run_insert_error(self):
        self.channel(PPG_ED_CH1)
        self.device.write(":SOURce:PATTern:EADDition:SINGle")

    def run_query_error_addition_rate(self):
        self.channel(PPG_ED_CH1)
        return self.device.query(":SOURce:PATTern:EADDition:RATE?")

    def run_set_error_addition_rate(self, exponent):
        self.channel(PPG_ED_CH1)
        self.device.write(":SOURce:PATTern:EADDition:RATE " + "E_" + str(exponent) + ",1")

    def run_query_error_count_total(self):
        self.channel(PPG_ED_CH1)
        return int(self.device.query(":CALCulate:DATA:EALarm? " + '"CURRent:EC:TOTal"')[1:-1])

    def run_query_error_count_inserted(self):
        self.channel(PPG_ED_CH1)
        return int(self.device.query(":CALCulate:DATA:EALarm? " + '"CURRent:EC:INSertion"')[1:-1])

    def run_query_error_count_omitted(self):
        self.channel(PPG_ED_CH1)
        return int(self.device.query(":CALCulate:DATA:EALarm? " + '"CURRent:EC:OMIssion"')[1:-1])

    def run_query_error_rate_total(self):
        self.channel(PPG_ED_CH1)
        return float(self.device.query(":CALCulate:DATA:EALarm? " + '"CURRent:ER:TOTal"')[1:-1])

    def run_query_error_rate_inserted(self):
        self.channel(PPG_ED_CH1)
        return float(self.device.query(":CALCulate:DATA:EALarm? " + '"CURRent:ER:INSertion"')[1:-1])

    def run_query_error_rate_omitted(self):
        self.channel(PPG_ED_CH1)
        return float(self.device.query(":CALCulate:DATA:EALarm? " + '"CURRent:ER:OMIssion"')[1:-1])

    def run_set_gating_cycle_type(self, mode):
        self.channel(PPG_ED_CH1)
        self.device.write(":SENSe:MEASure:EALarm:MODE " + mode)

    def run_query_gating_cycle_type(self):
        self.channel(PPG_ED_CH1)
        return self.device.query(":SENSe:MEASure:EALarm:MODE?")

    def run_set_gating_cycle_period(self, days, hours, minutes, seconds):
        self.channel(PPG_ED_CH1)
        self.device.write(":SENSe:MEASure:EALarm:PERiod " + "{},{},{},{}".format(days, hours, minutes, seconds))

    def run_query_gating_cycle_period(self):
        self.channel(PPG_ED_CH1)
        return tuple([int(i) for i in self.device.query(":SENSe:MEASure:EALarm:PERiod?").split(",")])

    def run_query_realtime_measurement_results(self):
        self.channel(PPG_ED_CH1)
        return self.device.query(":DISPlay:RESult:EALarm:MODE?") == "1"

    def run_set_realtime_measurement_results_off(self):
        self.channel(PPG_ED_CH1)
        self.device.write(":DISPlay:RESult:EALarm:MODE " + OFF)

    def run_set_realtime_measurement_results_on(self):
        self.channel(PPG_ED_CH1)
        self.device.write(":DISPlay:RESult:EALarm:MODE " + ON)

    def run_obtain_last_screenshot(self):
        """
        :return: the byte string of the screenshot file
        """
        self.device.read_termination = None
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":SYSTem:DISPlay:DATA?")
        self.device.read_bytes(1)  # burn the hash character

        size_of_bytes_size = int(self.device.read_bytes(1))
        bytes_size = int(self.device.read_bytes(size_of_bytes_size))
        photo_bytes = self.device.read_bytes(bytes_size)
        last_character = self.device.read_bytes(1)

        self.device.read_termination = TERMINATION_CHARACTER
        if last_character == TERMINATION_CHARACTER:
            # it all went well
            return photo_bytes
        else:
            raise Exception("Something done goofed when obtaining the screenshot from the instrument")

    def channel(self, module_number):
        """
        For some reason, doing anything automated to the EYE/Pulse Scope screen
        needs to have the module specified or it wont work. Doing things to other modules
        after setting that module does not work either, so we are just going to set the channel before every command
        :param module_number: the module to let the instrument know that said module has a query coming its way
        """
        self.device.write(":MODule:ID " + str(module_number))
