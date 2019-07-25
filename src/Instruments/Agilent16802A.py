import win32com.client
import win32com
import matplotlib.pyplot as plt

from src.Instruments.IPDriver import IPDriver


class Agilent16802A(IPDriver):
    """
    This class models an Agilent 16802A Logic Analyzer
    """

    def __init__(self, IP):
        IPDriver.__init__(self, IP)
        self.name += "Agilent 16802A Logic Analyzer"

        self.connect = win32com.client.Dispatch("AgtLA.Connect")
        device = self.connect.GetInstrument(IP)
        self.device = device
        self.module = None
        self.busSignals = None

    def load_config(self, path):
        """
        This will load a config file given a file path, NOTE: throws exception if config is already loaded
        :param path: The path on the logic analyzer to the config file
        :return: None
        """
        self.device.Open(path)

    def open_module(self, module):
        """
        Opens one of the hardware modules on the logic analyzer
        :param module: The name or index of the module to open
        :return: None
        """
        if isinstance(module, str):
            self.module = self.device.GetModuleByName(module)
        elif isinstance(module, int):
            self.module = self.device.Modules(module)

    def start_capture(self, asynchronous=True, timeout=10):
        """
        Starts a capture on the logic analyzer, can be told to wait for completion
        :param asynchronous: If True this will immediately return after starting the capture, otherwise it will wait for
         the capture to complete
        :param timeout: The maximum time to wait if not asynchronous
        :return: None
        """
        self.device.Run()
        if not asynchronous:
            self.device.WaitComplete(timeout)
        self.busSignals = None

    def get_bus(self, bus_name):
        """
        Retrieves a bus from the logic analyzer
        :param bus_name: The name of the bus to retrieve
        :return: The requested Bus or None
        """
        if self.busSignals is None:
            self.busSignals = self.module.BusSignals
        for index in range(self.busSignals.Count):
            if self.busSignals.Item(index).Name == bus_name:
                return self.busSignals.Item(index)

    def get_bus_data(self, bus, output_chars=True):
        """
        Gets the data associated with a bus from the last sample
        :param bus: The name or instance of the bus to get data from
        :param output_chars: If true the sample is converted to an int
        :return:
        """
        inner_bus = bus
        if isinstance(bus, str):
            inner_bus = self.get_bus(bus)
        bus_data = inner_bus.BusSignalData
        bus_type = inner_bus.BusSignalType
        if bus_data.Type == "Sample":
            sample_data = win32com.client.CastTo(bus_data, "ISampleBusSignalData")
            result = sample_data.GetDataByTime(-float("inf"), float("inf"), bus_type)[0]
            if not output_chars:
                result = [ord(i) for i in result]
            return result

    def get_bus_info(self, bus):
        """
        Gets information associated with a bus from the last sample
        :param bus: The name or instance of the bus to get data from
        :return: A dict containing useful information
        """
        inner_bus = bus
        if isinstance(bus, str):
            inner_bus = self.get_bus(bus)
        bus_data = inner_bus.BusSignalData
        if bus_data.Type == "Sample":
            sample_data = win32com.client.CastTo(bus_data, "ISampleBusSignalData")
            bus_start_time = sample_data.StartTime
            bus_end_time = sample_data.EndTime
            bus_sample_count = (abs(sample_data.StartSample) + abs(sample_data.EndSample))
            return {'Start_Time': bus_start_time, 'End_Time': bus_end_time, 'Sample_Count': bus_sample_count,
                    'Bits': inner_bus.BitSize, "Bytes": inner_bus.BytesSize}

    @staticmethod
    def dec_range(start, end, step):
        """
        Port of built in generator "Range" for floating point and decimal numbers
        :param start: The starting decimal
        :param end: The ending decimal
        :param step: The interval of the range
        :return: A list of decimals
        """
        result = []
        value = start
        while value <= (end + step):
            result.append(value)
            value += step
        return result

    def attach_time_to_sample(self, bus, zipped=False, output_chars=True):
        """
        Attaches each sample to its corresponding time
        :param bus: The name or instance of the bus to get data from
        :param zipped: If true this will Zip the results into a list of tuples, otherwise two lists are returned
        :param output_chars: If true the sample is converted to an int
        :return: Either a list of zipped tuples or a tuple with two lists
        """
        inner_bus = bus
        if isinstance(bus, str):
            inner_bus = self.get_bus(bus)
        bus_info = self.get_bus_info(inner_bus)
        sample_rate = (abs(bus_info['Start_Time']) + abs(bus_info['End_Time'])) / (bus_info['Sample_Count'])
        y_axis = self.get_bus_data(inner_bus, output_chars)
        x_axis = self.dec_range(bus_info['Start_Time'], bus_info['End_Time'], sample_rate)

        if zipped:
            temp = zip(x_axis, y_axis)
        else:
            temp = (x_axis, y_axis)
        return temp

    def display_bus(self, bus):
        """
        Displays the data from a bus
        :param bus: The name or instance of the bus to get data from
        :return: None
        """
        inner_bus = bus
        if isinstance(bus, str):
            inner_bus = self.get_bus(bus)
        points = self.attach_time_to_sample(inner_bus, False)

        plt.plot(points[0], points[1])

        plt.show()
