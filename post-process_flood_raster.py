execfile ("calculate_percent_of_flood_extent_within_flood_zones.py")
import csv
import os

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