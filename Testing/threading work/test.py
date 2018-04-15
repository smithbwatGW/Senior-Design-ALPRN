#!/usr/local/bin/python
import Tkinter
import threading
from threading import Thread
import sys
from time import sleep

# Global variables
signal = [0]
signal_str = ["a"]
testcond = threading.Condition()
#HeadsUp = ["Thread not run\n"]
#print HeadsUp[0]

def ThreadFunc():
    sleep(5)
    for i in range(5):
        testcond.acquire()
        signal_str[0] = "Thread has run "+str(i+1)+" time"
        #HeadsUp[0] = "Thread has run "+str(i+1)
        signal[0] = 1
        testcond.wait()
        testcond.release()
        sleep(5)
    testcond.acquire()
    signal[0] = 1
    signal_str[0] = "Thread completed successfully!"
    testcond.release()

def exit_buttoncall(thread,window):
    #Need to include any other application close out here (Ex: alpr agent close, etc)
    thread.join()
    window.destroy()
    sys.exit()

def main():
    #Setting up the gui_nonpi    
    window = Tkinter.Tk()
    HeadsUp = Tkinter.StringVar()
    HeadsUp.set("Thread not running yet")
    notes = Tkinter.Label (window,bg="white",textvariable=HeadsUp)
    notes.place(relx=0.1,rely=0.1,relwidth=0.8,relheight=0.8)
    exitbutton = Tkinter.Button (window,pady=1,padx=5,text="Exit",bg="red",command=lambda: exit_buttoncall(thread,window))
    exitbutton.place(relheight=0.1,relwidth=0.1,relx=0,rely=0.9)
    
    thread = Thread(target = ThreadFunc)
    thread.start()
    while True:
        if(signal[0] == 1):
            testcond.acquire()
            signal[0] = 0
            HeadsUp.set(signal_str[0])
            testcond.notify()
            testcond.release()
        window.update_idletasks()
        window.update()
    
if __name__ == "__main__":
    main()
