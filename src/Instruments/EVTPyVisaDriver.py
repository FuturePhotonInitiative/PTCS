"""
A class that contains basic commands that all drivers may want to run
"""

import pyvisa
import inspect
import re


class EVTPyVisaDriver:

    def __init__(self, device, name):
        self.device = device
        self.name = name

    def __enter__(self):
        """
        Enter method for ability to use "with open" statements
        :return: Driver Object
        """
        return self

    def __exit__(self):
        """
        Close the device connection
        :return:
        """
        self.device.close()

    def who_am_i(self):
        if self.check_connected():
            return self.name + " at " + self.device.resource_info[0].alias
        else:
            return self.name + " DISCONNECTED"

    def what_can_i(self):
        methods = []
        for method in inspect.getmembers(self, inspect.ismethod):
            if re.match('^run_.+', method[0]):
                methods.append(method)
        return methods

    def check_connected(self):
        if not self.device:
            return False
        try:
            return self.device.session is not None
        except pyvisa.errors.InvalidSession:
            self.device = None
            return False
