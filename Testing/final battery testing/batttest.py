from datetime import datetime
import time
import csv
import subprocess
import string
import os
import signal
import sys

# Ensures new test is written to new versions of the files
open('batt1.csv','wb')
open('batt2.csv','wb')

# How many seconds to wait between measurements
sl_time = 5
# Total run time in seconds
run_time = 8 * 60 * 60
# Measurement count, based on above numbers
mes_count = run_time/sl_time

# Invoke core loading program(called stress) here
# 28,800 seconds is about 8 hrs
# Popen allows use of a variable which can be used to terminate the process later
# preexec_fn is called after the fork and before exec'ing stress
# os.setsid puts our set of threads/processes into a group that can be terminated together
#stressprog = subprocess.Popen(['python','ALPRN.py'], preexec_fn=os.setsid)
stressprog = subprocess.Popen(['python','ALPRN.py'])

def closeout(reason_str):
	#os.killpg(os.getpgid(stressprog.pid),signal.SIGTERM)
	# Writes a note informing that the test finished due to thermal
	with open('batt1.csv','ab') as csvfile:
		out1 = csv.writer(csvfile)
		out1.writerow([reason_str])
	with open('batt2.csv','ab') as csvfile:
		out2 = csv.writer(csvfile)
		out2.writerow([reason_str])

try:
	# Each tick in the loop represents approximately 6 seconds, 4800 ticks is roughly 8 hours
	for i in range(1,mes_count):
		# allocates current date and time for the log file
		curtime = datetime.today()
		# Utilizes a command line program to acquire a string with the core temp
		curtemp = subprocess.check_output(["/opt/vc/bin/vcgencmd","measure_temp"])
		# Strips the newline character from the end of the output from previous command
		curtemp = string.rstrip(curtemp,'\n')
		#curtemp = 'temp=55\'C'
		# This line outputs a status line.  This method allows overwriting the same line repeatedly to preclude drowning the console
		sys.stdout.write('{}{} {:.2f}{}'.format('\r',curtemp,(float(i)/float(mes_count))*100,'%'))
		sys.stdout.flush()
		# Finishes stripping characters from before and after the useful numbers from the string
		curtemp = string.lstrip(curtemp,'temp=')
		curtemp = string.rstrip(curtemp,'\'C')

		# code for testing thermal abort
		#if i == 2:
		#	curtemp = "81.0"

		# This section writes to two different csvs.  This is intended to avoid an issue from possibly corrupting a file by having it open for write at the time of running out of power.  This way a max of 6sec is lost, if the other file is somehow illegible
		if (i % 2) == 1:
			#write to end of file 1
			with open('batt1.csv','ab') as csvfile:
				out1 = csv.writer(csvfile)
				out1.writerow([curtime.isoformat(' '), curtemp])
		else:
			#write to end of file 2
			with open('batt2.csv','ab') as csvfile:
				out2 = csv.writer(csvfile)
				out2.writerow([curtime.isoformat(' '), curtemp])

		# Should abort the test if the thermal limit is reached
		# limit: 85C, with throttling before then
		if float(curtemp) >= 80.5:
			print "\nThermal condition present, Aborting test"
			#shutdown core loading program
			closeout('Thermal')
			break
	# Sleep this process for sl_time(set towards the top) seconds until recording a new value
	# Research suggests this may result in around 10-15ms inaccuracy in wait time
	time.sleep(sl_time)
	print "\nTest Concluded"
except KeyboardInterrupt:
	closeout('Keyboard')
	print "Keyboard Interrupt"	
