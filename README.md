# **P**IC **T**est **C**ontrol **S**oftware

## What is *PTCS* ?
PTCS is a software tool that lets a user create and run tests by remotely connecting to measurement instruments and integrated circuits. 

PTCS is being developed by the Center for Detectors at Rochester Institute of Technology

#### Features of PTCS
* Create, save and load a queue of pre-built tests
* Open result files through the UI
* Build a test through a GUI

#### Where Can I get PTCS?
PTCS is currently available from the [Future Photon Initiative public GitHub repository](https://github.com/FuturePhotonInitiative/PTCS).

## User Guide
The user guide for the project is EVT6 located the directory PTCSManuals as well as other useful documentation.
Start by reading EVT6 as it gives an overview of the functionality of the software.

#### Requirements to Run
Reading the above document will point you to EVT9 which details the requirements to run the software. 
You should read this as well. Blackdog in the lab is already set up this way, but if you do not have access to the lab, you need to set up your computer using this document.

#### Running TCL tests
EVT8 has some documentation about creating TCL based tests for the VCU108. Currently most use cases for this software have been 
implemented by writing and auto-generating python scripts. Sometimes it is useful to run a test that communicates with 
Vivado. Vivado can operate in headless mode by giving it a TCL script.

## Developer Documentation
If you are developing this software: after you read the above user guides but before you start reading the developer 
documentation below, you should read the New Developer Startup guide located Hawk's PTCS documentation folder.


#### Main Developer Document
The first developer document you should read is EVT11. It is the document that gives context to and glues all the files in the supporting developer documentation folder together.
