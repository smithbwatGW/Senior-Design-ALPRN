import picamera
from openalpr import Alpr
import csv

camera = picamera.PiCamera()
camera.resolution = (1920,1080)
camera.capture('camera.jpg')
threshold = 65.00
# Field labels for currently implemented csv fields
fields = ['plate', 'state', 'stolen']
# File names to be demonstrated, adjustable as desired
names = ["camera.jpg", "nolicense.jpg", "IBAY41.jpg", "JZH4505.jpg", "ea7the.jpg"]

# These seem to be functional
alpr = Alpr("us","/etc/openalpr/openalpr.conf","/usr/share/openalpr/runtime_data")
if not alpr.is_loaded():
	print("Error loading OpenALPR")
	sys.exit(1)
	
# This one dictates how many results to display
alpr.set_top_n(10)
# This determines whether alpr will try to determine region on recognize
alpr.set_detect_region(True)
# This one sets a default region, if desired
# alpr.set_default_region("md")

	# Runs the image through alpr and then deposits info in results
results = alpr.recognize_file("camera.jpg")
print("Results for Camera")	
i = 0
# This loop iterates through the plates the program identified	
for plate in results['results']:
	i += 1
	# These prints can be considered debug text, since we don't need them for final implementation
	print("Plate #%d" % i)
	print("Results above threshold:")
	print("   %12s %12s  %s" % ("Plate", "Confidence","Database Hit"))
	# This nested loop iterates through the various permutations it thinks this plate might be
	# higher confidence at the top
	for candidate in plate['candidates']:
		prefix = "-"
		if candidate['matches_template']:
			prefix = "*"
		# Polls for whether this candidate for plate has a high enough confidence for our criteria
		# threshold is defined above
		if candidate['confidence'] >= threshold:
			with open('database.csv','rb') as csvfile:
				dline = csv.DictReader(csvfile,fieldnames=fields)
				for row in dline:
					if candidate['plate'] == row['plate']:
						match = "Match!"
						break
					else:
						match = "No Match"
			print("  %s %12s%12f  %s" % (prefix, candidate['plate'], candidate['confidence'], match))
		else:
			# Debug line showing the below threshold value with an X
			#print("  X %12s%12f" % (candidate['plate'], candidate['confidence']))
			break
raw_input("Press Enter to continue")
# This is the line to unload our alpr agent from memory		
alpr.unload()
