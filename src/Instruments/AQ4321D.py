from src.Instruments.GPIBtoUSBAdapter import GPIBtoUSBAdapter
import time

MIN_POWER = -20.0
MAX_POWER = 10.0
MIN_WAVELENGTH = 1520.000
MAX_WAVELENGTH = 1620.000
MIN_SWEEP_WAVELENGTH = .001
MAX_SWEEP_WAVELENGTH = 100.000

SWEEP_MODE_STEP = 0
SWEEP_MODE_CONTINUOUS = 1
SWEEP_MODE_TRIGGER = 2
MIN_STEP_TIME = .1
MAX_STEP_TIME = 999.0
MIN_CONT_TIME = 1.0
MAX_CONT_TIME = 99999.0
THOUSANDTHS = .001
TENTHS = .1


class AQ4321D(GPIBtoUSBAdapter):

    def __init__(self, device):
        GPIBtoUSBAdapter.__init__(self)
        self.device = device
        self.name += "Ando AQ4321D laser"

        self.become_controller()
        self.set_gpib_address(24)

        # Reading data will hang with PyVisa if this is not set
        self.turn_message_delimiters_on()

        # strip the terminating \r\n off the message when querying the instrument
        device.read_termination = "\r\n"

    def identify(self):
        """
        :return: Instrument information. This device does not fully conform to IEEE-488.2 though
        """
        return self._query_device("*IDN?")

    def turn_message_delimiters_on(self):
        """
        If run, every message read from the instrument will have a guaranteed \r\n on the end of it
        """
        self._send_to_device("DELIM1")

    def turn_message_delimiters_off(self):
        """
        If run, there will not be a termination sequence of commands coming from the instrument
        """
        self._send_to_device("DELIM0")

    def enter_password(self):
        """
        Logs onto the instrument when first booted up
        """
        self._send_to_device("PASSWORD4321")

    def is_initializing(self):
        """
        :return: if the instrument is initializing or not
        """
        return self._query_device("INIT?") == "1"

    def get_wavelength(self):
        """
        :return: The current wavelength setting in nm.
        """
        return float(self._query_device("TWL?"))

    def set_wavelength(self, wavelength):
        """
        :param wavelength: The wavelength to set. 1520.000 to 1620.000 inclusive, up to the thousandths place.
        """
        self._check_float(wavelength, MIN_WAVELENGTH, MAX_WAVELENGTH, THOUSANDTHS)
        self._send_to_device("TWL{}".format(wavelength))

    def get_power(self):
        """
        :return: The current power setting in dBm
        """
        return float(self._query_device("TPDB?"))

    def set_power(self, power):
        """
        :param power: The power to set. -20.0 to 10.0 inclusive, up to the tenths place.
        """
        self._check_float(power, MIN_POWER, MAX_POWER, TENTHS)
        self._send_to_device("TPDB{}".format(power))

    def set_start_sweep_wavelength(self, wavelength):
        """
        :param wavelength: The wavelength the sweep should start at
        """
        self._check_float(wavelength, MIN_WAVELENGTH, MAX_WAVELENGTH, THOUSANDTHS)
        self._send_to_device("TSTAWL{}".format(wavelength))

    def set_stop_sweep_wavelength(self, wavelength):
        """
        :param wavelength: The wavelength the sweep should end at
        """
        self._check_float(wavelength, MIN_WAVELENGTH, MAX_WAVELENGTH, THOUSANDTHS)
        self._send_to_device("TSTPWL{}".format(wavelength))

    def set_step_sweep_wavelength(self, wavelength):
        """
        :param wavelength: The amount of wavelength the sweep should traverse each step
        """
        self._check_float(wavelength, MIN_SWEEP_WAVELENGTH, MAX_SWEEP_WAVELENGTH, THOUSANDTHS)
        self._send_to_device("TSTEWL{}".format(wavelength))

    def set_step_time_sweep(self, time):
        """
        :param time: The time that each step should take
        """
        self._check_float(time, MIN_STEP_TIME, MAX_STEP_TIME, TENTHS)
        self._send_to_device("TSTET{}".format(time))

    def run_sweep_step(self, start, stop, wavelength_step, time_step):
        """
        Runs a step based sweep. This will run the necessary number of steps depending on how long each step should
        take and how much wavelength should be traversed at each step
        :param start: The wavelength the sweep should start at
        :param stop: The wavelength the sweep should end at
        :param wavelength_step: The amount of wavelength the sweep should traverse each step
        :param time_step: The time that each step should take
        """
        self._send_to_device("TSWM{}".format(SWEEP_MODE_STEP))  # this is the step version of a sweep
        self.set_start_sweep_wavelength(start)
        self.set_stop_sweep_wavelength(stop)
        self.set_step_sweep_wavelength(wavelength_step)
        self.set_step_time_sweep(time_step)
        self.turn_laser_on()
        self.start_sweep()
        # aparently the instrument freezes for about 6 seconds right after the laser is
        # turned on and the start sweep command is issued
        time.sleep(6)
        self._print("Step sweeping in progress...")
        while self.sweep_in_progress():
            self._print("sweep in progress")
            time.sleep(1)
        self.turn_laser_off()
        self._print("Sweeping Done!")

    def set_cont_time_sweep(self, time):
        """
        :param time: How long the continuous sweep should take in total
        """
        self._check_float(time, MIN_CONT_TIME, MAX_CONT_TIME, TENTHS)
        self._send_to_device("TSWET{}".format(time))

    def run_sweep_continuous(self, start, stop, time_length):
        """
        Runs a continuous sweep. This appears to be like one step of a step based sweep.
        :param start: The wavelength the sweep should start at
        :param stop: The wavelength the sweep should end at
        :param time_length: How long the continuous sweep should take in total
        :return:
        """
        self._send_to_device("TSWM{}".format(SWEEP_MODE_CONTINUOUS))  # this is the continuous mode of a sweep
        self.set_start_sweep_wavelength(start)
        self.set_stop_sweep_wavelength(stop)
        self.set_cont_time_sweep(time_length)
        self.turn_laser_on()
        self.start_sweep()
        # aparently the instrument freezes for about 6 seconds right after the laser is
        # turned on and the start sweep command is issued
        time.sleep(6)
        self._print("Continuous sweeping in progress for {} seconds...".format(time_length))
        while self.sweep_in_progress():
            time.sleep(1)
        self.turn_laser_off()
        self._print("Sweeping Done!")

    def sweep_in_progress(self):
        """
        :return: if a sweep is in progress or not
        """
        return self._query_device("TSWEEP?")[2] != "0"

    def start_sweep(self):
        """
        starts the currently selected and configured sweep
        """
        self._send_to_device("TSGL")

    def stop_sweep(self):
        """
        Stops the currently running sweep if one was running
        """
        self._send_to_device("TSTP")

    def pause_sweep(self):
        """
        Pauses the currently running sweep
        """
        self._send_to_device("TPAS")

    def resume_sweep(self):
        """
        Resumes the currently paused sweep
        """
        self._send_to_device("TCONT")

    def start_repeat_sweep(self):
        self._send_to_device("TRET")

    def turn_laser_on(self):
        """
        Turns the laser on. This may take some time in certain scenarios
        """
        self._print("turning laser on")
        self._send_to_device("L1")

    def turn_laser_off(self):
        """
        Turns the laser off.
        """
        self._print("turning laser off")
        self._send_to_device("L0")

    @staticmethod
    def _check_float(num, min, max, precision):
        """
        Checks num for bounds, precision and None. Raises an exception if any checks fail
        :param num: A float value to check
        :param min: The minimum value the num can be inclusive
        :param max: The maximum value the num can be inclusive
        :param precision: The smallest absolute value a number can be away from the next number
        """
        if num is None or not min <= num <= max or not (num * (1/precision)).is_integer():
            raise Exception("Value: {} out of allotted range: {} to {} or too precise".format(num, min, max))

    def _query_device(self, query):
        """
        The GPIB to USB adapter needs to know that it is expecting a response from the instrument.
        :param query: the query string to ask the instrument
        :return: the response string
        """
        self.turn_on_read_after_write()
        return self.device.query(query)

    def _send_to_device(self, query):
        """
        :param query: the query string to ask the instrument
        """
        self.turn_off_read_after_write()
        self.device.write(query)

    @staticmethod
    def _print(string):
        print("ANDO-AQ4321D> " + string)

