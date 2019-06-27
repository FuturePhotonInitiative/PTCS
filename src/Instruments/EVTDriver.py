# The base level abstract class for a driver used in this EVT project

import re
import inspect
import abc


class EVTDriver:

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.device = None  # your driver should set self.device after calling the super class constructor(s)
        self.name = ""

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
        return [method[0] for method in inspect.getmembers(self, inspect.ismethod) if re.match('^[^_].+', method[0])]
