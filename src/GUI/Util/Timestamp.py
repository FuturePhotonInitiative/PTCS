import datetime
from src.GUI.Util.CONSTANTS import TIMESTAMP_FORMAT

FORMAT_FOR_FILE_NAME = "_y%Y_m%m_d%d_h%H_m%M_s%S_us%f"


class Timestamp:

    def __init__(self):
        self._stamp = datetime.datetime.today()

    @classmethod
    def from_str(cls, timestamp: str):
        instance = Timestamp()
        instance._stamp = datetime.datetime.strptime(timestamp, TIMESTAMP_FORMAT)
        return instance

    def for_filename(self) -> str:
        return self._stamp.strftime(FORMAT_FOR_FILE_NAME)

    def __str__(self):
        return self._stamp.strftime(TIMESTAMP_FORMAT)
