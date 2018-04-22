import Tkinter
from Tkinter import StringVar

camsearch = [0]
screenblink = [0]

def ch_color(blinky):
   	current_color = blinky.cget("background")
   	next_color = "white" if current_color == "black" else "black"
   	blinky.config(background=next_color)

def change_color(blinky,delay,enable):
	if (enable[0] == 1):
		ch_color(blinky)		
	window.after(delay, change_color, blinky, delay, enable)
	
	
def clear_buttoncall():
	camsearch[0] = 1
	screenblink[0] = 0
	notes.place_forget()
	window.config(background="light grey")
	
	
def acknowledge_buttoncall():
	if (screenblink[0] == 0):
		screenblink[0] = 1
		notes.place(relx=0.1,rely=0.1,relwidth=0.8,relheight=0.7)
	else:
		screenblink[0] = 0
		window.config(background="light grey")
		
	
def exit_buttoncall():
	#Need to include any other application close out here (Ex: alpr agent close, etc)
	window.destroy()
	
#Instantiates the window then makes it fullscreen
window = Tkinter.Tk()
window.attributes("-fullscreen",True)

HeadsUp = Tkinter.StringVar()
HeadsUp.set("This is just a test!\nThis text label is intended to give you\nCar info over a blinking screen")

#Instantiating elements for the window
alive = Tkinter.Button (window,bg="black")
okay = Tkinter.Button (window,pady=1,padx=5,text="Clear",command=clear_buttoncall,bg="green")
acknowledge = Tkinter.Button (window,pady=1,padx=5,text="Acknowledge",command=acknowledge_buttoncall,bg="yellow")
exitbutton = Tkinter.Button (window,pady=1,padx=5,text="Exit",command=exit_buttoncall,bg="red")
notes = Tkinter.Label (window,bg="white",textvariable=HeadsUp,font=("Courier",20))

# Variables used to manipulate multiple button placements and sizes
bottom_row_height = 0.15
bottom_row_width = 0.3

#Placing elements in the window
alive.place(relheight=0.045,relwidth=0.025,relx=0,rely=0)
exitbutton.place(relheight=bottom_row_height,relwidth=0.1,relx=0,rely=1-bottom_row_height)
acknowledge.place(relheight=bottom_row_height,relwidth=bottom_row_width,relx=1-(2*bottom_row_width),rely=1-bottom_row_height)
okay.place(relheight=bottom_row_height,relwidth=bottom_row_width,relx=1-bottom_row_width,rely=1-bottom_row_height)

change_color(alive,1500,[1])
change_color(window,750,screenblink)

window.mainloop()
