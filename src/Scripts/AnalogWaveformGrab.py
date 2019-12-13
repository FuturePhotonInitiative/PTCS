# -*- coding: utf-8 -*-

import sys
import visa # PyVisa info @ http://PyVisa.readthedocs.io/en/stable/
import time
import struct
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

## Keysight IO Libraries 17.1.19xxx was used.
## Anaconda Python 2.7.7 64 bit is used and recommended
## PyVisa 1.8 is used
## Windows 7 Enterprise, 64 bit (has implications for time.clock if ported to unix type machine, use time.time instead)
## HiSlip and Socket connections not supported

## DESCRIPTION OF FUNCTIONALITY
"""In general, this script shows how to pull the waveform data from the analog channels for already acquired data, and save it to a computer.
More specifically, it shows how to determine which channels are on and have data, how much data, get the data into an array, scale data for each channel,
and save/recall it to/from disk in both csv and Python numpy formats.  Methods for getting ALL or just some data are shown in addenda.
This script shows a "brute force" method.  Another similar script shows an "elegant" method."""

## INSTRCUTIONS:
## Edit in the VISA address of the oscilloscope
## Edit in the file save locations ## IMPORTANT NOTE:  This script WILL overwrite previously saved files!
## Manually (or write more code) acquire data on the oscilloscope.  Ensure that it finished (Run/Stop button is red).

    ## None of these scopes offer more than 8,000,000 points
    ## Setting this to 8000000 or more will ensure that the maximum number of available points is retrieved, though often less will come back.
    ## Average and High Resolution acquisition types have shallow memory depth, and thus acquiring waveforms in Normal acq. type and post processing for High Res. or repeated acqs. for Average is suggested if more points are desired.
    ## Asking for zero (0) points, a negative number of points, fewer than 100 points, or a non-integer number of points (100.1 -> error, but 100. or 100.0 is ok) will result in an error, specifically -222,"Data out of range"

## Initialization constants
SCOPE_VISA_ADDRESS = "USB0::0x0957::0x1745::MY48260511::0::INSTR" # Get this from Keysight IO Libraries Connection Expert
GLOBAL_TOUT = 1000 # IO time out in milliseconds

## Save Locations - will overwrite
BASE_FILE_NAME = "my_data"
BASE_DIRECTORY = "C:\\Users\\Public\\"
USER_REQUESTED_POINTS = 1000

##############################################################################################################################################################################
##############################################################################################################################################################################
## Main code
##############################################################################################################################################################################
##############################################################################################################################################################################

sys.stdout.write("Script is running.  This may take a while...")

##############################################################################################################################################################################
##############################################################################################################################################################################
## Connect and initialize scope
##############################################################################################################################################################################
##############################################################################################################################################################################

## Define VISA Resource Manager & Install directory
## This directory will need to be changed if VISA was installed somewhere else.
rm = visa.ResourceManager('C:\\Windows\\System32\\visa32.dll') # This uses PyVisa; PyVisa info @ http://PyVisa.readthedocs.io/en/stable/
## This is more or less ok too: rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')
## In fact, it is generally not needed to call it explicitly: rm = visa.ResourceManager()

## Open Connection
## Define & open the scope by the VISA address ; # This uses PyVisa
try:
    KsInfiniiVisionX = rm.open_resource(SCOPE_VISA_ADDRESS)
except Exception:
    print "Unable to connect to oscilloscope at " + str(SCOPE_VISA_ADDRESS) + ". Aborting script.\n"
    sys.exit()

## Set Global Timeout
## This can be used wherever, but local timeouts are used for Arming, Triggering, and Finishing the acquisition... Thus it mostly handles IO timeouts
KsInfiniiVisionX.timeout = GLOBAL_TOUT

## Clear the instrument bus
KsInfiniiVisionX.clear()

## DO NOT RESET THE SCOPE! - since that would wipe out data...

## Data should already be acquired and scope should be STOPPED (Run/Stop button is red).

## Brute Force method
##
##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################

##########################################################
##########################################################
## Determine Which channels are on AND have acquired data - Scope should have already acquired data and be in a stopped state (Run/Stop button is red).

#########################################
## Get Number of analog channels on scope
IDN = str(KsInfiniiVisionX.query("*IDN?"))
## Parse IDN
IDN = IDN.split(',') # IDN parts are separated by commas, so parse on the commas
MODEL = IDN[1]
if list(MODEL[1]) == "9": # This is the test for the PXIe scope, M942xA)
    NUMBER_ANALOG_CHS = 2
else:
    NUMBER_ANALOG_CHS = int(MODEL[len(MODEL)-2])
NUMBER_CHANNELS_ON = 0

#########################################
## Actually find which channels are on, have acquired data, and get the pre-amble info if needed.
## The assumption here is that, if the channel is off, even if it has data behind it, data will not be retrieved from it.
## Note that this only has to be done once for repetitive acquisitions if the channel scales (and on/off) are not changed.

KsInfiniiVisionX.write(":WAVeform:POINts:MODE MAX") # MAX mode works for all acquisition types, so this is done here to avoid Acq. Type vs points mode problems. Adjusted later for specific acquisition types.
## Channel 1
On_Off = int(KsInfiniiVisionX.query(":CHANnel1:DISPlay?")) # Is the channel displayed? If not, don't pull.
if On_Off == 1:
    Channel_Acquired = int(KsInfiniiVisionX.query(":WAVeform:SOURce CHANnel1;:WAVeform:POINts?"))  # The scope can acquire waveform data even if the channel is off (in some cases) - so modify as needed
        ## If this returns a zero, then this channel did not capture data and thus there are no points
        ## Note that setting the :WAV:SOUR to some channel has the effect of turning it on
else:
    Channel_Acquired = 0
if Channel_Acquired == 0:
    CHAN1_STATE = 0
    KsInfiniiVisionX.write(":CHANnel1:DISPlay OFF") # Setting a channel to be a waveform source turns it on... so if here, turn it off.
    NUMBER_CHANNELS_ON += 0
