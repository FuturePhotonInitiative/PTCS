import datetime
import time
import re

from src.Instruments.PyVisaDriver import PyVisaDriver


class Polatis_3000(PyVisaDriver):
    """
    This class models a Polatis 3000 Switch
    """

    def __init__(self, device):
        PyVisaDriver.__init__(self)
        self.name += "Polatis 3000 Switch"
        self.device = device

    def get_all_connections(self):
        return str(self.device.query(':oxo:swit:conn:stat?'))[:-2]

    def get_port_stat(self, port_number):
        time.sleep(0.1)
        return str(self.device.query(':oxc:swit:conn:port? %d' % port_number))[:-2]

    def reset(self):
        time.sleep(0.1)
        self.device.write('*RST;')

    def quick_connect(self, ingress=0, egress=0):
        ingress = int(ingress)
        egress = int(egress)
        if ingress > egress:
            ingress, egress = egress, ingress

        formatted = self.__format_connections__(ingress, egress)
        self.device.write(':oxc:swit:conn:add ' + formatted + ';')

    def make_connections(self, ingress, egress, explicit='only'):
        formatted = self.__format_connections__(ingress, egress)
        if re.match('(only|add|sub)', explicit):
            self.device.write(':oxc:swit:conn:' + explicit + ' ' + formatted + ';')

    def __make_connections__(self, ports):
        time.sleep(0.1)
        self.device.write(':oxc:swit:conn:only '+ports+';')

    @staticmethod
    def __format_connections__(ingress, egress):
        if not isinstance(ingress, list):
            ingress = [ingress]
        if not isinstance(egress, list):
            egress = [egress]
        return ','.join([','.join(map(str, i)).join(['(@', ')']) for i in [ingress, egress]])

    def get_boot_mode(self):
        return str(self.device.query(':oxc:boot:mode?'))

    def set_boot_mode(self, mode='aut'):
        if re.match('(DARK|REST(ore)?|AUT(osave)?)', mode):
            self.device.write(':oxc:boot:mode ' + mode + ';')

    def cmd_line(self, commands):
        if not isinstance(commands, list):
            commands = [i + ';' for i in commands.split(';')]
        replies = {}
        for cmd in commands:
            replies[cmd] = self.__cmd_handler__(cmd)
        return replies

    def __cmd_handler__(self, command):
        try:
            if re.match('.+\?$', command):
                return self.device.query(command)
            else:
                self.device.write(command)
                return None
        except Exception as e:
            return e

    def write_pattern(self, name='newPattern.txt'):
        with open(name, 'w') as f:
            f.write(name+' '+str(datetime.datetime.now())+'\n')
            time.sleep(0.1)
            f.write(self.get_all_connections())

    def read_pattern(self, name='newPattern.txt', load=True):
        try:
            with open(name, 'r') as f:
                f.readline()
                pattern = f.readline()
                if load:
                    self.reset()
                    self.__make_connections__(pattern)
                else:
                    return pattern
        except Exception as e:
            return e

    def get_zip_connections(self):
        connections = [re.sub('[(@)]', '', i).split(',') for i in self.get_all_connections().split("),(")]
        return list(zip(connections[0], connections[1]))