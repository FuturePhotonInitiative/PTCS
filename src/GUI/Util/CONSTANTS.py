import wx
import os

MAIN_PAGE_TITLE = "PIC Test Control Software"
PAGE_SIZE = (900, 500)
QUEUE_PAGE_NAME = "Queue"
HARDWARE_PAGE_NAME = "Hardware"
BUILD_EXPERIMENTS_PAGE_NAME = "Build"
RESULTS_PAGE_NAME = "Results"
SPACE_SIZE = 4

QUEUE_PANEL_PROPORTION = 1
QUEUE_CONTROL_PANEL_PROPORTION = 2

HARDWARE_PANEL_PROPORTION = 1
HARDWARE_CONTROL_PANEL_PROPORTION = 1

BUILD_PANEL_PROPORTION = 3
BUILD_SCRIPT_PANEL_PROPORTION = 1

RESULTS_EXPERIMENT_PANEL_PROPORTION = 1
RESULTS_FILE_PANEL_PROPORTION = 1

LIST_PANEL_COLOR = wx.Colour(50, 50, 50)
LIST_PANEL_FOREGROUND_COLOR = wx.WHITE#wx.Colour(100, 100, 100)

CONTROL_PANEL_COLOR = wx.WHITE
CONTROL_PANEL_FOREGROUND_COLOR = wx.BLACK#wx.Colour(100, 100, 100)

LABEL_PROPORTION = .1

# directories of interest
PROJ_DIR = os.path.dirname(os.path.dirname(os.getcwd()))
WORKING_DIRECTORY = os.path.join(PROJ_DIR, "System")
CONFIGS = os.path.join(PROJ_DIR, "Configs")
SCRIPTS_DIR = os.path.join(os.path.join(PROJ_DIR, "src"), "Scripts")
DRIVERS_DIR = os.path.join(os.path.join(PROJ_DIR, "src"), "Instruments")
RESULTS_DIR = os.path.join(PROJ_DIR, "Results")
DEVICES_CONFIG = os.path.join(os.path.join(PROJ_DIR, "System"), "Devices.json")
RESULTS_CONFIG_DIR = os.path.join(os.path.join(PROJ_DIR, "System"), "ResultsConfiguration")

EXPERIMENT_QUEUE_RESULT_ROOT = "Experiment Queues"

QUEUE_FILE_TITLE = "queue_result"

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
