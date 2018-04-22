#!/usr/bin/python
import Tkinter
import threading
from threading import Thread
from openalpr import Alpr
from picamera import PiCamera
import time
import sys
import csv

# Global variables
screenblink = [0]
foundmatch = [0]
foundindex = [0]
foundplate = ['None']
alprwake = threading.Condition()
lastseenlock = threading.Condition()

# Database and its field references
dBase = []
# XXX: If new fields to be added to the database, add here
fields = ['plate', 'state', 'ROI','color','make','model']
platestatus = ['Unknown','Stolen','Missing Person','Amber alert']


def dBase_fill():
    with open('database.csv','rb') as csvfile:
        dline = csv.DictReader(csvfile,fieldnames=fields)
        for row in dline:
            # This implementation allows easier legibility when referencing entry values
            dBase.append({fields[0]:row[fields[0]],fields[1]:row[fields[1]],fields[2]:row[fields[2]],fields[3]:row[fields[3]],fields[4]:row[fields[4]],fields[5]:row[fields[5]]})

    # Trims the first two entries, may or may not be necessary depending on file
    for i in range(2):
        dBase.remove(dBase[0])
        
def Alpr_run():
    #camera = PiCamera()
    #camera.resolution = (1920,1080)
    
    # TODO: change these depending on platform
    #alpr = Alpr("us","/home/zib/Senior-Design-ALPR/src/build/config/openalpr.conf","/home/zib/Senior-Design-ALPR/runtime_data")
    alpr = Alpr("us","/home/smith/workspace/openalpr/src/build/config/openalpr.conf","/home/smith/workspace/openalpr/runtime_data")
    if not alpr.is_loaded():
        print("Error loading OpenALPR")
        foundmatch[0] = 7
        sys.exit(1)
        
    alpr.set_top_n(10)
            
    try:
        while True:
            #camera.capture('/home/zib/plates/image.jpg',format='jpeg',quality=100)
            #results = alpr.recognize_file("/home/zib/plates/image.jpg")
            results = alpr.recognize_file("ETALLIC.jpg")
            if foundmatch[0] == 8:
                    alpr.unload()
                    #print "Thead exitted"
                    sys.exit()
            for plate in results['results']:
                if foundmatch[0] == 8:
                    alpr.unload()
                    #print "Thead exitted"
                    sys.exit()
                for candidate in plate['candidates']:
                    if candidate['confidence'] >= 85:
                        lastseenlock.acquire()
                        foundplate[0] = time.strftime("%X",time.localtime(time.time()))+' Plate: '+candidate['plate']
                        lastseenlock.release()
                        # hit_index will be used by the gui to fill in the desired info for display when a match occurs
                        # May or may not be useful if separate processes between gui and this
                        hit_index=0
                        for entry in dBase:
                            if candidate['plate'] == entry['plate']:
                                # XXX: Location to add logging, like copy picture, or add to a log file
                                #Conditional works as both a lock and the signal to wake the thread back up
                                alprwake.acquire()
                                foundmatch[0] = 1
                                foundindex[0] = hit_index
                                alprwake.wait() #Sleeps till notified
                                alprwake.release()
                                break
                            else:
                                hit_index+=1
                    if foundmatch[0] == 8:
                        alpr.unload()
                        #print "Thead exitted"
                        sys.exit()
        alpr.unload()
        #print "Thead exitted"
    except KeyboardInterrupt:
        alprwake.acquire()
        foundmatch[0] = 7
        alprwake.release()
        alpr.unload()
        #print "Thread exitted"
        sys.exit()

def ch_arr_variable(var,elem,value):
    var[elem] = value;

def ch_color(blinky):
    current_color = blinky.cget("background")
    next_color = "white" if current_color == "black" else "black"
    blinky.config(background=next_color)

def change_color(blinky,window,delay,enable):
    if (enable[0] == 1):
        ch_color(blinky)        
    window.after(delay, change_color, blinky, window, delay, enable)

def clear_buttoncall(window,notes):
    alprwake.acquire()
    screenblink[0] = 0
    notes.place_forget()
    window.config(background="light grey")
    alprwake.notify_all()
    alprwake.release()
    
