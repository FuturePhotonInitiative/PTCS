import struct

from src.Instruments.IEEE_488_2 import IEEE_488_2


class Agilent_HP8163A(IEEE_488_2):
    """
    This class models an Agilent HP8163A Lightwave Multimeter
    """

    def __init__(self, device):
        IEEE_488_2.__init__(self)
        self.name += "Agilent HP8163A Lightwave Multimeter"
        self.device = device

        self.__channel = None
        self.__port = None

    def set_channel(self, channel):
        if '.' in str(channel):
            segments = channel.split('.')
            self.__channel = int(segments[0])
            self.__port = int(segments[1])
        else:
            self.__channel = int(channel)
            self.__port = 1

    def get_power(self):
        cmd = 'read'
        cmd += self.__channel + ':chan' + self.__port
        cmd += ':pow?'
        return float(self.device.query(cmd))

    def config_meter(self, range):
        if self.__port != 2:
            range = str(range)
            self.device.write('sens' + self.__channel + ':chan' + self.__port + ':pow:unit 0')
            self.device.write('sens' + self.__channel + ':chan' + self.__port + ':pow:range:auto 0')
            self.device.write('sens' + self.__channel + ':chan' + self.__port + ':pow:range ' + range + 'DBM')

    def prep_measure_on_trigger(self, samples=64):
        if self.__port != 2:
            self.clear_status()
            samples = str(samples)
            self.device.write('sens' + self.__channel + ':chan' + self.__port + ':func:stat logg,stop')
            self.device.write('trig' + self.__channel + ':chan' + self.__port + ':inp sme')
            self.device.query('trig' + self.__channel + ':inp?')
            self.device.write('sens' + self.__channel + ':chan' + self.__port + ':func:par:logg ' + samples + ',100us')
            self.device.query('sens' + self.__channel + ':chan' + self.__port + ':func:par:logg?')
            self.device.write('sens' + self.__channel + ':chan' + self.__port + ':func:stat logg,start')
            self.device.query('sens' + self.__channel + ':chan' + self.__port + ':func:stat?')
            self.device.query('syst:err?')

    def get_results_from_log(self, samples=64):
        if self.__port != 2:
            self.device.query('sens' + self.__channel + ':chan' + self.__port + ':func:stat?')
        samples = int(samples)
        self.device.write('sens' + self.__channel + ':chan' + self.__port + ':func:res?')
        raw_data = self.device.read_raw()
        self.device.query('syst:err?')

        num_digits = int(raw_data[1])
        hex_data = raw_data[2 + num_digits: 2 + num_digits + samples * 4]
        flo_data = []

        for idx in range(0, samples*4-1,4):
            data = hex_data[idx: idx+4]
            value = struct.unpack('<f', struct.pack('4c', *data))[0]
            flo_data.append(value)

        return flo_data[1:]