# Code from the legacy driver that may be useful in the future:

#     def run_set_wavelength(self, wavelength):
#         """
#         Loads a single wavelength and sets output high
#
#         :param wavelength: Specified wavelength
#         :type wavelength: Integer
#         """
#         self.run_output_off()
#
#         if wavelength < 1520 or wavelength > 1620:
#             print ('Specified Wavelength Out of Range')
#         else:
#             # Execute setting of wavelength
#             self.device.write('TWL ' + str(wavelength))
#             time.sleep(0.55)
#             self.device.write('TWL?')
#             info = self.device.read()
#             print ('Wavelength Sent: %s' % info)
#
#             self.device.write('L1')
#
#             # High for test period
#             while self.run_check_status_single() is False:
#                 time.sleep(0.1)
#                 # Print if successful
#             print('Single Wavelength Complete')
#
#     def run_sweep_wavelengths_trigger_setup(self, start, end, step):
#         """
#         Have to keep track of Triggers in main command, use Stop Sweep Command to end sweep.
#         Extra triggers do not make the laser sweep outside of specified end wavelength.
#         Remember to shut off laser after sweep ends
#
#         :param start: Specified wavelength between 1520-1580
#         :type start: Integer
#         :param end: Specified wavelength between 1520-1580
#         :type end: Integer
#         :param step: Specified time
#         :type step: Float
#         """
#
#         self.run_output_off()
#         self.run_stop_sweep()
#
#         if (
#             float(start) < 1520 or
#             float(start) > 1580 or
#             float(end) < 1520 or
#             float(end) > 1580 or
#             float(step) < 0.001
#         ):
#             print ('Specified Wavelengths Out of Range, or Step Too Low')
#
#         else:
#             self.device.write('TSWM 2')
#             self.device.write('TSTAWL ' + str(start))
#             self.device.write('TSTPWL ' + str(end))
#             self.device.write('TSTEWL ' + str(step))
#             self.device.write('L1')
#             self.device.write('TSGL')  # Single Sweep
#             time.sleep(4)
#             print ('Trigger Setup Complete')
#
#     def trigger(self):
#         """Triggers laser"""
#
#         time.sleep(0.4)
#         self.device.write('TRIG')
#         time.sleep(0.05)
#
#     def run_check_status(self):
#         """
#         Checks the status of the laser. Handles timeout exception
#
#         :returns: Boolean
#         """
#
#         try:
#             self.device.write('SRQ3?')
#             status = int(self.device.read())
#             print('Status: %d' % status)
#             if status > 0:
#                 return True
#             else:
#                 return False
#         except pyvisa.errors.VisaIOError:
#             time.sleep(0.2)
#             return self.run_check_status()
#
#     def run_check_status_single(self):
#         """
#         Checks the status of the laser. Handles timeout exception
#
#         :returns: Boolean
#         """
#
#         try:
#             self.device.write('SRQ0?')
#             status = int(self.device.read())
#             if status > 0:
#                 return True
#             else:
#                 return False
#         except pyvisa.errors.VisaIOError:
#             time.sleep(0.2)
#             return self.run_check_status()
#
#     def run_manual_step(self, step):
#         """
#         Use if want to manually step by a particular size, in con-junction with Send Single Wavelength
#
#         :param step: specified step increment, but be greater than or equal to 0.001
#         :type step: Float
#         """
#
#         if step < 0.001:
#                 print('Step size cannot be lower than 0.001')
#         else:
#             self.device.write('TSTEWL ' + str(step))
#             self.device.write('TWLUP')
#
# '''
# Copyright (C) 2017  Robert Polster
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# '''