else:
    CHAN1_STATE = 1
    NUMBER_CHANNELS_ON += 1
    if NUMBER_CHANNELS_ON == 1:
        FIRST_CHANNEL_ON = 1
    LAST_CHANNEL_ON = 1
    Pre = KsInfiniiVisionX.query(":WAVeform:SOURce CHANnel1;:WAVeform:PREamble?").split(',')
    Y_INCrement_Ch1 = float(Pre[7]) # Voltage difference between data points; Could also be found with :WAVeform:YINCrement? after setting :WAVeform:SOURce
    Y_ORIGin_Ch1    = float(Pre[8]) # Voltage at center screen; Could also be found with :WAVeform:YORigin? after setting :WAVeform:SOURce
    Y_REFerence_Ch1 = float(Pre[9]) # Specifies the data point where y-origin occurs, always zero; Could also be found with :WAVeform:YREFerence? after setting :WAVeform:SOURce
        ## The programmer's guide has a very good description of this, under the info on :WAVeform:PREamble.
    ## In most cases this will need to be done for each channel as the vertical scale and offset will differ. However,
        ## if the vertical scales and offset are identical, the values for one channel can be used for the others.
        ## For math waveforms, this should always be done.

## Channel 2
On_Off = int(KsInfiniiVisionX.query(":CHANnel2:DISPlay?"))
if On_Off == 1:
    Channel_Acquired = int(KsInfiniiVisionX.query(":WAVeform:SOURce CHANnel2;:WAVeform:POINts?"))
else:
    Channel_Acquired = 0
if Channel_Acquired == 0:
    CHAN2_STATE = 0
    KsInfiniiVisionX.write(":CHANnel2:DISPlay OFF")
    NUMBER_CHANNELS_ON += 0
else:
    CHAN2_STATE = 1
    NUMBER_CHANNELS_ON += 1
    if NUMBER_CHANNELS_ON == 1:
        FIRST_CHANNEL_ON = 2
    LAST_CHANNEL_ON = 2
    Pre = KsInfiniiVisionX.query(":WAVeform:SOURce CHANnel2;:WAVeform:PREamble?").split(',')
    Y_INCrement_Ch2 = float(Pre[7])
    Y_ORIGin_Ch2    = float(Pre[8])
    Y_REFerence_Ch2 = float(Pre[9])

if NUMBER_ANALOG_CHS == 4: # Only check channels 3 & 4 if it is a 4 channel scope
    ## Channel 3
    On_Off = int(KsInfiniiVisionX.query(":CHANnel3:DISPlay?"))
    if On_Off == 1:
        Channel_Acquired = int(KsInfiniiVisionX.query(":WAVeform:SOURce CHANnel3;:WAVeform:POINts?"))
    else:
        Channel_Acquired = 0
    if Channel_Acquired == 0:
        CHAN3_STATE = 0
        KsInfiniiVisionX.write(":CHANnel3:DISPlay OFF")
        NUMBER_CHANNELS_ON += 0
    else:
        CHAN3_STATE = 1
        NUMBER_CHANNELS_ON += 1
        if NUMBER_CHANNELS_ON == 1:
            FIRST_CHANNEL_ON = 3
        LAST_CHANNEL_ON = 3
        Pre = KsInfiniiVisionX.query(":WAVeform:SOURce CHANnel3;:WAVeform:PREamble?").split(',')
        Y_INCrement_Ch3 = float(Pre[7])
        Y_ORIGin_Ch3    = float(Pre[8])
        Y_REFerence_Ch3 = float(Pre[9])

    ## Channel 4
    On_Off = int(KsInfiniiVisionX.query(":CHANnel4:DISPlay?"))
    if On_Off == 1:
        Channel_Acquired = int(KsInfiniiVisionX.query(":WAVeform:SOURce CHANnel3;:WAVeform:POINts?"))
    else:
        Channel_Acquired = 0
    if Channel_Acquired == 0:
        CHAN4_STATE = 0
        KsInfiniiVisionX.write(":CHANnel4:DISPlay OFF")
        NUMBER_CHANNELS_ON += 0
    else:
        CHAN4_STATE = 1
        NUMBER_CHANNELS_ON += 1
        if NUMBER_CHANNELS_ON == 1:
            FIRST_CHANNEL_ON = 4
        LAST_CHANNEL_ON = 4
        Pre = KsInfiniiVisionX.query(":WAVeform:SOURce CHANnel4;:WAVeform:PREamble?").split(',')
        Y_INCrement_Ch4 = float(Pre[7])
        Y_ORIGin_Ch4    = float(Pre[8])
        Y_REFerence_Ch4 = float(Pre[9])
else: # 2 channel scope:
    CHAN3_STATE = 0
    CHAN4_STATE = 0

if NUMBER_CHANNELS_ON == 0:
    KsInfiniiVisionX.clear()
    KsInfiniiVisionX.close()
    sys.exit("No data has been acquired. Properly closing scope and aborting script.")

#####################################################

################################################################################################################
## Setup data export - For repetitive acquisitions, this only needs to be done once unless settings are changed

KsInfiniiVisionX.write(":WAVeform:FORMat WORD") # 16 bit word format... or BYTE for 8 bit format - WORD recommended, see more comments below when the data is actually retrieved
    ## WORD format especially  recommended  for Average and High Res. Acq. Types, which can produce more than 8 bits of resolution.
KsInfiniiVisionX.write(":WAVeform:BYTeorder LSBFirst") # Explicitly set this to avoid confusion - only applies to WORD FORMat
KsInfiniiVisionX.write(":WAVeform:UNSigned 0") # Explicitly set this to avoid confusion

#####################################################################################################################################
#####################################################################################################################################
## Set and get points to be retrieved - For repetitive acquisitions, this only needs to be done once unless scope settings are changed
## This is non-trivial, but the below algorithm always works w/o throwing an error, as long as USER_REQUESTED_POINTS is a positive whole number (positive integer)

#########################################################
## Determine Acquisition Type to set points mode properly

ACQ_TYPE = str(KsInfiniiVisionX.query(":ACQuire:TYPE?")).strip("\n")
        ## This can also be done when pulling pre-ambles (pre[1]) or may be known ahead of time, but since the script is supposed to find everything, it is done now.
