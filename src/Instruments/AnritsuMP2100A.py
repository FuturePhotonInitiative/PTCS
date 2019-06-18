# coding=UTF-8

from src.Instruments.IEEE_488_2 import IEEE_488_2

# channel numbers
PPG_ED_CH1 = 1
SFP = 3
EYE_PULSE_SCOPE = 5
JITTER_ANALYSIS = 6
TRANSMISSION_ANALYSIS = 7


# test if it is possible to do stuff while output and measure is on
# set vs query
# get vs change
class AnritsuMP2100A(IEEE_488_2):

    def __init__(self, device):
        IEEE_488_2.__init__(self, device, "Anritsu MP2100A BERT Analyzer")
        self.device.read_termination = '\n'

    # ✓
    def run_run_all_measurements(self):
        self.device.write("*TRG")

    # ✓
    def run_stop_all_measurements(self):
        self.device.write(":SENSe:MEASure:ASTP")

    # ✓
    def run_get_device_option_codes(self):
        return self.device.query("*OPT?")

    # ✓
    def run_query_is_running(self):
        return self.device.query(":SENSe:MEASure:ASTate?") == 1

    # ✓
    def run_change_bitrate(self, bitrate):
        self.channel(PPG_ED_CH1)
        self.device.write(":SENSe:PARam:TRACking 1")
        self.device.write(":OUTPut:BITRate:STANdard " + bitrate)

    # ✓
    def run_query_bitrate(self):
        self.channel(PPG_ED_CH1)
        return self.device.query(":OUTPut:BITRate:STANdard?")

    # ✓
    def run_clear_display(self):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":DISPlay:WINDow:GRAPhics:CLEar")

    # ✓
    def run_query_amplitude(self):
        self.channel(PPG_ED_CH1)
        return self.device.query(":OUTPut:DATA:AMPLitude? DATA")

    # ✓
    def run_set_amplitude(self, amplitude):
        self.channel(PPG_ED_CH1)
        self.device.write(":OUTPut:DATA:AMPLitude DATA," + str(amplitude))

    # ✓
    def run_set_scale(self, scale):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":DISPlay:WINDow:Y:DIVision:CHA " + str(scale))

    # ✓
    def run_query_scale(self):
        self.channel(EYE_PULSE_SCOPE)
        return self.device.query(":DISPlay:WINDow:Y:DIVision:CHA?")

    # ✓
    def run_set_amplitude_offset(self, offset):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":DISPlay:WINDow:Y:OFFSets:CHA " + str(offset))

    # ✓
    def run_query_amplitude_offset(self):
        self.channel(EYE_PULSE_SCOPE)
        return self.device.query(":DISPlay:WINDow:Y:OFFSets:CHA?")

    def run_save_eye_screenshot_to_file(self):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":EYEPulse:PRINt:COPY")

    def run_save_full_screen_screenshot_to_file(self):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":SYSTem:PRINt:COPY")

    def run_obtain_screenshot(self):
        self.device.query(":SYSTem:DISPlay:DATA?")

    # ✓
    def run_turn_on_output(self):
        self.device.write(":SOURce:OUTPut:ASET ON")

    # ✓
    def run_turn_off_output(self):
        self.device.write(":SOURce:OUTPut:ASET OFF")

    # ✓
    def run_query_sample_run_state(self):
        self.channel(EYE_PULSE_SCOPE)
        return self.device.query(":SAMPling:STATus?")

    # ✓
    def run_run_sample(self):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":SAMPling:STATus RUN")

    # ✓
    def run_hold_sample(self):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":SAMPling:STATus HOLD")

    # ✓
    def run_set_bit_view_number(self, bits):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":DISPlay:WINDow:X:BITs " + str(bits))

    # ✓
    def run_get_bit_view_number(self):
        self.channel(EYE_PULSE_SCOPE)
        return self.device.query(":DISPlay:WINDow:X:BITs?")

    # ✓
    def run_get_time_offset(self):
        self.channel(EYE_PULSE_SCOPE)
        return self.device.query(":DISPlay:WINDow:X:OFFSets?")

    # ✓
    def run_set_time_offset(self, offset):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":DISPlay:WINDow:X:OFFSets " + str(offset))

    # ✓
    def run_set_display_type(self, display_type):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":DISPlay:MODE " + str(display_type))

    # ✓
    def run_get_display_type(self):
        self.channel(EYE_PULSE_SCOPE)
        return self.device.query(":DISPlay:MODE?")

    # ✓
    def run_get_sample_limit(self):
        self.channel(EYE_PULSE_SCOPE)
        return self.device.query(":ACCUmulation:LIMit?")

    # ✓
    def run_set_samples_limit(self, sample_limit):
        self.channel(EYE_PULSE_SCOPE)
        self.device.write(":ACCUmulation:TYPe LIMited")
        self.device.write(":ACCUmulation:LIMit SAMPLe," + str(sample_limit))

    def channel(self, module_number):
        """
        For some reason, doing anything automated to the EYE/Pulse Scope screen
        needs to have the module specified or it wont work. Doing things to other modules
        after setting that module does not work either, so we are just going to set the channel before every command
        :param module_number: the module to let the instrument know that said module has a query coming its way
        """
        self.device.write(":MODule:ID " + str(module_number))
