# The base level abstract class for a driver used in this EVT project

import re
import inspect


class EVTDriver:

    def __init__(self, device, name):
        self.device = device
        self.name = name

    def __enter__(self):
        # abstract
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        # abstract
        pass

    def check_connected(self):
        # abstract
        pass

    def who_am_i(self):
        # abstract
        pass

    def what_can_i(self):
        methods = []
        for method in inspect.getmembers(self, inspect.ismethod):
            if re.match('^run_.+', method[0]):
                methods.append(method)
        return methods