if ACQ_TYPE == "AVER" or ACQ_TYPE == "HRES": # Don't need to check for both types of mnemonics like this: if ACQ_TYPE == "AVER" or ACQ_TYPE == "AVERage": becasue the scope ALWAYS returns the short form
    POINTS_MODE = "NORMal" # Use for Average and High Resoultion acquisition Types.
        ## If the :WAVeform:POINts:MODE is RAW, and the Acquisition Type is Average, the number of points available is 0. If :WAVeform:POINts:MODE is MAX, it may or may not return 0 points.
        ## If the :WAVeform:POINts:MODE is RAW, and the Acquisition Type is High Resolution, then the effect is (mostly) the same as if the Acq. Type was Normal (no box-car averaging).
        ## Note: if you use :SINGle to acquire the waveform in AVERage Acq. Type, no average is performed, and RAW works. See sample script "InfiniiVision_2_Simple_Synchronization_Methods.py"
else:
    POINTS_MODE = "RAW" # Use for Acq. Type NORMal or PEAK
    ## Note, if using "precision mode" on 5/6/70000s or X6000A, then you must use POINTS_MODE = "NORMal" to get the "precision record."

## Note:
    ## :WAVeform:POINts:MODE RAW corresponds to saving the ASCII XY or Binary data formats to a USB stick on the scope
    ## :WAVeform:POINts:MODE NORMal corresponds to saving the CSV or H5 data formats to a USB stick on the scope

###########################################################################################################
## Find max points for scope as is, ask for desired points, find how many points will actually be returned
    ## KEY POINT: the data must be on screen to be retrieved.  If there is data off-screen, :WAVeform:POINts? will not "see it."
        ## Addendum 1 shows how to properly get all data on screen, but this is never needed for Average and High Resolution Acquisition Types,
        ## since they basically don't use off-screen data; what you see is what you get.

## First, set waveform source to any channel that is known to be on and have points, here the FIRST_CHANNEL_ON - if we don't do this, it could be set to a channel that was off or did not acquire data.
KsInfiniiVisionX.write(":WAVeform:SOURce CHANnel" + str(FIRST_CHANNEL_ON))

## The next line is similar to, but distinct from, the previously sent command ":WAVeform:POINts:MODE MAX".  This next command is one of the most important parts of this script.
KsInfiniiVisionX.write(":WAVeform:POINts MAX") # This command sets the points mode to MAX AND ensures that the maximum # of points to be transferred is set, though they must still be on screen

## Since the ":WAVeform:POINts MAX" command above also changes the :POINts:MODE to MAXimum, which may or may not be a good thing, so change it to what is needed next.
KsInfiniiVisionX.write(":WAVeform:POINts:MODE " + str(POINTS_MODE))
## If measurements are also being made, they are made on the "measurement record."  This record can be accessed by using:
    ## :WAVeform:POINts:MODE NORMal instead of :WAVeform:POINts:MODE RAW
    ## Please refer to the progammer's guide for more details on :WAV:POIN:MODE RAW/NORMal/MAX

## Now find how many points are actually currently available for transfer in the given points mode (must still be on screen)
MAX_CURRENTLY_AVAILABLE_POINTS = int(KsInfiniiVisionX.query(":WAVeform:POINts?")) # This is the max number of points currently available - this is for on screen data only - Will not change channel to channel.
## NOTES:
    ## For getting ALL of the data off of the scope, as opposed to just what is on screen, see Addendum 1
    ## For getting ONLY CERTAIN data points, see Addendum 2
    ## The methods shown in these addenda are combinable
    ## The number of points can change with the number of channels that have acquired data, the Acq. Mode, Acq Type, time scale (they must be on screen to be retrieved),
        ## number of channels on, and the acquisition method (:RUNS/:STOP, :SINGle, :DIGitize), and :WAV:POINts:MODE

## The scope will return a -222,"Data out of range" error if fewer than 100 points are requested, even though it may actually return fewer than 100 points.
if USER_REQUESTED_POINTS < 100:
    USER_REQUESTED_POINTS = 100
## One may also wish to do other tests, such as: is it a whole number (integer)?, is it real? and so forth...

if MAX_CURRENTLY_AVAILABLE_POINTS < 100:
    MAX_CURRENTLY_AVAILABLE_POINTS = 100

if USER_REQUESTED_POINTS > MAX_CURRENTLY_AVAILABLE_POINTS or ACQ_TYPE == "PEAK":
     USER_REQUESTED_POINTS = MAX_CURRENTLY_AVAILABLE_POINTS
     ## Note: for Peak Detect, it is always suggested to transfer the max number of points available so that narrow spikes are not missed.
     ## If the scope is asked for more points than :ACQuire:POINts? (see below) yields, though, not necessarily MAX_CURRENTLY_AVAILABLE_POINTS, it will throw an error, specifically -222,"Data out of range"

## If one wants some other number of points...
## Tell it how many points you want
KsInfiniiVisionX.write(":WAVeform:POINts " + str(USER_REQUESTED_POINTS))

## Then ask how many points it will actually give you, as it may not give you exactly what you want.
NUMBER_OF_POINTS_TO_ACTUALLY_RETRIEVE = int(KsInfiniiVisionX.query(":WAVeform:POINts?"))
## Warn user if points will be less than requested, if desired...
## Note that if less than the max is set, it will stay at that value (or whatever is closest) until it is changed again, even if the time base is changed.
## What does the scope return if less than MAX_CURRENTLY_AVAILABLE_POINTS is returned?
    ## It depends on the :WAVeform:POINts:MODE
    ## If :WAVeform:POINts:MODE is RAW
        ## The scope decimates the data, only returning every Nth point.
        ## The points are NOT re-mapped; the values of the points, both vertical and horizontal, are preserved.
        ## Aliasing, lost pulses and transitions, are very possible when this is done.
    ## If :WAVeform:POINts:MODE is NORMal
        ## The scope re-maps this "measurement record" down to the number of points requested to give the best representation of the waveform for the requested number of points.
        ## This changes both the vertical and horizontal values.
        ## Aliasing, lost pulses and transitions, are definitely possible, though less likely for well displayed waveforms in many, but not all, cases.

## This above method always works w/o errors.  In summary, after an acquisition is complete:
        ## Set POINts to MAX
        ## Set :POINts:MODE as desired/needed
        ## Ask for the number of points available.  This is the MOST the scope can give for current settings/timescale/Acq. Type
        ## Set a different number of points if desired and if less than above
        ## Ask how many points it will actually return, use that

## What about :ACQUIRE:POINTS?
## The Programmers's Guide says:
    ## The :ACQuire:POINts? query returns the number of data points that the
    ## hardware will acquire from the input signal. The number of points
    ## acquired is not directly controllable. To set the number of points to be
    ## transferred from the oscilloscope, use the command :WAVeform:POINts. The
    ## :WAVeform:POINts? query will return the number of points available to be
    ## transferred from the oscilloscope.

