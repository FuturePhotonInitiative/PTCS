import time
import pyvisa

from src.Instruments.PyVisaDriver import PyVisaDriver


class AQ4321(PyVisaDriver):
    """
    This class models an Ando AQ4321 laser.

    .. note:: When using any laser command, remember to send shut-off-laser
              command at the end of each sweep command set.
              For Trigger Sweep, send shut-off-laser command
              after sweep ends (sweep end condition noted in TriggerSweepSetup function
    """

    def __init__(self, device):
        """
        Constructor method
        standard address='GPIB0::24::INSTR'
        """
        PyVisaDriver.__init__(self)
        self.name += "Ando AQ4321 laser"
        self.device = device
        self.max_wavelength = 1579.9
        self.min_wavelength = 1520
#
        # self.gpib = res_manager.open_resource(address)
        # self.gpib.write('PASSWORD4321')
#
        # self.gpib.write('INIT')
        # self.gpib.write ('IDN?')
        # info = self.gpib.read()
        # print ('Connection Successful: %s' % info)

        # self.gpib.write ('LOCK?')
        # info = self.gpib.read()
        # print('Locked: %s' %info)
#
        # #Ensure Output is OFF
        # self.gpib.write ('L0')
#
        # #Check Output Status
        # time.sleep(0.55)
        # self.gpib.write ('L?')
        # info = self.gpib.read()
        # print('Output: %s' %info

    def run_get_max_wavelength(self):
        """
        Queries the maximum allowed wavelength

        :returns: Integer
        """
        return self.max_wavelength

    def run_get_min_wavelength(self):
        """
        Queries the minimum allowed wavelength

        :returns: Integer
        """
        return self.min_wavelength

    def run_set_wavelength(self, wavelength):
        """
        Loads a single wavelength and sets output high

        :param wavelength: Specified wavelength
        :type wavelength: Integer
        """
        self.run_output_off()

        if wavelength < 1520 or wavelength > 1620:
            print ('Specified Wavelength Out of Range')
        else:
            # Execute setting of wavelength
            self.device.write('TWL ' + str(wavelength))
            time.sleep(0.55)
            self.device.write('TWL?')
            info = self.device.read()
            print ('Wavelength Sent: %s' % info)

            self.device.write('L1')

            # High for test period
            while self.run_check_status_single() is False:
                time.sleep(0.1)
                # Print if successful
            print('Single Wavelength Complete')

    def run_sweep_wavelengths_step(self, start, end, step):
        """
        Executes a sweep with respect to a specified step

        :param start: Specified wavelength between 1520-1580
        :type start: Integer
        :param end: Specified wavelength between 1520-1580
        :type end: Integer
        :param step: Specified step must be greater or equal to than 0.001
        :type step: Float
        """
        self.run_output_off()

        if (
            float(start) < 1520 or
            float(start) > 1580 or
            float(end) < 1520 or
            float(end) > 1580 or
            float(step) < 0.001
        ):
            print ('Start '+str(float(start))+' End '+str(float(end)))
            print ('Specified Wavelengths Out of Range, or Step Too Low')

        else:
            self.device.write('TSWM 0')
            self.device.write('TSTAWL ' + str(start))
            self.device.write('TSTPWL ' + str(end))
            self.device.write('TSTEWL ' + str(step))
            self.device.write('TSTET 0.2')    # Time between each step
            self.device.write('L1')
            self.device.write('TSGL')         # Step Sweep

            # Wait for reception
            while self.run_check_status() is False:
                pass

            # Print when successful
            print ('Sweep Wavelength Step Complete')

    def run_sweep_wavelengths_continuous(self, start, end, step):
        """
        Executes a sweep with respect to a specified time

        :param start: Specified wavelength between 1520-1580
        :type start: Integer
        :param end: Specified wavelength between 1520-1580
        :type end: Integer
        :param step: Specified time
        :type step: Float
        """

        self.run_output_off()

        if start < 1520 or start > 1580 or end < 1520 or end > 1580:
            print ('Specified Wavelengths Out of Range')

        else:
            self.device.write('TSWM 1')
            self.device.write('TSTAWL ' + str(start))
            self.device.write('TSTPWL ' + str(end))
            self.device.write('TSWET ' + str(step))
            self.device.write('L1')
            self.device.write('TSGL')  # Single Sweep

            while self.run_check_status() is False:
                pass
            print ('Sweep Wavelength Continuous Complete')

    def run_sweep_wavelengths_trigger_setup(self, start, end, step):
        """
        Have to keep track of Triggers in main command, use Stop Sweep Command to end sweep.
        Extra triggers do not make the laser sweep outside of specified end wavelength.
        Remember to shut off laser after sweep ends

        :param start: Specified wavelength between 1520-1580
        :type start: Integer
        :param end: Specified wavelength between 1520-1580
        :type end: Integer
        :param step: Specified time
        :type step: Float
        """

        self.run_output_off()
        self.run_stop_sweep()

        if (
            float(start) < 1520 or
            float(start) > 1580 or
            float(end) < 1520 or
            float(end) > 1580 or
            float(step) < 0.001
        ):
            print ('Specified Wavelengths Out of Range, or Step Too Low')

        else:
            self.device.write('TSWM 2')
            self.device.write('TSTAWL ' + str(start))
            self.device.write('TSTPWL ' + str(end))
            self.device.write('TSTEWL ' + str(step))
            self.device.write('L1')
            self.device.write('TSGL')  # Single Sweep
            time.sleep(4)
            print ('Trigger Setup Complete')

    def trigger(self):
        """Triggers laser"""

        time.sleep(0.4)
        self.device.write('TRIG')
        time.sleep(0.05)

    def run_check_status(self):
        """
        Checks the status of the laser. Handles timeout exception

        :returns: Boolean
        """

        try:
            self.device.write('SRQ3?')
            status = int(self.device.read())
            print('Status: %d' % status)
            if status > 0:
                return True
            else:
                return False
        except pyvisa.errors.VisaIOError:
            time.sleep(0.2)
            return self.run_check_status()

    def run_check_status_single(self):
        """
        Checks the status of the laser. Handles timeout exception

        :returns: Boolean
        """

        try:
            self.device.write('SRQ0?')
            status = int(self.device.read())
            if status > 0:
                return True
            else:
                return False
        except pyvisa.errors.VisaIOError:
            time.sleep(0.2)
            return self.run_check_status()

    def run_manual_step(self, step):
        """
        Use if want to manually step by a particular size, in con-junction with Send Single Wavelength

        :param step: specified step increment, but be greater than or equal to 0.001
        :type step: Float
        """

        if step < 0.001:
                print('Step size cannot be lower than 0.001')
        else:
            self.device.write('TSTEWL ' + str(step))
            self.device.write('TWLUP')

    def run_stop_sweep(self):
        """
        Stop sweep
        """
        self.device.write('TSTP')

    def run_pause_sweep(self):
        """
        Suspend sweep
        """
        self.device.write('TPAS')

    def run_resume_sweep(self):
        """
        Use after pause to resume, still have to call trigger() for next data point if using with trigger sweep
        """
        self.device.write('TCONT')

    def run_output_off(self):
        """
        Turns output of laser source OFF

        .. note:: Output occasionally doesn't turn off unless turned ON beforehand
        """
        self.device.write('L0')

    def run_get_wavelength(self):
        """
        Queries wavelength of the laser

        :returns: Float
        """
        self.device.write('TWL?')
        return float(self.device.read())

    def run_set_power(self, power=0):
        """
        Sets power in dbm

        :param power: Specified power to set the laser to in dbm
        :type power: Integer
        """
        self.device.write('TPDB ' + str(power))

    def run_get_power(self):
        """
        Gets output power in dbm

        :returns: Float
        """
        self.device.write('TPDB?')
        return float(self.device.read())


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
