from src.Instruments.PyVisaDriver import PyVisaDriver


class CSA8000(PyVisaDriver):
    """
    This class models an Tektronix CSA8000 Communications Signal Analyzer
    """

    def __init__(self, device):
        PyVisaDriver.__init__(self)
        self.name += "Tektronix CSA8000"
        self.device = device

    def get_acquisition_param(self):
        return self.device.query('ACQuire?')

    def set_acquisition_mode(self, sample=True, average=False, envelope=False):
        sample = bool(sample)
        average = bool(average)
        envelope = bool(envelope)

        if (sample ^ average ^ envelope) & ~(sample & average & envelope):
            print("Exactly one parameter needs to be set to True")
            return

        if sample:
            self.device.write('ACQuire:MODe SAMple')
            return

        if average:
            self.device.write('ACQuire:MODe AVERage')
            return

        if envelope:
            self.device.write('ACQuire:MODe ENVElope')
            return

    def set_averaging_num(self, num=16):
        self.device.write('ACQuire:NUMAVg ' + str(num))
        return

    def start_acquisition(self):
        self.device.write('ACQuire:STATE ON')
        self.device.write('ACQuire:STATE RUN')
        return

    def stop_acquisition(self):
        self.device.write('ACQuire:STATE STOP')
        self.device.write('ACQuire:STATE OFF')
        return

    def get_sample_rate(self):
        return self.device.query('HORizontal:MAIn:SCAle?')

    def set_sample_rate(self, scale):
        # self.gpib.write('HORizontal:DISPlayscale:SEConds PERScreen; HORizontal:UNIts S; HORizontal:MAIn:SCAle {:.10E}'.format(scale))
        scale = float(scale)
        self.device.write('HORizontal:MAIn:SCAle {:.10E}'.format(scale))
        return

    def get_mask_paramter(self):
        return self.device.query('MASK?')

    def mask_auto_fit(self):
        self.device.write('MASK:AUTOFit EXECute')
        return

    def mask_auto_size(self):
        self.device.write('MASK:AUTOSEEk EXECute')
        return

    def set_mask_hit_ratio_target(self, ratio):
        if not (1e-8 < float(ratio) < 0.1):
            print("Ratio must be within 1E-8 and 0.1")
            return
        self.device.write('MASK:AUTOSEEk:HITRatio ' + str(float(ratio)))
        return

    def set_mask_hit_count_target(self, count):
        self.device.write('MASK:AUTOSEEk:MASKCount ' + str(int(count)))
        return

    def get_mask_hit_ratio(self):
        return self.device.query('MASK:AUTOSEEk:MEASHitratio?')

    def reset_mask(self):
        self.device.write('MASK:COUNt')
        return

    def get_mask_hit_count(self):
        return self.device.query('MASK:COUNt:TOTal?')

    def set_mask_source(self, source='CH1'):
        self.device.write('MASK:SOUrce ' + source)
        return

    def set_mask_standard(self, standard="NONe"):
        self.device.write('MASK:STANDARD ' + standard)
        return

    def reset_histogram_count(self):
        self.device.write('HIStogram:COUNt')
        return

    def set_histogram_mode(self, horizontal=True, vertical=False):
        horizontal = bool(horizontal)
        vertical = bool(vertical)

        if ~(horizontal ^ vertical):
            print("Exactly one parameter needs to be set to True")
            return

        if horizontal:
            self.device.write('HIStogram:MODe HORizontal')
            return

        if vertical:
            self.device.write('HIStogram:MODe VERtical')
            return

    def set_histogram_source(self, source='CH1'):
        self.device.write('HIStogram:SOUrce ' + source)
        return

    def get_histogram_statistics(self):
        return self.device.query('HIStogram:STATistics?')

    def set_histogram_axis(self, linear=True, log=True):
        linear = bool(linear)
        log = bool(log)

        if ~(linear ^ log):
            print("Exactly one parameter needs to be set to True")
            return

        if linear:
            self.device.write('HIStogram:TYPE LINEAr')
            return

        if log:
            self.device.write('HIStogram:TYPE LOG')
            return

    def select_math_slot(self, num):
        if not (0 < int(num) < 9):
            print("num must be between 1 and 8")
            return
        self.device.write('SELect:MATH' + str(int(num)) + ' ON')
        return

    def set_math_function(self, func_string='C1+C2'):
        self.device.write('MATH<x>:DEFine ' + str(func_string))
        return

    def get_measurement_val(self, meas_type, source='CH1', meas_slot=1):
        meas_slot = int(meas_slot)
        self.device.write('MEASUrement:STATIstics:ENABle ON')
        self.device.write('MEASUrement:MEAS{}:SOUrce1:WFM {}'.format(meas_slot, source))
        self.device.write('MEASUrement:MEAS{}:TYPe {}'.format(meas_slot, meas_type))
        return self.device.query('MEASUrement:MEAS{}:MEAN?'.format(meas_slot))