## It is not a terribly useful query. It basically only gives the max amount of points available for transfer if:
        ## The scope is stopped AND has acquired data the way you want to use it and the waveform is entirely on screen
            ## In other words, if you do a :SINGle, THEN turn on, say digital chs, this will give the wrong answer for digital chs on for the next acquisition.
        ## :POINts:MODE is RAW or MAX - thus it DOES NOT work for Average or High Res. Acq. Types, which need NORMal!
        ## and RUN/STOP vs SINGle vs :DIG makes a difference!
        ## and Acq. Type makes a difference! (it can be misleading for Average or High Res. Acq. Types)
        ## and all of the data is on screen!
        ## Thus it is not too useful here.
## What it is good for is:
    ## 1. determining if there is off screen data, for Normal or Peak Detect Acq. Types, after an acquisition is complete, for the current settings (compare this result with MAX_CURRENTLY_AVAILABLE_POINTS).
    ## 2. finding the max possible points that could possibly be available for Normal or Peak Detect Acq. Types, after an acquisition is complete, for the current settings, if all of the data is on-screen.

#####################################################################################################################################
#####################################################################################################################################
## Get timing pre-amble data and create time axis
## One could just save off the preamble factors and #points and post process this later...

Pre = KsInfiniiVisionX.query(":WAVeform:PREamble?").split(',') # This does need to be set to a channel that is on, but that is already done... e.g. Pre = KsInfiniiVisionX.query(":WAVeform:SOURce CHANnel" + str(FIRST_CHANNEL_ON) + ";PREamble?").split(',')
## While these values can always be used for all analog channels, they need to be retrieved and used separately for math/other waveforms as they will likely be different.
#ACQ_TYPE    = float(Pre[1]) # Gives the scope Acquisition Type; this is already done above in this particular script
X_INCrement = float(Pre[4]) # Time difference between data points; Could also be found with :WAVeform:XINCrement? after setting :WAVeform:SOURce
X_ORIGin    = float(Pre[5]) # Always the first data point in memory; Could also be found with :WAVeform:XORigin? after setting :WAVeform:SOURce
X_REFerence = float(Pre[6]) # Specifies the data point associated with x-origin; The x-reference point is the first point displayed and XREFerence is always 0.; Could also be found with :WAVeform:XREFerence? after setting :WAVeform:SOURce
## This could have been pulled earlier...
del Pre
    ## The programmer's guide has a very good description of this, under the info on :WAVeform:PREamble.
    ## This could also be reasonably be done when pulling the vertical pre-ambles for any channel that is on and acquired data.
    ## This is the same for all channels.
    ## For repetitive acquisitions, it only needs to be done once unless settings change.

DataTime = ((np.linspace(0,NUMBER_OF_POINTS_TO_ACTUALLY_RETRIEVE-1,NUMBER_OF_POINTS_TO_ACTUALLY_RETRIEVE)-X_REFerence)*X_INCrement)+X_ORIGin
if ACQ_TYPE == "PEAK": # This means Peak Detect Acq. Type
    DataTime = np.repeat(DataTime,2)
    ##  The points come out as Low(time1),High(time1),Low(time2),High(time2)....
    ### SEE IMPORTANT NOTE ABOUT PEAK DETECT AT VERY END, specific to fast time scales

###################################################################################################
###################################################################################################
## Determine number of bytes that will actually be transferred and set the "chunk size" accordingly.

    ## When using PyVisa, this is in fact completely unnecessary, but may be needed in other leagues, MATLAB, for example.
    ## However, the benefit in Python is that the transfers can take less time, particularly longer ones.

## Get the waveform format
WFORM = str(KsInfiniiVisionX.query(":WAVeform:FORMat?"))
if WFORM == "BYTE":
    FORMAT_MULTIPLIER = 1
else: #WFORM == "WORD"
    FORMAT_MULTIPLIER = 2

if ACQ_TYPE == "PEAK":
    POINTS_MULTIPLIER = 2 # Recall that Peak Acq. Type basically doubles the number of points.
else:
    POINTS_MULTIPLIER = 1

TOTAL_BYTES_TO_XFER = POINTS_MULTIPLIER * NUMBER_OF_POINTS_TO_ACTUALLY_RETRIEVE * FORMAT_MULTIPLIER + 11
    ## Why + 11?  The IEEE488.2 waveform header for definite length binary blocks (what this will use) consists of 10 bytes.  The default termination character, \n, takes up another byte.
        ## If you are using mutliplr termination characters, adjust accordingly.
    ## Note that Python 2.7 uses ASCII, where all characters are 1 byte.  Python 3.5 uses Unicode, which does not have a set number of bytes per character.

## Set chunk size:
    ## More info @ http://pyvisa.readthedocs.io/en/stable/resources.html
if TOTAL_BYTES_TO_XFER >= 400000:
    KsInfiniiVisionX.chunk_size = TOTAL_BYTES_TO_XFER
## else:
    ## use default size, which is 20480

## Any given user may want to tweak this for best throughput, if desired.  The 400,000 was chosen after testing various chunk sizes over various transfer sizes, over USB,
    ## and determined to be the best, or at least simplest, cutoff.  When the transfers are smaller, the intrinsic "latencies" seem to dominate, and the default chunk size works fine.

## How does the default chuck size work?
    ## It just pulls the data repeatedly and sequentially (in series) until the termination character is found...

## Do I need to adjust the timeout for a larger chunk sizes, where it will pull up to an entire 8,000,000 sample record in a single IO transaction?
    ## If you use a 10s timeout (10,000 ms in PyVisa), that will be good enough for USB and LAN.
    ## If you are using GPIB, which is slower than LAN or USB, quite possibly, yes.
    ## If you don't want to deal with this, don't set the chunk size, and use a 10 second timeout, and everything will be fine in Python.
        ## When you use the default chunk size, there are repeated IO transactions to pull the total waveform.  It is each individual IO transaction that needs to complete within the timeout.

#####################################################
#####################################################
## Pull waveform data, scale it

