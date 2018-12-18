import inspect
import re

import pyvisa


class CSA8000(object):
	methods = []

	def __init__(self, device):
		self.device = device

	def who_am_i(self):
		if self.check_connected():
			return "Tektronix CSA8000 at " + self.device.resource_info[0].alias
		else:
			return "Tektronix CSA8000 DISCONNECTED"

	def what_can_i(self):
		if len(CSA8000.methods) == 0:
			for method in inspect.getmembers(self, inspect.ismethod):
				if re.match('^run_.+', method[0]):
					CSA8000.methods.append(method)
		return CSA8000.methods

	def check_connected(self):
		if not self.device:
			return False
		try:
			return self.device.session is not None
		except pyvisa.errors.InvalidSession:
			self.device = None
			return False

	def run_get_acquisition_param(self):
		return self.device.query('ACQuire?')

	def run_set_acquisition_mode(self, sample=True, average=False, envelope=False):
		sample = bool(sample)
		average = bool(average)
		envelope = bool(envelope)

		if (sample ^ average ^ envelope) & ~(sample & average & envelope):
			print "Exactly one parameter needs to be set to True"
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

	def run_set_averaging_num(self, num=16):
		self.device.write('ACQuire:NUMAVg ' + str(num))
		return

	def run_start_acquisition(self):
		self.device.write('ACQuire:STATE ON')
		self.device.write('ACQuire:STATE RUN')
		return

	def run_stop_acquisition(self):
		self.device.write('ACQuire:STATE STOP')
		self.device.write('ACQuire:STATE OFF')
		return

	def run_get_sample_rate(self):
		return self.device.query('HORizontal:MAIn:SCAle?')

	def run_set_sample_rate(self, scale):
		# self.gpib.write('HORizontal:DISPlayscale:SEConds PERScreen; HORizontal:UNIts S; HORizontal:MAIn:SCAle {:.10E}'.format(scale))
		scale = float(scale)
		self.device.write('HORizontal:MAIn:SCAle {:.10E}'.format(scale))
		return

	def run_get_mask_paramter(self):
		return self.device.query('MASK?')

	def run_mask_auto_fit(self):
		self.device.write('MASK:AUTOFit EXECute')
		return

	def run_mask_auto_size(self):
		self.device.write('MASK:AUTOSEEk EXECute')
		return

	def run_set_mask_hit_ratio_target(self, ratio):
		if not (1e-8 < float(ratio) < 0.1):
			print "Ratio must be within 1E-8 and 0.1"
			return
		self.device.write('MASK:AUTOSEEk:HITRatio ' + str(float(ratio)))
		return

	def run_set_mask_hit_count_target(self, count):
		self.device.write('MASK:AUTOSEEk:MASKCount ' + str(int(count)))
		return

	def run_get_mask_hit_ratio(self):
		return self.device.query('MASK:AUTOSEEk:MEASHitratio?')

	def run_reset_mask(self):
		self.device.write('MASK:COUNt')
		return

	def run_get_mask_hit_count(self):
		return self.device.query('MASK:COUNt:TOTal?')

	def run_set_mask_source(self, source='CH1'):
		self.device.write('MASK:SOUrce ' + source)
		return

	def run_set_mask_standard(self, standard="NONe"):
		self.device.write('MASK:STANDARD ' + standard)
		return

	def run_reset_histogram_count(self):
		self.device.write('HIStogram:COUNt')
		return


	def run_set_histogram_mode(self, horizontal=True, vertical=False):
		horizontal = bool(horizontal)
		vertical = bool(vertical)

		if ~(horizontal ^ vertical):
			print "Exactly one parameter needs to be set to True"
			return

		if horizontal:
			self.device.write('HIStogram:MODe HORizontal')
			return

		if vertical:
			self.device.write('HIStogram:MODe VERtical')
			return

	def run_set_histogram_source(self, source='CH1'):
		self.device.write('HIStogram:SOUrce ' + source)
		return

	def run_get_histogram_statistics(self):
		return self.device.query('HIStogram:STATistics?')

	def run_set_histogram_axis(self, linear=True, log=True):
		linear = bool(linear)
		log = bool(log)

		if ~(linear ^ log):
			print "Exactly one parameter needs to be set to True"
			return

		if linear:
			self.device.write('HIStogram:TYPE LINEAr')
			return

		if log:
			self.device.write('HIStogram:TYPE LOG')
			return

	def run_select_math_slot(self, num):
		if not (0 < int(num) < 9):
			print "num must be between 1 and 8"
			return
		self.device.write('SELect:MATH' + str(int(num)) + ' ON')
		return

	def run_set_math_function(self, func_string='C1+C2'):
		self.device.write('MATH<x>:DEFine ' + str(func_string))
		return

	def run_get_measurement_val(self, meas_type, source='CH1', meas_slot=1):
		meas_slot = int(meas_slot)
		self.device.write('MEASUrement:STATIstics:ENABle ON')
		self.device.write('MEASUrement:MEAS{}:SOUrce1:WFM {}'.format(meas_slot, source))
		self.device.write('MEASUrement:MEAS{}:TYPe {}'.format(meas_slot, meas_type))
		return self.device.query('MEASUrement:MEAS{}:MEAN?'.format(meas_slot))
