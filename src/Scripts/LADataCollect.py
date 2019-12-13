
# prints all of the bus/signal's from the
# first module in a 168x/9x/9xx Logic Analysis System.
#
# LAHostNameOrIP -> change to the hostname or IP address of the LA
# you're connecting to (default is 'localhost'
# if you're running Python directly on the LA)
# LAModule -> change to the analyzer name to transfer data from
# (default is the first module)
# LAStartRange, LAEndRange -> change to the data range to upload
# (default is -10 and 10 respectively)
#
# Python version 2.2.3
import sys
import string
# Libraries needed to interface with the Logic Analyzer COM interface.
import win32com.client
from win32com.client import constants
import pythoncom
### ==================================================================
### * Begin Subroutines *
### ------------------------------------------------------------------
##--------------------------------------------------------------------
## FUNCTION:
## PrintArrays -- prints the Logic Analyzer Data Arrays
##
## SYNOPSIS:
##
## ARGUMENTS:
## arrays - array of data arrays to format and print. The
## first array contains the bus/signal names.
##
##--------------------------------------------------------------------
LADataArrays = []

def PrintArrays(arrays):
    NameArray = arrays[0]
    TypeArray = arrays[1]
    DataArrays = arrays[2:]
    DataStringArrays = []
    # Calculate the max width for each column and store in an array.
    MaxWidthArray = []
    for name in NameArray:
        MaxWidthArray.append(len(name))
    for column in range(len(DataArrays)):
        DataStringArray = []
    for dataValue in DataArrays[column]:
        if TypeArray[column] == constants.AgtBusSignalProbed:
            dataValueString = "%X" % dataValue
        elif TypeArray[column] == constants.AgtBusSignalGenerated:
            dataValueString = "%s" % dataValue
        elif TypeArray[column] == constants.AgtBusSignalSampleNum:
            dataValueString = "%d" % dataValue
        elif TypeArray[column] == constants.AgtBusSignalTime:
            dataValueString = "%E" % dataValue

        DataStringArray.append(dataValueString)
        dataValueStringLength = len(dataValueString)
        if dataValueStringLength > MaxWidthArray[column]:
            MaxWidthArray[column] = dataValueStringLength
        DataStringArrays.append(DataStringArray)

    # Print the header row.
    print ""
    for column in range(len(NameArray)):
        print " " + string.center(NameArray[column], \
            MaxWidthArray[column]),
    print ""
    for column in range(len(NameArray)):
        print " " + "-" * MaxWidthArray[column],
    print ""

    # Print the data rows.
    for row in range(len(DataStringArrays[1])):
        for column in range(len(DataStringArrays)):
            print " " + string.rjust(DataStringArrays[column][row], \
                MaxWidthArray[column]),
        print ""
    ### ------------------------------------------------------------------
    ### End of Subroutines
    ### ==================================================================
    ### ==================================================================
    ### * Begin Main Routine *
    ### ------------------------------------------------------------------
    # Logic Analyzer host name or IP address.
    LAHostNameOrIP = "localhost"
    # Create the logic analyzer client server, and
    # connect to the remote logic analyzer instrument.
    print "\nConnecting to '%s'" % LAHostNameOrIP ;
    try:
        LAConnect = win32com.client.Dispatch("AgtLA.Connect")
        LAInst = LAConnect.GetInstrument(LAHostNameOrIP)
    except pythoncom.com_error, (hr, msg, exc, arg):
        print "The AgtLA call failed with code: %d: %s" % (hr, msg)
        if exc is None:
            print "There is no extended error information"
        else:
            wcode, source, text, helpFile, helpId, scode = exc
            print "The source of the error is", source
            print "The error message is", text
            print "More info can be found in %s (id=%d)" % (helpFile, helpId)
        sys.exit(1)
    # Optionally, load a configuration file that exists on the
    # logic analyzer. If the file only exists on your client PC,
    # then use the LAConnect.CopyFile() method to copy the file
    # onto your logic analyzer.
    #
    # LAInst.Open("test.xml")
    # Get the logic analyzer module.
    #
    # LAModule = LAInst.GetModuleByName("My 1691D-1")
    LAModule = LAInst.Modules(0)
    # Optionally, set up a trigger before running the analyzer.
    #
    # if LAModule.Type == "Analyzer":
    # LAAnalyzerModule = \
    # win32com.client.CastTo(LAModule, "IAnalyzerModule")
    # LAAnalyzerModule.SimpleTrigger("My Bus 1=hff")
    # Run the analyzer and wait for the measurement to complete
    # before getting data.
    LAInst.Run()
    LAInst.WaitComplete(10) # Time out after 10 seconds.
    # Get the module's bus/signal names and types, and store
    # into 'LABusSignalNameArray' and 'LABusSignalTypeArray'.
    LABusSignals = LAModule.BusSignals
    LABusSignalsCount = LABusSignals.Count
    LABusSignalNameArray = []
    LABusSignalTypeArray = []

    for index in range(LABusSignalsCount):
        LABusSignalName = LABusSignals.Item(index).Name
        LABusSignalType = LABusSignals.Item(index).BusSignalType
        LABusSignalNameArray.append(LABusSignalName)
        LABusSignalTypeArray.append(LABusSignalType)

    # Get the module's bus/signal data and store into 'LADataArrays'.
    LADataArrays.append(LABusSignalNameArray)
    LADataArrays.append(LABusSignalTypeArray)
    LAStartRange = -10
    LAEndRange = 10

    for index in range(LABusSignalsCount):
        LAData = LABusSignals.Item(index).BusSignalData
        LABusSignalType = LABusSignalTypeArray[index]
        LADataType = constants.AgtDataLong

        if LABusSignalType == constants.AgtBusSignalTime:
            LADataType = constants.AgtDataTime

        if LAData.Type == "Sample":
            SampleBusSignalData = \
                win32com.client.CastTo(LAData, "ISampleBusSignalData")
            (LADataArray, NumRows) = \
                SampleBusSignalData.GetDataBySample(LAStartRange,
                                                    LAEndRange,
                                                    LADataType)
        LADataArrays.append(LADataArray)
#
# Print the Arrays.
#
PrintArrays(LADataArrays)