now = time.clock() # Only to show how long it takes to transfer and scale the data.
## Channel 1
## If on, pull data
if CHAN1_STATE == 1:
    ## Gets the waveform in 16 bit WORD format
    ## The below method uses an IEEE488.2 compliant definite length binary block transfer invoked by :WAVeform:DATA?.
        ## ASCII transfers are also possible, but MUCH slower.
    Data_Ch1 = np.array(KsInfiniiVisionX.query_binary_values(':WAVeform:SOURce CHANnel1;DATA?', "h", False))
    ## Here, WORD format, LSBF, and signed integers are used (these are the scope settings in this script).  The query_binary_values function must be setup the same (https://docs.python.org/2/library/struct.html#format-characters):
            ## For BYTE format and unsigned, use "b" instead of "h"; b is a signed char; see link from above line
            ## For BYTE format and signed,   use "B" instead of "h"; B is an unsigned char
            ## For WORD format and unsigned, use "h"; h is a short
            ## For WORD format and signed,   use "H" instead of "h"; H is an unsigned short
            ## For MSBFirst use True (Don't use MSBFirst unless that is the computer architecture - most common WinTel are LSBF - see sys.byteorder @ https://docs.python.org/2/library/sys.html)

         ## WORD is more accurate, but slower for long records, say over 100 kPts.
         ## WORD strongly suggested for Average and High Res. Acquisition Types.

        ## query_binary_values() is a PyVisa specific IEEE 488.2 binary block reader.  Most languages have a similar function.
            ## The InfiniiVision and InfiniiVision-X scopes always return a definite length binary block in response to the :WAVeform:DATA? querry
            ## query_binary_values() does also read the termination character, but this is not always the case in other languages (MATLAB, for example)
                ## In that case, another read is needed to read the termination character (or a device clear).
            ## In the case of Keysight VISA (IO Libraries), the default termination character is '\n' but this can be changed, depending on the interface....
                ## For more on termination characters: https://PyVisa.readthedocs.io/en/stable/resources.html#termination-characters

        ## Notice that the waveform source is specified, and the actual data query is concatenated into one line with a semi-colon (;) essentially like this:
            ## :WAVeform:SOURce CHANnel1;DATA?
            ## This makes it "go" a little faster.

        ## When the data is being exported w/ :WAVeform:DATA?, the oscilloscope front panel knobs don't work; they are blocked like :DIGitize, and the actions take effect AFTER the data transfer is complete.
        ## The :WAVeform:DATA? query can be interrupted without an error by doing a device clear: KsInfiniiVisionX.clear()

    ## Scales the waveform
    ## One could just save off the preamble factors and post process this later.
    Data_Ch1 = ((Data_Ch1-Y_REFerence_Ch1)*Y_INCrement_Ch1)+Y_ORIGin_Ch1

## Channel 2
if CHAN2_STATE == 1:
    Data_Ch2 = np.array(KsInfiniiVisionX.query_binary_values(':WAVeform:SOURce CHANnel2;DATA?', "h", False))
    Data_Ch2 = ((Data_Ch2-Y_REFerence_Ch2)*Y_INCrement_Ch2)+Y_ORIGin_Ch2

## Channel 3
if CHAN3_STATE == 1:
    Data_Ch3 = np.array(KsInfiniiVisionX.query_binary_values(':WAVeform:SOURce CHANnel3;DATA?', "h", False))
    Data_Ch3 = ((Data_Ch3-Y_REFerence_Ch3)*Y_INCrement_Ch3)+Y_ORIGin_Ch3

## Channel 4
if CHAN4_STATE == 1:
    Data_Ch4 = np.array(KsInfiniiVisionX.query_binary_values(':WAVeform:SOURce CHANnel4;DATA?', "h", False))
    Data_Ch4 = ((Data_Ch4-Y_REFerence_Ch4)*Y_INCrement_Ch4)+Y_ORIGin_Ch4

## Reset the chunk size back to default if needed.
if TOTAL_BYTES_TO_XFER >= 400000:
    KsInfiniiVisionX.chunk_size = 20480
    ## If you don't do this, and now wanted to do something else... such as ask for a measurement result, and leave the chunk size set to something large,
        ## it can really slow down the script, so set it back to default, which works well.

print "\n\nIt took " + str(time.clock() - now) + " seconds to transfer and scale " + str(NUMBER_CHANNELS_ON) + " channel(s). Each channel had " + str(NUMBER_OF_POINTS_TO_ACTUALLY_RETRIEVE) + " points.\n"
del now

###################################################################
###################################################################
## Done with scope operations - Close Connection to scope properly

KsInfiniiVisionX.clear()
KsInfiniiVisionX.close()

################################################################################################
################################################################################################
## Save waveform data -  really, there are MANY ways to do this, of course
################################################################################################
################################################################################################

## If saving repetitive acquisitions, it may be better to just save off a single time axis file, and not just replicate it w/ every save

########################################################
## As CSV - easy to deal with later, but slow and large
########################################################

## Channel 1
## If on, save data
if CHAN1_STATE == 1:
    ########################################################
    ## As CSV - easy to deal with later, but slow and large
    ########################################################
    header = "Time (s),Channel 1 (V)\n"
    now = time.clock() # Only to show how long it takes to save
    filename = BASE_DIRECTORY + BASE_FILE_NAME + "_Channel1.csv"
    ## Using: with open takes care of a lot of stuff, and no need to explicitly close
    with open(filename, 'w') as filehandle: # w means open for writing; can overwrite
        filehandle.write(header)
        np.savetxt(filehandle, np.vstack((DataTime,Data_Ch1)).T, delimiter=',')
            ## np.vstack basically concatenates the timing info and analog data into one array, but it will be shape (2 rows, NPoints columns),
            ## and typically one wants (NPoints rows,2 columns), and the .T (transpose) at the end takes care of that
    print "It took " + str(time.clock() - now) + " seconds to save 1 channel in csv format."
    del now

    ## Read the csv data back into python with:
    with open(filename, 'r') as filehandle: # r means open for reading
        recalled_brute_force_csv_ch1 = np.loadtxt(filehandle,delimiter=',',skiprows=1) # Skiprows keeps it from pulling the header in

    del filehandle, filename, header
    print 'Channel 1 CSV data has been recalled into "recalled_csv_data".\n'

    ########################################################
    ## As a NUMPY BINARY file - fast and small, but really only good for python - can't use header
    ########################################################
    now = time.clock() # Only to show how long it takes to save
    filename = BASE_DIRECTORY + BASE_FILE_NAME + "_Channel1.npy"
    with open(filename, 'wb') as filehandle: # wb means open for writing in binary; can overwrite
        np.save(filehandle, np.vstack((DataTime,Data_Ch1)).T) # See comment above regarding np.vstack and .T
        ## NOTE, if one were to not use with open, and just do np.save like this:
            ## np.save(filename, np.vstack((DataTime,Data_Ch1)).T)
            ## this method automatically appends a .npy to the file name...
    print "It took " + str(time.clock() - now) + " seconds to save 1 channel in binary format."
    del now

    ## Read the NUMPY BINARY data back into python with:
    with open(filename, 'rb') as filehandle: # rb means open for reading binary
        recalled_brute_force_NPY_ch1 = np.load(filehandle)
    del filename, filehandle
    print 'Channel 1 Binary data has been recalled into "recalled_NPY_data".\n'
    print 'Binary saves are MUCH faster than CSV.\n'

