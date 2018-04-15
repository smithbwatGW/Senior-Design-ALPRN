# Automatic License Plate Reader and Notification System Instruction Manual
Zach Liebold, Blake Smith, Irene Morchio

This guide is an overview on how to operate the ALPR and Notification System device, as well as how to install any necessary software packages onto your Raspberry Pi. 

The ALPR and Notification System device works automatically upon boot, and will begin taking images and analyzing them for items of interest. Once the GUI has booted, you can verify that the software is running correctly by looking for the flashing square in the top left corner of the GUI - if this is cycling, the program is running successfully. If the software finds a license plate with sufficient confidence, it will then compare that license plate against a database of license plates of interest. Should a match be made here, the GUI will notify the user of the match, and will then require input from the user as to what to do next. The user can either acknowledge the match, or ignore the match and return to normal operation.

In order to work properly, the Raspberry Pi needs a version of Ubuntu Linux installed as its operating system. For testing purposes, Ubuntu Mate was used. 

Once you have a Raspberry Pi with a working version of Ubuntu installed, make sure you have sudo privileges. The following steps will install the OpenALPR software; can be copy and pasted into a script or executed from the command line: 

# Install prerequisites
sudo apt-get install libopencv-dev libtesseract-dev git cmake build-essential libleptonica-dev
sudo apt-get install liblog4cplus-dev libcurl3-dev
# Clone the latest code from GitHub
git clone https://github.com/openalpr/openalpr.git
# Setup the build directory
cd openalpr/src
mkdir build
cd build
# Setup the compile environment
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc ..
# compile the library
make
# Install the binaries/libraries to your local system (prefix is /usr)
sudo make install
# Test the library
wget http://plates.openalpr.com/h786poj.jpg -O lp.jpg
alpr lp.jpg
# For the GUI, you will need to install TKInter: 
sudo apt-get install python
sudo apt-get install python-tk
# Clone this project:
git clone https://github.com/smithbwatGW/Senior-Design-ALPRN.git

Note: This python file can be run as a script, if the first line points properly to your python interpreter.
# To run it at Raspberry Pi startup
To set up the GUI and ALPR service to startup on launch, you will need to do the following to your startup menus: 
Navigate to System>Control Center>Personal>Startup Applications
Add a new Startup Program
Name the Program. We recommend using something like GUI or ALPRN to keep it easy to read
Type the execution line. This should be: ‘python /path/to/gui/script.py’ 
Now your services should start automatically upon startup of your machine!
