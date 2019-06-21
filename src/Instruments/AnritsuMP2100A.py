from src.Instruments.IEEE_488_2 import IEEE_488_2
import time
import re
import inspect

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


class AnritsuMP2100A(IEEE_488_2):

    def __init__(self, device):
        IEEE_488_2.__init__(self, device, "Anritsu MP2100A BERT Analyzer")
        self.device.read_termination = TERMINATION_CHARACTER

    def run_all_measurements(self):
        self.device.write("*TRG")

    def stop_all_measurements(self):
        self.device.write(":SENSe:MEASure:ASTP")

    def get_device_option_codes(self):
        return self.device.query("*OPT?")

    def measurement_is_running(self):
        return self.device.query(":SENSe:MEASure:ASTate?") == 1

    def set_bitrate(self, bitrate):
        self._channel(PPG_ED_CH1)
        self.device.write(":SENSe:PARam:TRACking 1")
        self.device.write(":OUTPut:BITRate:STANdard " + bitrate)

    def get_bitrate(self):
        self._channel(PPG_ED_CH1)
        return self.device.query(":OUTPut:BITRate:STANdard?")

    def clear_display(self):
        self._channel(EYE_PULSE_SCOPE)
        self.device.write(":DISPlay:WINDow:GRAPhics:CLEar")

    def get_amplitude(self):
        self._channel(PPG_ED_CH1)
        return self.device.query(":OUTPut:DATA:AMPLitude? DATA")

    def set_amplitude(self, amplitude):
        self._channel(PPG_ED_CH1)
        self.device.write(":OUTPut:DATA:AMPLitude DATA," + str(amplitude))

    def set_scale(self, scale):
        self._channel(EYE_PULSE_SCOPE)
        self.device.write(":DISPlay:WINDow:Y:DIVision:CHA " + str(scale))

    def get_scale(self):
        self._channel(EYE_PULSE_SCOPE)
        return self.device.query(":DISPlay:WINDow:Y:DIVision:CHA?")

    def set_amplitude_offset(self, offset):
        self._channel(EYE_PULSE_SCOPE)
        self.device.write(":DISPlay:WINDow:Y:OFFSets:CHA " + str(offset))

    def get_amplitude_offset(self):
        self._channel(EYE_PULSE_SCOPE)
        return self.device.query(":DISPlay:WINDow:Y:OFFSets:CHA?")

    # the file will not save unless the connection stays open a little
    def save_eye_screenshot_to_file(self):
        self._channel(EYE_PULSE_SCOPE)
        self.device.write(":EYEPulse:PRINt:COPY")
        time.sleep(5)

    # the file will not save unless the connection stays open a little
    def save_full_screen_screenshot_to_file(self):
        self._channel(EYE_PULSE_SCOPE)
        self.device.write(":SYSTem:PRINt:COPY")
        time.sleep(5)

    def turn_on_output(self):
        self.device.write(":SOURce:OUTPut:ASET " + ON)

    def turn_off_output(self):
        self.device.write(":SOURce:OUTPut:ASET " + OFF)

    def get_sample_run_state(self):
        self._channel(EYE_PULSE_SCOPE)
        return self.device.query(":SAMPling:STATus?")

    def run_sample(self):
        self._channel(EYE_PULSE_SCOPE)
        self.device.write(":SAMPling:STATus RUN")

    def hold_sample(self):
        self._channel(EYE_PULSE_SCOPE)
        self.device.write(":SAMPling:STATus HOLD")

    def set_bit_view_number(self, bits):
        self._channel(EYE_PULSE_SCOPE)
        self.device.write(":DISPlay:WINDow:X:BITs " + str(bits))

    def get_bit_view_number(self):
        self._channel(EYE_PULSE_SCOPE)
        return self.device.query(":DISPlay:WINDow:X:BITs?")

    def get_time_offset(self):
        self._channel(EYE_PULSE_SCOPE)
        return self.device.query(":DISPlay:WINDow:X:OFFSets?")

    def set_time_offset(self, offset):
        self._channel(EYE_PULSE_SCOPE)
        self.device.write(":DISPlay:WINDow:X:OFFSets " + str(offset))

    def set_display_type(self, display_type):
        self._channel(EYE_PULSE_SCOPE)
        self.device.write(":DISPlay:MODE " + str(display_type))

    def get_display_type(self):
        self._channel(EYE_PULSE_SCOPE)
        return self.device.query(":DISPlay:MODE?")

    def get_sample_limit(self):
        self._channel(EYE_PULSE_SCOPE)
        return self.device.query(":ACCUmulation:LIMit?")

    def set_sample_limit(self, sample_limit):
        self._channel(EYE_PULSE_SCOPE)
        self.device.write(":ACCUmulation:TYPe LIMited")
        self.device.write(":ACCUmulation:LIMit SAMPLe," + str(sample_limit))

    def set_channel_a_on(self):
        self._channel(EYE_PULSE_SCOPE)
        self.device.write(":INPut:CHA " + ON)

    def set_channel_a_off(self):
        self._channel(EYE_PULSE_SCOPE)
        self.device.write(":INPut:CHA " + OFF)

    def get_channel_a_on(self):
        self._channel(EYE_PULSE_SCOPE)
        return self.device.query(":INPut:CHA?") == ON

    def get_channel_a_off(self):
        return not self.run_get_channel_a_on()

    def set_channel_b_on(self):
        self._channel(EYE_PULSE_SCOPE)
        self.device.write(":INPut:CHB " + ON)

    def set_channel_b_off(self):
        self._channel(EYE_PULSE_SCOPE)
        self.device.write(":INPut:CHB " + OFF)

    def get_channel_b_on(self):
        self._channel(EYE_PULSE_SCOPE)
        return self.device.query(":INPut:CHB?") == ON

    def get_channel_b_off(self):
        return not self.run_get_channel_b_on()

    def turn_on_data_clock_tracking_rate(self):
        self._channel(EYE_PULSE_SCOPE)
        self.device.write(":CONFigure:TRACking:DRATe " + ON)

    def get_data_clock_tracking_rate(self):
        self._channel(EYE_PULSE_SCOPE)
        return self.device.query(":CONFigure:TRACking:DRATe?") == "1"

    def turn_on_data_clock_master_ppg1(self):
        self._channel(EYE_PULSE_SCOPE)
        self.device.write(":CONFigure:TRACking:DRATe:MASTer " + "0")

    def get_data_clock_master(self):
        self._channel(EYE_PULSE_SCOPE)
        return self.device.query(":CONFigure:TRACking:DRATe:MASTer?") == "0"

    def turn_on_error_addition(self):
        self._channel(PPG_ED_CH1)
        self.device.write(":SOURce:PATTern:EADDition:SET " + ON)

    def turn_off_error_addition(self):
        self._channel(PPG_ED_CH1)
        self.device.write(":SOURce:PATTern:EADDition:SET " + OFF)

    def get_error_addition_on(self):
        self._channel(PPG_ED_CH1)
        return self.device.query(":SOURce:PATTern:EADDition:SET?") == "1"

    def get_error_addition_variation_repeat(self):
        self._channel(PPG_ED_CH1)
        return self.device.query(":SOURce:PATTern:EADDition:VARiation?") == REPEAT

    def get_error_addition_variation_single(self):
        self._channel(PPG_ED_CH1)
        return self.device.query(":SOURce:PATTern:EADDition:VARiation?") == SINGLE

    def set_error_addition_repeat(self):
        self._channel(PPG_ED_CH1)
        self.device.write(":SOURce:PATTern:EADDition:VARiation " + REPEAT)

    def set_error_addition_single(self):
        self._channel(PPG_ED_CH1)
        self.device.write(":SOURce:PATTern:EADDition:VARiation " + SINGLE)

    def insert_error(self):
        self._channel(PPG_ED_CH1)
        self.device.write(":SOURce:PATTern:EADDition:SINGle")

    def get_error_addition_rate(self):
        self._channel(PPG_ED_CH1)
        return self.device.query(":SOURce:PATTern:EADDition:RATE?")

    def set_error_addition_rate(self, exponent):
        self._channel(PPG_ED_CH1)
        self.device.write(":SOURce:PATTern:EADDition:RATE " + "E_" + str(exponent) + ",1")

    def get_error_count_total(self):
        self._channel(PPG_ED_CH1)
        return int(self.device.query(":CALCulate:DATA:EALarm? " + '"CURRent:EC:TOTal"')[1:-1])

    def get_error_count_inserted(self):
        self._channel(PPG_ED_CH1)
        return int(self.device.query(":CALCulate:DATA:EALarm? " + '"CURRent:EC:INSertion"')[1:-1])

    def get_error_count_omitted(self):
        self._channel(PPG_ED_CH1)
        return int(self.device.query(":CALCulate:DATA:EALarm? " + '"CURRent:EC:OMIssion"')[1:-1])

    def get_error_rate_total(self):
        self._channel(PPG_ED_CH1)
        return float(self.device.query(":CALCulate:DATA:EALarm? " + '"CURRent:ER:TOTal"')[1:-1])

    def get_error_rate_inserted(self):
        self._channel(PPG_ED_CH1)
        return float(self.device.query(":CALCulate:DATA:EALarm? " + '"CURRent:ER:INSertion"')[1:-1])

    def get_error_rate_omitted(self):
        self._channel(PPG_ED_CH1)
        return float(self.device.query(":CALCulate:DATA:EALarm? " + '"CURRent:ER:OMIssion"')[1:-1])

    def set_gating_cycle_type(self, mode):
        self._channel(PPG_ED_CH1)
        self.device.write(":SENSe:MEASure:EALarm:MODE " + mode)

    def get_gating_cycle_type(self):
        self._channel(PPG_ED_CH1)
        return self.device.query(":SENSe:MEASure:EALarm:MODE?")

    def set_gating_cycle_period(self, days, hours, minutes, seconds):
        self._channel(PPG_ED_CH1)
        self.device.write(":SENSe:MEASure:EALarm:PERiod " + "{},{},{},{}".format(days, hours, minutes, seconds))

    def get_gating_cycle_period(self):
        self._channel(PPG_ED_CH1)
        return tuple([int(i) for i in self.device.query(":SENSe:MEASure:EALarm:PERiod?").split(",")])

    def get_realtime_measurement_results(self):
        self._channel(PPG_ED_CH1)
        return self.device.query(":DISPlay:RESult:EALarm:MODE?") == "1"

    def set_realtime_measurement_results_off(self):
        self._channel(PPG_ED_CH1)
        self.device.write(":DISPlay:RESult:EALarm:MODE " + OFF)

    def set_realtime_measurement_results_on(self):
        self._channel(PPG_ED_CH1)
        self.device.write(":DISPlay:RESult:EALarm:MODE " + ON)

    def get_last_screenshot(self):
        """
        :return: the byte string of the screenshot file
        """
        self.device.read_termination = None
        self._channel(EYE_PULSE_SCOPE)
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

    def _channel(self, module_number):
        """
        For some reason, doing anything automated to the EYE/Pulse Scope screen
        needs to have the module specified or it wont work. Doing things to other modules
        after setting that module does not work either, so we are just going to set the channel before every command
        :param module_number: the module to let the instrument know that said module has a query coming its way
        """
        self.device.write(":MODule:ID " + str(module_number))

    def what_can_i(self):
        """
        This overrides the base class implementation. Why are we sticking "run_" in front of every method name that we
        want to be run externally when there is already a python standard that says that you can put an underscore
        in front of any class member name that you want to be for internal use only. That seems like a more sustainable
        option, so this class is going to be the change.
        """
        return [method[0] for method in inspect.getmembers(self, inspect.ismethod) if re.match('^[^_].+', method[0])]
