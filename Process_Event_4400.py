# generate county percentages for Event 4338
# this script generates county-specific percentages of flood extent that occurred outside of FEMA flood zones for Event 4338

execfile ("calculate_percent_of_flood_extent_within_flood_zones.py")
import csv
import os
#counties_list = [19023,19017,19013,19019,19127,19171,19011,19113]
counties_list = [19011,19013,19017,19019,19023,19043,19055,19065,19075,19113,19127,19171]
#counties_list = [19023]
event_id = 4400
percent_flooded_outside_list  = []
percent_flooded_in_geography_list = []

for fips in counties_list:
	#print (str(fips))
	percent_flooded_outside      = estimate_percent_of_flood_within_flood_zone(event_id,"county",str(fips))[0]
	percent_flooded_in_geography = estimate_percent_of_flood_within_flood_zone(event_id,"county",str(fips))[1]	
	percent_flooded_outside_list.append(percent_flooded_outside)
	percent_flooded_in_geography_list.append(percent_flooded_in_geography)
	
print(percent_flooded_outside_list)
print(percent_flooded_in_geography_list)
f = "C:\\Users\\jdeclet-barreto\\Documents\\EPIF\\data\\overlay_analysis\\geography-specific_analysis\\county\\csv\\Event_" + str(event_id) + "_selected_counties_report.csv"
if os.path.exists(f):
    os.remove(f)
with open(f, 'wb') as outcsv:
    writer = csv.writer(outcsv)
    writer.writerow(["FIPS", "PER_FLOOD_OUTSIDE_FEMA_FLOOD_ZONES","PER_FLOODED_IN_GEOGRAPHY"])
    
    for fips, percent_flooded_outside, percent_flooded_in_geography in zip(counties_list,percent_flooded_outside_list,percent_flooded_in_geography_list):
    	per1 = 100 * round(percent_flooded_outside,4)
    	per2 = 100 * round(percent_flooded_in_geography,4)
    	writer.writerow([fips, per1,per2])
    outcsv.close()