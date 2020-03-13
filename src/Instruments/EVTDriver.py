import re
import inspect
import abc


class EVTDriver(metaclass=abc.ABCMeta):
    """
    The base level abstract class for a driver used in this EVT project
    """

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

    def what_can_i(self):
        """
        :return: all the methods that are able to be run by this class and all the classes that extend it that are not
        "python private" (its name does not start with an underscore)
        """
        return [method[0] for method in inspect.getmembers(self, inspect.ismethod) if re.match('^[^_].+', method[0])]
