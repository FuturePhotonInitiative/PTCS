# Design of SPAE
#### Introduction

###### What is *SPAE* ?
The **S**implified **P**rober for **A**utomated **E**xperimentation project is inspired by the [ProberControl](https://probercontrol.github.io/ProberControl/index.html) project created by Columbia University’s Lightwave Research Laboratory and is being developed by the Center for Detectors at Rochester Institute of Technology.

###### What is a Prober Controller?
In this context, a Prober Controller is a piece of software that can automatically:
* Manipulate hardware
* Collect sensor data
* Analyze collected data
* Produce an output that is human readable and highlights interesting features
* Store the output in a logical manner for future analysis

###### How Does SPAE differ from ProberControl?
While ProberControl focuses on the testing of wafer devices, SPAE places emphasis on package level testing. However, SPAE is flexible enough that wafer testing should be possible in the future if the need arises.

###### Where Can I get SPAE?
SPAE is currently available from the [Future Photon Initiative public GitHub repository.](https://github.com/FuturePhotonInitiative/SPAE)

* * *
#### Anatomy of SPAE
###### Launcher
The SPAE launcher is the entry point for execution and is responsible for initializing experiment prerequisites. This file is called Prober.py and is
executed using a python 2.7 interpreter. The launcher will expect the location of a valid [configuration file](#configs) to be passed as an execution argument but
will prompt the user if one is not specified. Once a valid configuration is loaded, the launcher then stages the [scripts](#experiment). This will ensure that the
experiment procedures are executed in the order specified, including simultaneously if designated. The launcher then attempts to connect to each of
[devices](#instruments) specified. If a device is designated as a VISA resource, the launcher will then check if a default connection address is specified and will
try to connect to that. If a default is not specified or the default cannot be found, the launcher will display a list of the currently connected devices
and ask the user to input the desired address. If a device is not VISA compliant, such as the Agilent16802A logic analyzer, the launcher will ask the user
to input an address without displaying the currently connected devices. The details of this address should be documented in the device driver documentation.
Each device will be added to the [Data Map](#data-map) once initialized. After all the devices have been initialized, the launcher will move any data, if provided, into the
Initial data section of the Data Map for use by experiment procedures. When the data has all been initialized, the launcher will then begin to execute the tasks
that were specified in the configurations experiment. Once all tasks have been completed, the launcher will exit and terminate the program.
###### Configs
Configuration files are the basis of all SPAE experiments. These files are all JSON formatted and have the following structure
<div>
<img src="http://ridl.cfd.rit.edu/images/Prober%20Documentation/Config_Format.jpeg" height="1000" />
<img src="http://ridl.cfd.rit.edu/images/Prober%20Documentation/Example_Config.png" height="1000" />
</div>

Left: Formal definition of configuration file, Right: an example configuration file
To comply with the JSON format, the official ECMA specification is available [here](http://www.ecma-international.org/publications/files/ECMA-ST/ECMA-404.pdf)

###### Instruments
Instruments are a software object that models some external equipment, either physical or virtual. Each of these objects need to follow a few simple design patterns
to ensure proper compatibility with SPAE. SPAE utilizes Object Orient Programming and therefore the instrument must be represented by a class. In addition to OOP, each
instrument also must implement python's [*with*](https://docs.python.org/3/whatsnew/2.6.html#pep-343-the-with-statement) pattern, which requires an `__enter__` method
and an `__exit__` method. Finally, SPAE also expects a few methods used to gather information about a particular device:
* who_am_i
  This method should return a string that contains a reference to the type of device and it's connection status.
* check_connected
  this method should return a Boolean indicating if the device is currently connected
* what_can_i
  this method should return a list of methods in the class that are prepended by the "run_" phrase, for optimal performance this list can be cached for later use
  the following is an example where methods is a static list of the Agilent class
 <img src="http://ridl.cfd.rit.edu/images/Prober%20Documentation/Sample_WCI.png" height="100" />

Any other method that is user exposed, IE not strictly internal, should be prepended by the phrase "run_", this will help the GUI identify options for graphical programming

###### Experiment
The experiment section of the [config file](#configs) is the main logic of the experiment. It defines what needs to be run and when. This can either be python scripts that are executed,
or any other program. If two tasks share the same order they will be executed at the same time.
SPAE will not continue to the next stage until all of the tasks in the current stage are complete.

Scripts are python tasks that can be run by SPAE. These will be passed a data map which contains any data specified in the configuration as well as any data that
a previous stage may have put there. The script can add and manipulate this data map in any way it chooses. The script must have a static top level method name `main` that
takes in one parameter (the data map). If the method returns anything it will be ignored, any data that needs to be passed should be put in the data map.
###### Data Map
The data map stores data as SPAE moves from stage to stage. This is implemented as a Python dict (aka KV pair, hashmap). The data map will always contain a few sections and
the rest is up to the developer of the experiment. All sections of the data map should be treated as read only with the one exception of the data section. This object is
automatically generated by the launcher.

<img src="http://ridl.cfd.rit.edu/images/Prober%20Documentation/Data_Map_Diagram.png" height="500" />