## Repeat as needed...
## Channel 2

if CHAN2_STATE == 1:
    ########################################################
    ## As CSV - easy to deal with later, but slow and large
    ########################################################
    header = "Time (s),Channel 2 (V)\n"
    now = time.clock() # Only to show how long it takes to save
    filename = BASE_DIRECTORY + BASE_FILE_NAME + "_Channel2.csv"
    ## Using: with open takes care of a lot of stuff, and no need to explicitly close
    with open(filename, 'w') as filehandle: # w means open for writing; can overwrite
        filehandle.write(header)
        np.savetxt(filehandle, np.vstack((DataTime,Data_Ch1)).T, delimiter=',')
            ## np.vstack basically concatenates the timing info and analog data into one array, but it will be shape (2 rows, NPoints columns),
            ## and typically one wants (NPoints rows,2 columns), and the .T (transpose) at the end takes care of that
    print "It took " + str(time.clock() - now) + " seconds to save 1 channel in csv format."
    del now

    ## Read the csv data back into python with:
    with open(filename, 'r') as filehandle: # r means open for reading
        recalled_brute_force_csv_ch2 = np.loadtxt(filehandle,delimiter=',',skiprows=1) # Skiprows keeps it from pulling the header in

    del filehandle, filename, header
    print 'Channel 2 CSV data has been recalled into "recalled_csv_data".\n'

    ########################################################
    ## As a NUMPY BINARY file - fast and small, but really only good for python - can't use header
    ########################################################
    now = time.clock() # Only to show how long it takes to save
    filename = BASE_DIRECTORY + BASE_FILE_NAME + "_Channel2.npy"
    with open(filename, 'wb') as filehandle: # wb means open for writing in binary; can overwrite
        np.save(filehandle, np.vstack((DataTime,Data_Ch1)).T) # See comment above regarding np.vstack and .T
        ## NOTE, if one were to not use with open, and just do np.save like this:
            ## np.save(filename, np.vstack((DataTime,Data_Ch1)).T)
            ## this method automatically appends a .npy to the file name...
    print "It took " + str(time.clock() - now) + " seconds to save 1 channel in binary format."
    del now

    ## Read the NUMPY BINARY data back into python with:
    with open(filename, 'rb') as filehandle: # rb means open for reading binary
        recalled_brute_force_NPY_ch2 = np.load(filehandle)
    del filename, filehandle
    print 'Channel 2 Binary data has been recalled into "recalled_NPY_data".\n'
    print 'Binary saves are MUCH faster than CSV.\n'
## Channel 3

if CHAN3_STATE == 1:
    ########################################################
    ## As CSV - easy to deal with later, but slow and large
    ########################################################
    header = "Time (s),Channel 3 (V)\n"
    now = time.clock() # Only to show how long it takes to save
    filename = BASE_DIRECTORY + BASE_FILE_NAME + "_Channel3.csv"
    ## Using: with open takes care of a lot of stuff, and no need to explicitly close
    with open(filename, 'w') as filehandle: # w means open for writing; can overwrite
        filehandle.write(header)
        np.savetxt(filehandle, np.vstack((DataTime,Data_Ch1)).T, delimiter=',')
            ## np.vstack basically concatenates the timing info and analog data into one array, but it will be shape (2 rows, NPoints columns),
            ## and typically one wants (NPoints rows,2 columns), and the .T (transpose) at the end takes care of that
    print "It took " + str(time.clock() - now) + " seconds to save 1 channel in csv format."
    del now

    ## Read the csv data back into python with:
    with open(filename, 'r') as filehandle: # r means open for reading
        recalled_brute_force_csv_ch1 = np.loadtxt(filehandle,delimiter=',',skiprows=1) # Skiprows keeps it from pulling the header in

    del filehandle, filename, header
    print 'Channel 3 CSV data has been recalled into "recalled_csv_data".\n'

    ########################################################
    ## As a NUMPY BINARY file - fast and small, but really only good for python - can't use header
    ########################################################
    now = time.clock() # Only to show how long it takes to save
    filename = BASE_DIRECTORY + BASE_FILE_NAME + "_Channel3.npy"
    with open(filename, 'wb') as filehandle: # wb means open for writing in binary; can overwrite
        np.save(filehandle, np.vstack((DataTime,Data_Ch1)).T) # See comment above regarding np.vstack and .T
        ## NOTE, if one were to not use with open, and just do np.save like this:
            ## np.save(filename, np.vstack((DataTime,Data_Ch1)).T)
            ## this method automatically appends a .npy to the file name...
    print "It took " + str(time.clock() - now) + " seconds to save 1 channel in binary format."
    del now

    ## Read the NUMPY BINARY data back into python with:
    with open(filename, 'rb') as filehandle: # rb means open for reading binary
        recalled_brute_force_NPY_ch3 = np.load(filehandle)
    del filename, filehandle
    print 'Channel 3 Binary data has been recalled into "recalled_NPY_data".\n'
    print 'Binary saves are MUCH faster than CSV.\n'
