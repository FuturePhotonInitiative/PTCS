# **P**IC **T**est **C**ontrol **S**oftware

## What is *PTCS* ?
PTCS is a software tool that lets a user create and run tests by remotely connecting to measurement instruments and integrated circuits. 

PTCS is being developed by the Center for Detectors at Rochester Institute of Technology

#### Features of PTCS
* Create, save and load a queue of pre-built tests
* Open result files through the UI
* Build a test through a GUI

#### Where Can I get PTCS?
PTCS is currently available from the [Future Photon Initiative public GitHub repository.](https://github.com/FuturePhotonInitiative/PTCS)

## User Documentation
User facing documentation for the whole EVT project is located in \\hawk\RIDL\internal\projects\EVT\internal documents\Documentation on Hawk
You should read these documents first. 

#### User Guide
EVT6 will guide a user in using all the features of PTCS. This document assumes that all the requirements to run are satisfied.

#### Requirements to Run
See EVT9 for the python version, pip packages, and supported windows versions to run the software

#### Running TCL tests
Currently most use cases for this software have been implemented by writing and auto-generating python scripts. Sometimes it is useful to run a test that communicates with Vivado. Vivado can operate in headless mode by giving it a TCL script. EVT8 has some helpful information about running TCL tests with PTCS

## Developer Documentation

#### Developer documentation directory
All the documentation relating to how the code works and how to modify it is located in \\hawk\RIDL\internal\projects\EVT\internal documents\ProberControl Documentation\PTCS Fall2019. This is pretty much a copy of the folder we (Owen and Mark) used in Summer, but it is cleaned up.
If you have not yet, read and complete everything in the *New Developer Startup Guide* When you have completed this, read through the *Codebase Overview* document. As you read this, it should refer you to every other document in this directory. If it does not, then read those documents anyway. (except all the documents in the *Instrument Connection Documentation* folder. Those are just datasheets for how to connect to the instruments we have in the lab remotely)