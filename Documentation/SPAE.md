# Design of SPAE
#### Introduction

###### What is *SPAE* ?
The **S**implified **P**rober for **A**utomated **E**xperimentation project is inspired by the [ProberControl](https://probercontrol.github.io/ProberControl/index.html) project created by Columbia Univerity's Lightwave Reasearch Laboratory and is being developed by the Center for Detectors at Rochester Institute of Technology.

###### What is a Prober Controller?
In this context, a Prober Controller is a piece of software that can automatically:
* Manipulate hardware
* Collect sensor data
* Analyze collected data
* Produce an output that is human readable and highlights interesting features
* Store the output in a logical manner for future analysis

###### How Does SPAE differ from ProberControl?
While ProberControl focueses on the testing of wafer devices, SPAE places emphasis on package level testing. However, SPAE is flexible enough that wafer testing should be possible in the future if the need arises.

###### Where Can I get SPAE?
SPAE is currently available from the [Future Photon Initialive public GitHub repository.](https://github.com/FuturePhotonInitiative/SPAE)

* * *
#### Anatomy of SPAE
###### Launcher
The SPAE launcher is the entry point for execution and is responsible for initializing experiment prerequisites. This file is called Prober.py and is
executed using a python 2.7 interpreter. The launcher will expect the location of a valid configuration file to be passed as an execution argument but
will prompt the user if one is not specified. Once a valid configuration is loaded, the launcher then stages the scripts. This will ensure that the
experiment procedures are executed in the order specified, including simultaneously if designated. The launcher then attempts to connect to each of
devices specified. If a device is designated as a VISA resource, the launcher will then check if a default connection address is specified and will
try to connect to that. If a default is not specified or the default cannot be found, the launcher will display a list of the currently connected devices
and ask the user to input the desired address. If a device is not VISA compliant, such as the Agilent16802A logic analyzer, the launcher will ask the user
to input an address without displaying the currently connected devices. The details of this address should be documented in the device driver documentation.
Each device will be added to the Data Map once initialized. After all the devices have been initialized, the launcher will move any data, if provided, into the
Initial data section of the Data Map for use by experiment procedures. When the data has all been initialized, the launcher will then begin to execute the tasks
that were specified in the configurations experiment. Once all tasks have been completed, the launcher will exit and terminate the program.
###### Configs
Configuration files are the basis of all SPAE experiments. These files are all JSON formatted and have the following structure

###### Instruments
###### Scripts
###### Data Map