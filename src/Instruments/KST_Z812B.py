from src.Instruments.KST_ZST import Motor_KST_ZST


class KST_Z812B(Motor_KST_ZST):

    def __init__(self, device):
        Motor_KST_ZST.__init__(self, device)

    def home(self):
        """
        Puts the motor to backward limit position so that the
        position markers make sense
        """

        # variable moving is not necessary
        # self.moving = True
        self.device.write_raw([0x43, 0x04, 0x01, 0x00, 0x50, 0x01])
        response = self.device.read()
        if response != [0x44, 0x04, 0x01, 0x00, 0x01, 0x50]:
            # self.logger.error('problem homing', extra=self.ext)
            # raise error?
            exit()
        #
        # self.logger.info('homed successfully.', extra=self.ext)
        # self.moving = False

    def delta_root(self, degrees):
        if self.deg_pos + degrees > self.STOP_LIMIT or self.deg_pos + degrees < -self.STOP_LIMIT:
            return False