## Channel 4
if CHAN4_STATE == 1:
    ########################################################
    ## As CSV - easy to deal with later, but slow and large
    ########################################################
    header = "Time (s),Channel 4 (V)\n"
    now = time.clock() # Only to show how long it takes to save
    filename = BASE_DIRECTORY + BASE_FILE_NAME + "_Channel4.csv"
    ## Using: with open takes care of a lot of stuff, and no need to explicitly close
    with open(filename, 'w') as filehandle: # w means open for writing; can overwrite
        filehandle.write(header)
        np.savetxt(filehandle, np.vstack((DataTime,Data_Ch1)).T, delimiter=',')
            ## np.vstack basically concatenates the timing info and analog data into one array, but it will be shape (2 rows, NPoints columns),
            ## and typically one wants (NPoints rows,2 columns), and the .T (transpose) at the end takes care of that
    print "It took " + str(time.clock() - now) + " seconds to save 1 channel in csv format."
    del now

    ## Read the csv data back into python with:
    with open(filename, 'r') as filehandle: # r means open for reading
        recalled_brute_force_csv_ch4 = np.loadtxt(filehandle,delimiter=',',skiprows=1) # Skiprows keeps it from pulling the header in

    del filehandle, filename, header
    print 'Channel 4 CSV data has been recalled into "recalled_csv_data".\n'

    ########################################################
    ## As a NUMPY BINARY file - fast and small, but really only good for python - can't use header
    ########################################################
    now = time.clock() # Only to show how long it takes to save
    filename = BASE_DIRECTORY + BASE_FILE_NAME + "_Channel4.npy"
    with open(filename, 'wb') as filehandle: # wb means open for writing in binary; can overwrite
        np.save(filehandle, np.vstack((DataTime,Data_Ch1)).T) # See comment above regarding np.vstack and .T
        ## NOTE, if one were to not use with open, and just do np.save like this:
            ## np.save(filename, np.vstack((DataTime,Data_Ch1)).T)
            ## this method automatically appends a .npy to the file name...
    print "It took " + str(time.clock() - now) + " seconds to save 1 channel in binary format."
    del now

    ## Read the NUMPY BINARY data back into python with:
    with open(filename, 'rb') as filehandle: # rb means open for reading binary
        recalled_brute_force_NPY_ch1 = np.load(filehandle)
    del filename, filehandle
    print 'Channel 4 Binary data has been recalled into "recalled_NPY_data".\n'
    print 'Binary saves are MUCH faster than CSV.\n'

print 'All done.\n'

##############################################################################################################################################################################
##############################################################################################################################################################################
## Addendum 1, For getting ALL of the data off of the scope, as opposed to just what is on screen
## The methods shown in these addenda are combinable
##############################################################################################################################################################################
##############################################################################################################################################################################

## Only use this method with Normal or Peak Detect Acq. Types. This method IS NOT suitable for Average and High Resolution Acquisition Types, as changing the time scale effectively changes the waveform (after an acq.) for these Acq. Types,
    ## particularly since :WAVeform:POINts:MODE NORMal must be used, which gets "re-mapped" when the time base is changed.

## The InfiniiVision scopes ONLY pull data from what is available on screen. Thus, if data was acquired at a short time scale,
    ## data may be available off screen.  It can easily be brought on screen by setting the time scale to something very large.
    ## However, in certain cases (long time scale initial captures with large positions), the time position and time reference can
    ## cause data to still be off screen, even at maximum timescale (50s/Div).  The below can take care of all of this.

## For any given setup and acquisition method, there may or may not be data off screen. To test, compare :ACQuire:POINts? with MAX_CURRENTLY_AVAILABLE_POINTS:
    ## Points are off-screen if :ACQuire:POINts? > MAX_CURRENTLY_AVAILABLE_POINTS
    ## Again, NOT suitable for Average and High Resolution Acquisition Type.  Only use this method with Normal or Peak Detect Acq. Types.

## This method SHOULD NOT be used for :WAVeform:POINts:MODE NORMAL, use RAW.
    ## NORMAL is the so called measurement record, which is almost always shorter than the RAW record, represents what you see on screen, and will result in an aliased waveform when scrunched up
    ## If the measurement record is desired, don't even bother with this...

## This does not ensure that max memory is actually captured by the scope, only that whatever is captured is fully available.
    ## Refer to the polling_method() in InfiniiVision_2_Simple_Synchronization_Methods.py sample to ensure max memory is actually captured.

### Determine initial time base settings - Do this after data is acquired, but before determining the # of points.
#TimeScale = float(KsInfiniiVisionX.query(":TIMebase:SCALe?"))
#TimePosition = float(KsInfiniiVisionX.query(":TIMebase:POSition?"))
#TimeReference = str(KsInfiniiVisionX.query(":TIMebase:REFerence?")).strip("\n")
#if TimeReference == "CUST":
#    TimePositionPercent = int(KsInfiniiVisionX.query(":TIMebase:POSition:LOCation?"))
#elif TimeReference == "LEFT":
#    TimePositionPercent = 0.1
#elif TimeReference == "CENT":
#    TimePositionPercent = 0.5
#elif TimeReference == "RIGH":
#    TimePositionPercent = 0.9
#
### Bring data on screen for any initial time  base setup. This ensures that all data will be available in any scenario.
#if TimeScale > 20 and TimePosition < 500*(TimePositionPercent-1.0): # This defines the condition under which data is still not on screen at 50s/Div.
#    KsInfiniiVisionX.write(":TIMebase:SCALe 50;POSition " + str(500*(TimePositionPercent-1))) # Ensures all data on screen for above condition.
#else:
#    KsInfiniiVisionX.write(":TIMebase:SCALe 50")
#
### Determine # of points and pre-amble info as per above main script.
### Retrieve and scale waveform data as per above main script.
#
### Reset timebase (if desired/needed)
#if TimeScale > 20 and TimePosition < 500*(TimePositionPercent-1.0):
#    KsInfiniiVisionX.write(":TIMebase:SCALe " + str(TimeScale) + ";POSition " + str(TimePosition))
#else:
#    KsInfiniiVisionX.write(":TIMebase:SCALe " + str(TimeScale))

##############################################################################################################################################################################
##############################################################################################################################################################################
## Addendum 2, For getting ONLY CERTAIN data points
##############################################################################################################################################################################
##############################################################################################################################################################################

## It may sometimes be useful to only grab certain parts of a waveform.  This can be accomplished using the ZOOM window.
## Basically all that is needed is to turn it on, and adjust the width and position to contain only the desired data, and put it where it is needed...
    ## However, it is worth noting that this essentially uses :WAVeform:POINts:MODE NORMal, as opposed to RAW, and it is just as easy to
    ## NOT use the zoom window to the same effect (still need to get new timing, not vertical, pre-ambles in either case)...

