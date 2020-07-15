# generate county percentages for Event 4338
# this script generates county-specific percentages of flood extent that occurred outside of FEMA flood zones for Event 4338

execfile ("calculate_percent_of_flood_extent_within_flood_zones.py")
import csv
import os
counties_list = [48015,48089,48139,48145,48157,48161,48201,48213,48289,48331,48339,48349,48395,48407,48455,48471,48473,48481,48021,48051,48185,48293,48309,48423]
#counties_list = [48021]

#counties_list = [48015,48089]
percent_list  = []
#percent_list  = [45,90]

for fips in counties_list:
	#print (str(fips))
	percent = estimate_percent_of_flood_within_flood_zone(4348,"county",str(fips))
	percent_list.append(percent)
	
print(percent_list)
f = "C:\\Users\\jdeclet-barreto\\Documents\\EPIF\\data\\overlay_analysis\\geography-specific_analysis\\county\\csv\\Event_4338_selected_counties_report.csv"
if os.path.exists(f):
    os.remove(f)
with open(f, 'wb') as outcsv:
    writer = csv.writer(outcsv)
    writer.writerow(["FIPS", "PER_FLOOD_OUTSIDE_FEMA_FLOOD_ZONES"])
    
    for fips, percent in zip(counties_list,percent_list):
    	per = 100 * round(percent,4)
    	writer.writerow([fips, per])
    outcsv.close()