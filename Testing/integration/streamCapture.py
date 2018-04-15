from openalpr import Alpr
from time import sleep
from picamera import PiCamera
import sys
import csv

camera = PiCamera()
camera.resolution = (1920,1080)
alpr = Alpr("us","/home/zib/Senior-Design-ALPR/src/build/config/openalpr.conf","/home/zib/Senior-Design-ALPR/runtime_data")
if not alpr.is_loaded():
	print("Error loading OpenALPR")
	sys.exit(1)

alpr.set_top_n(10)
# Do we want to specify md?
alpr.set_default_region("md")

dBase = []
# When the database is further fleshed out, this will need the new fields inputted and a few other lines adjusted
fields = ['plate', 'state', 'stolen']

with open('database.csv','rb') as csvfile:
	dline = csv.DictReader(csvfile,fieldnames=fields)
	for row in dline:
		#This implementation allows easier legibility when referencing entry values
		dBase.append({fields[0]:row[fields[0]],fields[1]:row[fields[1]],fields[2]:row[fields[2]]})

#Trims the first two entries, which aren't database fields
for i in range(2):
	dBase.remove(dBase[0])


try:
	while True:
		camera.capture('/home/zib/plates/image.jpg')
		results = alpr.recognize_file("/home/zib/plates/image.jpg")
		i=0
		for plate in results['results']:
			i+=1
			#print("Plate #%d" % i)
			print("   %12s %12s" % ("Plate", "Confidence"))
			for candidate in plate['candidates']:
				matched = "No match"
				prefix = "-"
				if candidate['matches_template']:
					prefix = "*"
				if candidate['confidence'] >= 85:
					# hit_index will be used by the gui to fill in the desired info for display when a match occurs
					# May or may not be useful if separate processes between gui and this
					hit_index=0
					for entry in dBase:
						if candidate['plate'] == entry['plate']:
							matched = "Match!"
							#
							# Throw up notification!
							#	
							# I'm inclined to look into sleep/wake for the gui and pausing the program
							# Perhaps achievable with subprocess
							# But!! that's a consideration for down the road
						hit_index+=1
							
					print("   %s %12s%12f%12s" % (prefix, candidate['plate'], candidate['confidence'],matched))
		sleep(0.5)
	alpr.unload()
except KeyboardInterrupt:
	sys.exit()
	alpr.unload()