import time

from src.Instruments.PyVisaDriver import PyVisaDriver


class TSL_210H(PyVisaDriver):
    """
    This class models a Santec TSL-201H Laser
    """

    def __init__(self, device):
        PyVisaDriver.__init__(self)
        self.name += "Santec TSL-201H Laser"
        self.device = device

        self.max_wavelength = 1580
        self.min_wavelength = 1510

        self.active = False
        self.turn_output_on()
        self.locked = True

        self.sweep_start = None
        self.sweep_end = None
        self.sweep_step = None
        self.wavelength = None

    def change_state(self):
        self.active = ~self.active

    def get_max_wavelength(self):
        return self.max_wavelength

    def get_min_wavelength(self):
        return self.min_wavelength

    def set_wavelength(self, wavelength):
        if wavelength > self.max_wavelength or wavelength < self.min_wavelength:
            print 'Wavelength out of range'
        else:
            wavelength = "{0:.3f}".format(float(wavelength))
            self.device.write('WA' + wavelength)
            time.sleep(0.5)
            self.device.write('WA')
            self.wavelength = wavelength
            check = "0.000"
            while check != wavelength:
                while self.device.bytes_in_buffer == 0:
                    time.sleep(0.1)
                check = self.device.read()
        return

    def sweep_setup(self, start, end, step):
        if start < self.min_wavelength or start > self.max_wavelength or \
                end < self.min_wavelength or start > self.max_wavelength:
            print 'Wavelength out of range'
        else:
            self.sweep_start = start
            self.sweep_end = end
            self.sweep_step = step

    def sweep_step(self):
        if self.sweep_end > self.wavelength >= self.sweep_start:
            self.wavelength = float(self.wavelength) + float(self.sweep_step)
            self.set_wavelength(self.wavelength)

    def start_sweep(self):
        if self.sweep_start is None or self.sweep_end is None or self.sweep_step is None:
            print 'Sweep not configured'
        else:
            self.set_wavelength(self.sweep_start)

    def pause_sweep(self):
        """
        Pause sweep
        """
        self.device.write('WA')

    def stop_sweep(self):
        """
        Stop the sweep
        """
        self.turn_output_off()

    def check_status(self):
        """
        Check the status of the instrument

        :returns: Booleans
        """
        #
        # try:
        # 	self.device.write('SU')
        # 	status = int(self.device.read())
        # 	if status > 0:
        # 		return True
        # 	else:
        # 		return False
        # except Exception:
        # 	time.sleep(0.2)
        # 	return self.checkStatus()
        self.device.write('SU')
        for x in range(0, 50, 1):
            if self.device.bytes_in_buffer < 1:
                time.sleep(0.2)
                continue
            return int(self.device.read()) > 0
        return False

    def turn_output_on(self):
        """
        Turns output of laser source ON.
        """
        self.device.write('LO')  # turn on diode

    def turn_output_off(self):
        """
        Turns output of laser source OFF. Output occasionally doesn't turn off unless turned ON beforehand
        """
        self.device.write('LF')  # turn off diode

    def get_wavelength(self):
        """
        Query the current wavelength

        :returns: Float
        """
        # self.gpib.write('WA')
        # return float(self.device.read())
        return float(self.device.query('WA'))

    def set_power(self, power):
        """
        Set power in dbm

        :param power: power specified to set
        :type power: Float
        """
        self.device.write('OP' + str(power))

    def get_power(self):
        """
        Gets output power in dbm

        :returns: Float
        """
        # self.gpib.write('OP')
        # return float(self.gpib.read())
        return float(self.device.query('OP'))

    def set_current(self, current):
        """
        Set the current. Note: current is mA

        :param current: specified current to set
        :type current: Integer
        """
        self.device.write('CU' + str(current))

    def get_current(self):
        """
        Queries the current, Note: current is mA

        :returns: Float
        """
        # self.gpib.write('CU')
        # return float(self.gpib.read())
        return float(self.device.query('CU'))

    def set_temperature(self, temperature):
        """
        Set the temperature. Note: temperature is C

        :param temperature: specified temperature to set
        :type temperature: Integer
        """
        self.device.write('TL' + str(temperature))

    def get_temperature(self):
        """
        Queries the temperature, Note: temperature is C

        :returns: Float
        """
        # self.gpib.write('TL')
        # return float(self.gpib.read())
        return float(self.device.query('TL'))

    def set_ACC(self):
        """
        Sets the ACC
        """
        self.device.write('AO')

    def set_APC(self):
        """
        Sets the APC
        """
        self.device.write('AF')

    def get_status(self):
        """
        Queries the status of the...

        :returns: String
        """
        # self.gpib.write('SU')
        # return self.gpib.read()
        return self.device.query('SU')

    def set_power_mw(self, powermw):
        """
        Sets the powerMW

        :param powermw: specified powerMW to set
        :type powermw: Integer
        """
        self.device.write('LP' + str(powermw))

    def get_power_mw(self):
        """
        Queries the status of the powerMW

        :returns: Float
        """
        # self.gpib.write('LP')
        # return float(self.gpib.read())
        return float(self.device.query('LP'))

    def coherence_on(self):
        """
        Turns coherence ON
        """
        self.device.write('CO')

    def coherence_off(self):
        """
        Turns coherence OFF
        """
        self.device.write('CF')

    def set_coherence(self, coherence):
        """
        Sets the coherence

        :param coherence: Specified coherence
        :type coherence: Integer
        """
        self.device.write('CV' + str(coherence))

    def get_coherence(self):
        """
        Queries the coherence value

        :returns: Float
        """
        # self.gpib.write('CV')
        # return float(self.gpib.read())
        return float(self.device.query('CV'))
