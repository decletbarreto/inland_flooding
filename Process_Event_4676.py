# generate county percentages for Event 4676
# this script generates county-specific percentages of flood extent that occurred outside of FEMA flood zones for Event 4676

execfile ("calculate_percent_of_flood_extent_within_flood_zones.py")
import csv
import os
counties_list = [37129,37001,37007,37013,37015,37017,37019,37031,37033,37037,37041,37047,37049,37051,37057,37061,37063,37065,37067,37069,37079,37081,37083,37085,37091,37093,37095,37101,37103,37105,37107,37117,37123,37125,37127,37131,37133,37135,37137,37141,37143,37147,37151,37153,37155,37157,37163,37165,37167,37169,37183,37187,37191,37195,45015,45025,45027,45031,45033,45041,45043,45051,45067,45069,45089]
#counties_list = [19023]
event_id = 4676
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