#KsInfiniiVisionX.write(":WAVeform:POINts:MODE NORMal") # Set correct points mode for ZOOM window
#KsInfiniiVisionX.write(":TIMebase:MODE WINDow") # Turns zoom window on - do this first
#KsInfiniiVisionX.write(":TIMebase:WINDow:Range 20.00E-06") # Adjust width of window - do this second - this is the total width, not the scale (i.e. it is 10x the scale)
#KsInfiniiVisionX.write(":TIMebase:WINDow:POSition -250E-06") # Moves zoom window left/right - do this third - if it is done in opposite order, the POSition can change when the RANGE is adjusted
#    ## Note, for the ZOOM window, a negative position moves the window to the left, which is opposite the MAIN window behavior
#KsInfiniiVisionX.write(":WAVeform:SOURce CHANnel" + str(FIRST_CHANNEL_ON)) # Set waveform source to some channel that has data. Will not change channel to channel.
#POINTS_ZOOM_1 = int(KsInfiniiVisionX.query(":WAVeform:POINts?")) # Get the number of points available for THIS ZOOM window - all the stuff from the main script for setting and getting the # of points still applies here.
### Get timing pre-amble data for THIS ZOOM window
#Pre = KsInfiniiVisionX.query(":WAVeform:PREamble?").split(',')
#X_INCrement_ZOOM_1 = float(Pre[4])
#X_ORIGin_ZOOM_1    = float(Pre[5])
#X_REFerence_ZOOM_1 = float(Pre[6])
### Note that vertical pre-ambles do not change with this.
#del Pre
### Create time axis for THIS zoom window
#DataTime_ZOOM_1 = ((np.linspace(0,POINTS_ZOOM_1-1,POINTS_ZOOM_1)-X_REFerence_ZOOM_1)*X_INCrement_ZOOM_1)+X_ORIGin_ZOOM_1
#
### Pull and scale data... as per main script
#
### Do a second zoom window to get different data if desired...
#KsInfiniiVisionX.write(":TIMebase:WINDow:Range 50.00E-06")
#KsInfiniiVisionX.write(":TIMebase:WINDow:POSition 100E-06")
#KsInfiniiVisionX.write(":WAVeform:SOURce CHANnel" + str(FIRST_CHANNEL_ON))
### Getting the timing pre-amble for the NEW zoom window...
#POINTS_ZOOM_2 = int(KsInfiniiVisionX.query(":WAVeform:POINts?"))
#Pre = KsInfiniiVisionX.query(":WAVeform:PREamble?").split(',')
#X_INCrement_ZOOM_2 = float(Pre[4])
#X_ORIGin_ZOOM_2    = float(Pre[5])
#X_REFerence_ZOOM_2 = float(Pre[6])
### Note that vertical pre-ambles do not change with this.
#del Pre
### Create time axis for THIS zoom window
#DataTime_ZOOM_2 = ((np.linspace(0,POINTS_ZOOM_2-1,POINTS_ZOOM_2)-X_REFerence_ZOOM_2)*X_INCrement_ZOOM_2)+X_ORIGin_ZOOM_2
#
### Pull and scale data... as per main script
#
### Set time window back to main
#KsInfiniiVisionX.write(":TIMebase:MODE MAIN")
#    ## Note that if the zoom window is turned back on, it will revert to the last zoomed settings it had, not default

##############################################################################################################################################################################
##############################################################################################################################################################################
## IMPORTANT NOTE ABOUT PEAK DETECT - at fast time scales
##############################################################################################################################################################################
##############################################################################################################################################################################

## Peak Detect has no effect at the faster time scales.  Knowing when this happens takes an impossibly large lookup table.  That said, it normally returns twice as many
    ## data points as you request with :WAV:POIN xxxx in the format of
    ## The points come out as Low(time1),High(time1),Low(time2),High(time2)....

## When Peak Detect has no effect:
## For both InfiniiVisionX and InfiniiVision:
    ## The binary block header gives the correct number of bytes, but the Low/High pairs, as described above, repeat, as there are not actual oversamples.  In other words:
    ## First value is Low(time1) = High(time1)
    ## Second value is Low(time1) = High(time1)
    ## Third value is Low(time2) = High(time2)
    ## Fourth value is Low(time2) = High(time2)
    ## One can easily imagine a test for this condition and then change the ACQ_TYPE to NORMal and re-acquire.

## EXCEPT when :WAVeform:POINts:MODe NORMal is used for InfiniiVision, 5/6/7000s:
    ## The values do not repeat, but the binary block header is double what it should be.
    ## Say there are 1000 points, and the :WAV:POIN:FORMat is BYTE.
    ## When Peak Detect mode is working, the binary block header will correctly tell us that there are 2000 bytes available to read.
    ## However, if the time scale is fast enough so that peak has no effect, the binary block header will incorrectly tell us that there are 2000 bytes available to read,
        ## even though there are only 1000 bytes.  One can use the PyVisa read_raw() to handle this, should it be needed.
        ## On the other hand, depending on your needs, it might be best to just wrap the data grab with a try/except block (error handler).
        ## What happens here is that the query_binary_values function figures the number of bytes being transferred, and will try to read them all.
        ## When it gets to the end of the binblock, and there are no more bytes to read, it eventually times out.
        ## We just need to catch that time out, set the acquisition type to normal, and re-acquire.
        ## Of course, the data array should be half full, and one could just use that, but the data needs to be treated as if it were in ACQ_TYPE == NORMal
        ## The try/except block could look something like this:
    ## This is entirely avoidable if :WAVeform:POINts:MODe RAW is used.

#try:
#    myData = np.array(KsInfiniiVisionX.query_binary_values(':WAVeform:SOURce CHANnel' + str(channel_number) + ';DATA?', "h", False))
#except:
#    if ACQ_TYPE == "PEAK":
#         KsInfiniiVisionX.clear()
#         KsInfiniiVisionX.write(":ACQ:TYPE NORMal")
#         sys.stdout.write("Scope acquisition type reset to Normal as Peak Detect has no effect at this current time scale. Please acquire new data.\n")
#    else:
#        sys.stdout.write("Something went wrong.") # This should never happen if this script is followed properly.