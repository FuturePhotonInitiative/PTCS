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

## User Guide
The user guide for the project is EVT6 located in the EVT project formal documentation folder:
\\hawk\RIDL\internal\projects\EVT\internal documents\Documentation.
Start by reading this document as it gives an overview of the functionality of the software.

#### Requirements to Run
Reading this document will point you to EVT9 which details the requirements to run the software. 
You should read this as well, but you do not need to do anything found in it because Blackdog 
(the computer that is used for PTCS development) is already set up.

#### Running TCL tests
EVT8 has some documentation about creating TCL based tests. Currently most use cases for this software have been 
implemented by writing and auto-generating python scripts. Sometimes it is useful to run a test that communicates with 
Vivado. Vivado can operate in headless mode by giving it a TCL script.

## Developer Documentation
After you read the above user guides but before you start reading the developer documentation below, you should read the New Developer Startup guide
located in the supporting developer documentation folder: 
\\hawk\RIDL\internal\projects\EVT\internal documents\ProberControl Documentation\PTCS Fall2019

#### Main Developer Document
The first developer document you should read is EVT11. It is the document that gives context to and glues all the files in the supporting developer documentation folder together.
The supporting developer documentation folder is pretty much a copy of the folder we (Owen and Mark) used in Summer, but it is cleaned up. Feel free to edit these documents in the folder as the software changes.
If there are any files in EVT11 that are not mentioned (other than the remote instrument communication data sheets) make sure you read over and understand them also.
