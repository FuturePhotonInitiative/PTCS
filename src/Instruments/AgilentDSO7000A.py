import re

from src.Instruments.IEEE_488_2 import IEEE_488_2


class AgilentDSO7000A(IEEE_488_2):
    """
    This class models an Agilent DSO7000A Oscilloscope.
    """

    def __init__(self, device):
        """
        Constructor method.

        :param device: device from PyVisa open_resource object
        :type: PyVisa open_resource object
        """
        IEEE_488_2.__init__(self)
        self.name += "Agilent DSO7000A Oscilloscope"
        self.device = device

    def measure_set_source(self, channel_num):
        """
        Set source to measure
        :param: channel_num, channel number to measure
        :return: None
        """
        self.device.write(":MEASURE:SOURCE CHANNEL"+str(channel_num))

    def measure_vpp(self, channel_num=None):
        """
        Measure VPP from preset source
        :param: channel_num, channel number to measure
        :return: VPP from Source
        """
        if channel_num is not None:
            return self.device.query(":MEAS:VPP? CHAN"+str(channel_num), delay=8.25)
        else:
            return self.device.query(":MEAS:VPP?", delay=8.25)

    def measure_vaverage(self, channel_num=None):
        """
        Measure average voltage
        :param: channel_num, channel number to measure
        :return: Voltage average
        """
        if channel_num is not None:
            return self.device.query(":MEAS:VAV? CHAN"+str(channel_num), delay=8.25)
        else:
            return self.device.query(":MEAS:VAV?", delay=8.25)

    def measure_clear(self):
        """
        Clears commands from all measurements and markers
        :return:
        """
        self.device.write(":MEAS:CLE")

    def measure_duty_cycle(self, channel_num):
        """
        Measures duty cycle of source provided
        :param: channel_num: channel number to measure
        :return: Duty Cycle
        """
        if channel_num is not None:
            return self.device.query(":MEAS:DUTY? CHAN"+str(channel_num), delay=8.25)
        else:
            return self.device.query(":MEAS:DUTY?", delay=8.25)

    def measure_fall_time(self, channel_num=None):
        """
        Measure fall time of source provided
        :param channel_num, channel number to measure
        :return: Fall Time (seconds)
        """
        if channel_num is not None:
            return self.device(":MEAS:FALL? CHAN"+str(channel_num), delay=8.25)
        else:
            return self.device(":MEAS:FALL?", delay=8.25)

    def measure_frequency(self, channel_num=None):
        """
        Measure frequency of source provided
        :param channel_num, channel number to measure
        :return: Frequency (Hertz)
        """
        if channel_num is not None:
            return self.device(":MEAS:FREQ? CHAN"+str(channel_num), delay=8.25)
        else:
            return self.device(":MEAS:FREQ?", delay=8.25)

    def measure_nwidth(self, channel_num=None):
        """
        Measures negative pulse width of source provided
        :param channel_num, channel number to measure
        :return: Pulse Width (seconds)
        """
        if channel_num is not None:
            return self.device.query(":MEAS:NWID? CHAN"+str(channel_num), delay=8.25)
        else:
            return self.device.query(":MEAS:NWID?", delay=8.25)

    def measure_overshoot(self, channel_num=None):
        """
        Measure overshoot of source provided
        :param channel_num, channel number to measure
        :return: Overshoot percentage
        """
        if channel_num is not None:
            return self.device.query(":MEAS:OVER? CHAN"+str(channel_num), delay=8.25)
        else:
            return self.device.query(":MEAS:OVER?", delay=8.25)

    def measure_period(self, channel_num=None):
        """
        Measure period of source provided
        :param channel_num, channel number to measure
        :return: Period (seconds)
        """
        if channel_num is not None:
            return self.device.query(":MEAS:PER? CHAN"+str(channel_num), delay=8.25)
        else:
            return self.device.query(":MEAS:PER?", delay=8.25)

    def measure_phase(self, channel_num=None):
        """
        Measure phase of source provided
        :param channel_num, channel number to measure
        :return: Phase (degrees)
        """
        if channel_num is not None:
            return self.device.query(":MEAS:PHAS? CHAN" + str(channel_num), delay=8.25)
        else:
            return self.device.query(":MEAS:PHAS?", delay=8.25)

    def measure_preshoot(self, channel_num=None):
        """
        Measure preshoot of source provided
        :param channel_num, channel number to measure
        :return: Preshoot (percentage)
        """
        if channel_num is not None:
            return self.device.query(":MEAS:PRES? CHAN"+str(channel_num), delay=8.25)
        else:
            return self.device.query(":MEAS:PRES?", delay=8.25)

    def measure_pulse_width(self, channel_num=None):
        """
        Measure pulse width of source provided
        :param channel_num, channel number to measure
        :return: Pulse width (seconds)
        """
        if channel_num is not None:
            return self.device.query(":MEAS:PWID? CHAN"+str(channel_num), delay=8.25)
        else:
            return self.device.query(":MEAS:PWID?", delay=8.25)

    def measure_results(self, channel_num=None):
        """
        Measure all results
        :param channel_num, channel number to measure
        :return: Results (list of variables)
        """
        # Turn on statistics to also provide labels for values received
        self.device.write(":MEAS:STAT 1")
        return_results = {}
        if channel_num is not None:
            results = self.device.query(":MEAS:RES? CHAN"+str(channel_num), delay=8.25)
        else:
            results = self.device.query(":MEAS:RES?", delay=8.25)
        first_header = re.compile(r'(?P<header>[a-zA-Z\-]+?)\(.*\),')
        header = re.compile(r',+?(?P<header>[a-zA-Z\-]+?)\(.*\),')
        value = re.compile(r'.*?,(?P<value>.*?),')
        header_match = first_header.match(results)
        while True:
            if header_match is not None:
                head = header_match.group('header')
                return_results[head] = []
                results = results[results.index(head) + len(head):]
            header_match = header.match(results)
            while header_match is None:
                value_match = value.match(results)
                if value_match is not None:
                    val = value_match.group('value')
                    return_results[head].append(val)
                    results = results[results.index(val) + len(val):]
                header_match = header.match(results)
                if header_match is None and value_match is None:
                    return return_results

    def start_acquisition(self):
        """
        Start acquiring data
        :return: None
        """
        self.device.write(":RUN")

    def single_acquisition(self):
        """
        Run a single acquisition
        :return: None
        """
        self.device.write(":SINGLE")

    def stop_acquisition(self):
        """
        Stop running acquisition
        :return: None
        """
        self.device.write(":STOP")

    def set_channel_coupling(self, channel_num, acdc):
        """
        Set AC/DC coupling for channels
        :param: channel_num, channel number to set coupling
        :param: acdc, choice of ac or dc coupling to channel selected
        :return: None
        """
        self.device.write(":CHAN"+str(channel_num)+":COUP "+str(acdc))

    def set_channel_label(self, channel_num, label):
        """
        Set channel label
        :param: channel_num, channel number to set label
        :param: label, label to set to channel_num
        :return: None
        """
        self.device.write("CHAN"+str(channel_num)+":LAB "+str(label))

    def set_channel_impedance(self, channel_num, imp):
        """
        Set the channel impedance
        :param: channel_num, number of channel to change
        :param: imp, impedance choice of either ONEMEG or FIFTY
        :return: None
        """
        self.device.write(":CHAN"+str(channel_num)+":IMP "+imp)

    def set_channel_scale(self, channel_num, scale):
        """
        Set the channel scaling
        :param: channel_num, number of channel to change
        :param: scale, scaling factor 5V or 4mV
        :return: None
        """
        self.device.write(":CHAN"+str(channel_num)+":SCALE"+str(scale))

    def save_capture(self, name="Image"):
        """
        Saves the current capture from the oscilloscope
        :return: Filepath to find the file
        """
        # Sets file name to name
        self.device.write("SAVE:FIL "+str(name))
        # Saves image
        self.device.write(":SAVE:IMAG")
        # Return the saved file path and file name
        return self.device.query(":SAVE:PWD?")+self.device.query("SAVE:FIL?")

    def time_range(self, time_ns):
        """
        Update the timebase to specified value
        :param time_ns: time to set, in ns
        :return: None
        """
        self.device.write(":TIM:RANG "+str(time_ns))

    def time_scale(self, time_ps):
        """
        Update the time scale to specified value
        :param time_ps: time to set, in ps
        :return: None
        """
        self.device.write(":TIM:SCAL "+str(time_ps))

    def time_window_scale(self, time_val):
        """
        Update the window time scale seconds/division
        :param time_val: time in seconds
        :return: None
        """
        self.device.write(":TIM:WIND:SCAL "+str(time_val))

    def trigger_mode(self, mode):
        """
        Set the trigger mode to any of the following:
        EDGE, GLITch, PATTern, CAN, DURation, I2S, IIC, EBURst, LIN, M1553, SEQuence, SPI, TV,
        UART, USB, FLEXray
        :param mode: mode to change the trigger to. See above for options
        :return: None
        """
        self.device.write("TRIG:MODE "+mode)
