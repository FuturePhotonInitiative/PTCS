import logging
import sys

from src.Instruments.PyVisaDriver import PyVisaDriver

# the rotating stage class for the ELL8/M motor
# 	- wraps around Rot_Motor
DEG_PER_CNT = 0.00137329


class ELL8(PyVisaDriver):
    """
    This class models an ELL8 rotation stage
    """

    def __init__(self, device):
        """
            Constructor
        """
        PyVisaDriver.__init__(self)
        self.name += "ELL8"
        self.device = device

        self.position = 0
        self.zeros_position = 0
        self.count = -1

        # get the logger we loaded once in the beginning
        self.logger = logger

        # extra class info - for logger
        # self.ext = {'com_port': self.ser.port, 'ClassName': 'Rot_Motor'}

        self.home()

    def delta_move(self, steps):
        """
            rotate the stage by specified # of steps
        """
        self.position += steps

        # HOSTREQ_MOVERELATIVE
        self.device.write('0mr')

        # converted this line to not use this function
        # self.device.write(int2hex_str(steps, 4))
        self.device.write_binary_values('', [steps], datatype='i', is_big_endian=sys.byteorder != 'little')

        # wait for ell8 position message
        self.device.read(termination='0pO')

    def abs_move(self, steps):
        """
            rotate the stage by specified # of steps
        """

        # HOSTREQ_MOVERELATIVE
        self.device.write('0mr')

        # converted this line to not use this function
        # self.device.write(int2hex_str(steps - self.position, 4))
        self.device.write_binary_values('', [steps - self.position], datatype='i',
                                        is_big_endian=sys.byteorder != 'little')

        self.position = steps

        # wait for ell8 position message
        self.device.read(termination='0pO')

    def home(self):
        """
            homes the stage
        """
        #
        self.device.write('0ho0')
        self.device.read(termination='0pO')

    def get_position(self):
        """
         return the motors current position
        """
        # _HOSTREQ_HOME
        return self.position

    def set_as_zero(self, zer_deg):
        """
         change the origin (zero)
        """

        # TODO resolve missing new_zero reference

        self.zeros_position = zer_deg
        self.position -= zer_deg

    def set_vel_params(self, vel):
        """
         Set the velocity parameters for the motor in terms of percentage of max
        """

        # HOSTSET_VELOCITY
        self.device.write('0sv')  # head
        self.device.write(vel)

    def __str__(self):
        """
         <For Debugging Purposes>
         gives information relevant to the motor state
        """
        return 'position: ' + str(self.position) + '\nzeros-position: ' + str(self.zeros_position)

    def close(self):
        """
            releases motor control
        """
        self.device.close()
    """
    Unnecessary function. read() will take care of this wait
    def move_complete(self):
        rx = ''
        while rx[:3] != '0PO':
            if self.device.in_waiting > 0:
                rx = str(self.device.read())

    def _get_count(self):
        return self.count
    """


class Thorlabs_ELL8_M(ELL8):
    """
    This class models an ELL8 rotation stage motor
    """

    def __init__(self, device):
        """
         Constructor

         ser (Serial): the Serial object that corresponds to the port
         the motor is connected to
        """
        ELL8.__init__(self, device)

        self.moving = False  # set to false
        self.deg_pos = 0  # position of motor, in degrees
        self.deg_zeros = 0  # the origin, in degrees

    def delta_angle(self, deg):  # , m callback = None, params = ()):
        """
         Relative rotation on the motor

         deg (float): the degrees of rotation (negative -> counter-clockwise)
        """
        self.moving = True
        self.deg_pos += deg
        # convert degrees to steps
        steps = int(round(deg / DEG_PER_CNT))

        super(self).delta_move(steps)
        while self.deg_pos >= 360:
            self.deg_pos -= 360
        self.moving = False

    def abs_angle(self, deg):
        """
         Relative rotation on the motor

         deg (float): the degrees of rotation (negative -> counter-clockwise)
        """
        d = deg
        while d >= 360:
            d -= 360

        self.moving = True
        # convert degrees to steps
        steps = int(round(d / DEG_PER_CNT))

        super(self).abs_move(steps)
        self.deg_pos = d
        self.moving = False

    def get_angle(self):
        """
         return the motors current position, in degrees
        """
        return self.deg_pos

    def set_as_zero(self, zer_deg):
        """
         change the origin (zero)
        """
        n_zero = int(round(zer_deg / DEG_PER_CNT))
        super(self).set_as_zero(n_zero)

        self.deg_zeros = zer_deg
        self.deg_pos -= zer_deg

    def __str__(self):
        """
         <For Debugging Purposes>
         gives information relevant to the motor state
        """
        return 'position(degrees): ' + str(self.deg_pos) + '\nzeros-position(degrees): ' + str(self.deg_zeros)


# the motor class for ELL8/M Rotation Stage
# this function can be converted into a single line with write_binary_values
# def int2hex_str(integer, nb):
# 	"""
# 	 Convert an integer to its corresponding byte-array
#
# 	 integer (int): the number we want to convert
# 	 nb (int): the number of bytes
# 	"""
#
# 	bytes = []
# 	for i in range(nb):
# 		bytes.append(integer & 0x0FF)
# 		integer = integer >> 8
# 	bytes.reverse()
# 	s = str(binascii.hexlify(bytearray(bytes)))
# 	return s.upper()

# not needed
# def hex_string(data):
# 	"""
# 	 Creates a string that is a byte sequence of the hex values
# 	 input
# 	 e.g. data = '0A 23 34 56'
# 	"""
#
# 	h_str = ''
# 	data = data.split(' ')
# 	for byte in data:
# 		h_str += r'\x' + byte
#
# 	return h_str.decode('string_escape')


# setup the Logger
# -> should be done once
# initialize the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('[%(asctime)-15s] %(ClassName)s<%(com_port)s>: %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


'''
Copyright (C) 2017  Robert Polster
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