def acknowledge_buttoncall(window):
    screenblink[0] = 0
    window.config(background="light grey")

def exit_buttoncall(thread,window):
    #TODO: Include any other application close out here (Ex: alpr agent close, etc)
    #print "Exit called!"
    alprwake.acquire()
    foundmatch[0] = 8
    alprwake.notify_all()
    alprwake.release()
    #print "Thread told to exit"
    thread.join()
    #print "Thread joined"
    window.destroy()
    #print "window destroyed"
    sys.exit()

def main():
    try:
        # Instantiates the window then makes it fullscreen
        window = Tkinter.Tk(className=' ALPRN')
        #window.attributes("-fullscreen",True)

        HeadsUp = Tkinter.StringVar()
        HeadsUp.set("This shouldn't be visible")
        LastSeenUpdate = [1]
        LastSeen = Tkinter.StringVar()
        HeadsUp.set("This shouldn't be visible")
    
        # Initializes the database from file
        dBase_fill()
    
        # Instantiates the worker thread
        thread = Thread(target = Alpr_run)

        # Instantiating elements for the window
        alive = Tkinter.Button (window,bg="black")
        clearbutton = Tkinter.Button (window,pady=1,padx=5,text="Clear",command=lambda:clear_buttoncall(window,notes),bg="green")
        acknowledge = Tkinter.Button (window,pady=1,padx=5,text="Acknowledge",command=lambda: acknowledge_buttoncall(window),bg="yellow")
        exitbutton = Tkinter.Button (window,pady=1,padx=5,text="Exit",command=lambda:exit_buttoncall(thread,window),bg="red")
        notes = Tkinter.Label (window,bg="white",textvariable=HeadsUp)
        lastseen = Tkinter.Label (window,bg="white",textvariable=LastSeen)

        # Variables used to manipulate multiple button placements and sizes
        bottom_row_height = 0.15
        bottom_row_width = 0.3

        # Placing elements in the window
        alive.place(relheight=0.045,relwidth=0.025,relx=0,rely=0)
        exitbutton.place(relheight=bottom_row_height,relwidth=0.1,relx=0,rely=1-bottom_row_height)
        acknowledge.place(relheight=bottom_row_height,relwidth=bottom_row_width,relx=1-(2*bottom_row_width),rely=1-bottom_row_height)
        clearbutton.place(relheight=bottom_row_height,relwidth=bottom_row_width,relx=1-bottom_row_width,rely=1-bottom_row_height)
        lastseen.place(relheight=0.1,relwidth=0.5,relx=0.49,rely=0.01)
        
        change_color(alive,window,1500,[1])
        change_color(window,window,750,screenblink)
        # Starts the worker thread
        thread.start()
    
        # This is the gui loop
        while True:
            if(LastSeenUpdate[0] == 1):
                lastseenlock.acquire()
                LastSeen.set(foundplate[0])
                lastseenlock.release()
                LastSeenUpdate[0] = 0
                window.after(5000, ch_arr_variable, LastSeenUpdate,0,1)
            if(foundmatch[0] == 1):
                alprwake.acquire()
                foundmatch[0] = 0
                screenblink[0] = 1
                # XXX: Additional database fields must be fleshed out here
                HeadsUp.set("Match found!\nLicense plate: "+dBase[foundindex[0]][fields[0]]+" from "+dBase[foundindex[0]][fields[1]]+"\nReason for interest:"+platestatus[int(dBase[foundindex[0]][fields[2]])]+"\nMake,Model: "+dBase[foundindex[0]][fields[4]]+" "+dBase[foundindex[0]][fields[5]]+"\nColor: "+dBase[foundindex[0]][fields[3]])
                notes.place(relx=0.2,rely=0.2,relwidth=0.6,relheight=0.5)
                alprwake.release()
            if(foundmatch[0] == 7):
                break
            # These two lines are what update the display
            window.update_idletasks()
            window.update()
        exit_buttoncall(thread,window)
    except KeyboardInterrupt:
        exit_buttoncall(thread,window)
if __name__ == '__main__':
    main()
    