import re


# import time


class VCU108(object):

    def __init__(self, device):
        self.device = device
        self._locked = False

    def who_am_i(self):
        if self.check_connected():
            return "VCU108 at " + self.device._resource_name
        else:
            return "VCU108 DISCONNECTED"

    def check_connected(self):
        if not self.device:
            return False

        try:
            self.device.session
            return True
        except:
            self.device = None
            return False

    @staticmethod
    def what_can_i():
        return []

    def run_raw_command(self, command):
        if not self.check_connected():
            return False
        else:
            self.reset_menu()
            return self.device.query(command)

    def run_UART(self):
        if not self.check_connected():
            return False
        else:
            self.reset_menu()
            return self.device.query("1")

    def run_LED(self):
        if not self.check_connected():
            return False
        else:
            self.reset_menu()
            self.device.write("2")
            self.device.clear()
            return "Complete"

    def run_IIC(self):
        if not self.check_connected():
            return False
        else:
            self.reset_menu()
            buf = ""
            self.device.write("3")
            self.device.assert_trigger()
            self.device.wait_for_srq()
            # time.sleep(1)
            count = 0
            readData = False
            # self.device.query(b'3')
            # self.device.clear()
            while True or count > 50:
                line = str(self.device.query("z")).strip()
                print line
                if re.match("Press any key to return to main menu", line):
                    break
                if readData:
                    buf += line + "\n"
                if re.match("3", line):
                    readData = True
                count += 1
            # time.sleep(0.5)
            # self.device.clear()
            return buf

    def run_timer(self):
        if not self.check_connected():
            return False
        else:
            self.reset_menu()
            return self.device.query("5")

    def run_switch(self):
        if not self.check_connected():
            return False
        else:
            self.reset_menu()
            return self.device.query("7")

    def run_HDMI(self):
        if not self.check_connected():
            return False
        else:
            self.reset_menu()
            return self.device.query("8")

    def run_DDR4(self):
        if not self.check_connected():
            return False
        else:
            self.reset_menu()
            return self.device.query("9")

    def run_BRAM(self):
        if not self.check_connected():
            return False
        else:
            self.reset_menu()
            return self.device.query("A")

    def run_button(self):
        if not self.check_connected():
            return False
        else:
            self.reset_menu()
            return self.device.query("B")

    def run_clocking(self):
        if not self.check_connected():
            return False
        else:
            self.reset_menu()
            return self.device.query("C")

    def run_PMOD(self):
        if not self.check_connected():
            return False
        else:
            self.reset_menu()
            return self.device.query("D")

    def run_LVDS(self):
        if not self.check_connected():
            return False
        else:
            self.reset_menu()
            return self.device.query("F")

    def run_sys_mon(self):
        if not self.check_connected():
            return False
        else:
            self.reset_menu()
            return self.device.query("G")

    def run_ethernet(self):
        if not self.check_connected():
            return False
        else:
            self.reset_menu()
            return self.device.query("H")

    def run_exit(self):
        if not self.check_connected():
            return False
        else:
            self._locked = True
            self.reset_menu()
            return self.device.query("0")

    def reset_menu(self):
        if not self.check_connected() or self._locked:
            return False
        else:
            tries = 0
            self.device.query(b'z')
            # self.device.clear()
            while True or tries > 100:
                tries += 1
                response = self.device.read()
                response = str(response).strip()
                print response
                if re.match("0: Exit", response):
                    break
        # self.device.clear()
