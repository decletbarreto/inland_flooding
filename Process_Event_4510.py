# generate county percentages for Event 4510
# this script generates county-specific percentages of flood extent that occurred outside of FEMA flood zones for Event 4510

execfile ("calculate_percent_of_flood_extent_within_flood_zones.py")
import csv
import os


counties_list = ["22003","22011","22019","22023","22053","22113","22115","48039","48071","48157","48199","48201","48241","48245","48291","48339","48351","48361","48373","48407","48457","48471","48167"]
#counties_list = ["48351","48361","48373","48407","48457","48471","48167"]
#counties_list = ["48199","48201","48241","48245","48291","48339","48351","48361","48373","48407","48457","48471","48167"]


#counties_list = ["22001"]

event_id = 4510
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
f = "d:\\UCS_projects\\EPIF\\data\\overlay_analysis\\geography-specific_analysis\\county\\csv\\Event_" + str(event_id) + "_selected_counties_report.csv"
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