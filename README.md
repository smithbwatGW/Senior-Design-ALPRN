# Automatic License Plate Reader and Notification System Instruction Manual
Zach Liebold, Blake Smith, Irene Morchio

This guide is an overview on how to operate the ALPR and Notification System device, as well as how to install any necessary software packages onto your Raspberry Pi. 

The ALPR and Notification System device works automatically upon boot, and will begin taking images and analyzing them for items of interest. Once the GUI has booted, you can verify that the software is running correctly by looking for the flashing square in the top left corner of the GUI - if this is cycling, the program is running successfully. If the software finds a license plate with sufficient confidence, it will then compare that license plate against a database of license plates of interest. Should a match be made here, the GUI will notify the user of the match, and will then require input from the user as to what to do next. The user can either acknowledge the match, or ignore the match and return to normal operation.

In order to work properly, the Raspberry Pi needs a version of Ubuntu Linux installed as its operating system. For testing purposes, Ubuntu Mate was used. 

Once you have a Raspberry Pi with a working version of Ubuntu installed, make sure you have sudo privileges. The following steps will install the OpenALPR software; can be copy and pasted into a script or executed from the command line: 

# Install OpenALPR
https://github.com/openalpr/openalpr/wiki/Compilation-instructions-(Ubuntu-Linux)
# For the GUI, you will need to install TKInter: 
sudo apt install python python-tk
# Clone this project:
git clone https://github.com/smithbwatGW/Senior-Design-ALPRN.git

Note: This python file can be run as a script, if the first line points properly to your python interpreter.
# To run it on startup
To set up the GUI and ALPR service to startup on launch, you will need to do the following to your startup menus: 
Navigate to System>Control Center>Personal>Startup Applications
Add a new Startup Program
Name the Program. We recommend using something like GUI or ALPRN to keep it easy to read
Type the execution line. This should be: ‘python /path/to/ALPRN/script.py’ 
Now your services should start automatically upon startup of your machine!
