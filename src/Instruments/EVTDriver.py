# The base level abstract class for a driver used in this EVT project

import re
import inspect
import abc


class EVTDriver:

    __metaclass__ = abc.ABCMeta

    def __init__(self, device, name):
        self.device = device
        self.name = name

    @abc.abstractmethod
    def __enter__(self):
        pass

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @abc.abstractmethod
    def check_connected(self):
        pass

    @abc.abstractmethod
    def who_am_i(self):
        pass

    def what_can_i(self):
        methods = []
        for method in inspect.getmembers(self, inspect.ismethod):
            if re.match('^run_.+', method[0]):
                methods.append(method)
        return methods
