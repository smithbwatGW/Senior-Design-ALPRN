import csv

dBase = []
# When the database is further fleshed out, this will need the new fields inputted and a few other lines adjusted
fields = ['plate', 'state', 'stolen']
stub_candidates = []

with open('database.csv','rb') as csvfile:
	dline = csv.DictReader(csvfile,fieldnames=fields)
	for row in dline:
		# This implementation allows easier legibility when referencing entry values
		dBase.append({fields[0]:row[fields[0]],fields[1]:row[fields[1]],fields[2]:row[fields[2]]})
		stub_candidates.append({fields[0]:row[fields[0]],fields[1]:row[fields[1]],fields[2]:row[fields[2]]})
	
stub_candidates.append({fields[0]:'ETALLIC',fields[1]:'NY',fields[2]:'0'})
for i in range(2):
	dBase.remove(dBase[0])

# Demonstrates the ability to retrieve specific info per entry by its field name
print dBase[3]['state']
# Prints the whole database.  Entries are in the format of 'label':'value'
for entry in dBase:
	print entry
# Demo'ing matching
for entry in stub_candidates:
	match = "No Match"
	j=0
	for value in dBase:
		if entry['plate'] == value['plate']:
			match = "Matched!"
			break
		else:
			j+=1
	if  j < len(dBase):
		print("%12s%12s%12s" % (dBase[j][fields[0]],dBase[j][fields[1]],match))
		print("%12s%12s%12s" % (entry[fields[0]],entry[fields[1]],match))
	else:
		print("%12s%12s%12s" % (entry[fields[0]],entry[fields[1]],match))
	
	
	
	