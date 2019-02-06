import sys

def get_geography_workspace(argument):
    geography_dict = {
        "county": ["C:\\Users\\jdeclet-barreto\\Documents\\EPIF\\data\\counties.gdb\\counties_NAD83","GEOID","NAMELSAD"],
        "congressional_district": ["","",""]
    }
    return geography_dict.get(argument, "Invalid geography")

def estimate_percent_of_flood_within_flood_zone(flood_event_id, geography, geography_fips):
    import arcpy
    import datetime
    import glob
    import os
    
    flood_event_id = str(flood_event_id)
    geography_specific_analysis_dir = "C:\\Users\\jdeclet-barreto\\Documents\\EPIF\\data\\overlay_analysis\\geography-specific_analysis\\" + geography
    
    print ("PROCESS STARTING: Calculate Percent of Flood Extent within Flood Zones on " + str(datetime.datetime.now()))
    print ("Flood Event ID: " + flood_event_id)
    print ("Geography     : " + geography)
    print ("FIPS          : " + str(geography_fips))
    
    print ("Checking out Spatial Analyst extension")
    arcpy.CheckOutExtension("Spatial")

    #local variables
    flood_extent_GDBs_dir = "C:\\Users\\jdeclet-barreto\\Documents\\EPIF\\data\\overlay_analysis"
    FEMA_flood_zones = "C:\\Users\\jdeclet-barreto\\Documents\\EPIF\\data\\FEMA_flood_hazard_areas.gdb\\FEMA_NFHL_100_500_year_flood_zones_NAD83"
    geography_fc = get_geography_workspace(geography)[0]
    geography_geoid_fld_name = get_geography_workspace(geography)[1]
    geography_name_fld_name = get_geography_workspace(geography)[2]

    if arcpy.Exists(geography_fc):
  	print ("Geography " + geography_fc + " exists.")
    else:
    	print ("Geography " + geography_fc + " not found; exiting.")
  	sys.exit()
      
    
    #find flood event workspace
    #this flood event workspace must have already been created
    #cast to string
    flood_event_id = str(flood_event_id)
    flood_event_gdb = flood_extent_GDBs_dir + "\\Event_" + flood_event_id + ".gdb"
    flood_event_raster = flood_event_gdb  + "\\Event_" + flood_event_id + "_floodwaters_final"
    
    if arcpy.Exists(flood_event_gdb):
  	print ("Flood Event GDB " + flood_event_gdb + " exists.")
    else:
    	print ("Flood Event GDB " + flood_event_gdb + " not found; exiting.")
  	sys.exit()
    
    event_FEMA_flood_zones              = flood_event_gdb + "\\Event_" + flood_event_id + "_FEMA_flood_zones" 
    
    
    #find geography name
    qry = geography_geoid_fld_name + "='" + geography_fips + "'"
    print (qry)
    fields = [geography_name_fld_name]
    cursor = arcpy.da.SearchCursor(geography_fc, where_clause=qry,field_names=fields)
    for row in cursor:
    	name = str(cursor[0]).replace(" ","_")
    #create GDB for analysis
    geography_gdb = "Event_" + flood_event_id + "_" + name + ".gdb"
    
    #Process: Create FGDB
    #first try to delete existing one
    try:
    	if arcpy.Exists(geography_specific_analysis_dir + "\\" + geography_gdb):
    	   	print ("Deleting " + geography_specific_analysis_dir + "\\" + geography_gdb)
    		arcpy.Delete_management(geography_specific_analysis_dir + "\\" + geography_gdb)
    except:
    	print ("Delete " + geography_specific_analysis_dir + "\\" + geography_gdb + " failed.")
    	sys.exit()
    #now re-create FGDB
    try:
    	arcpy.CreateFileGDB_management(geography_specific_analysis_dir, geography_gdb, "CURRENT")
    	print ("Create " + geography_specific_analysis_dir + "\\" + geography_gdb + " succeeded.")
    except:
       	print ("Create " + geography_specific_analysis_dir + "\\" + geography_gdb + " failed.")

    event_FEMA_geography = geography_specific_analysis_dir + "\\" + geography_gdb + "\\Event_" + flood_event_id + "_" + name
    event_FEMA_flood_zones_in_geography = geography_specific_analysis_dir + "\\" + geography_gdb + "\\Event_" + flood_event_id + "_FEMA_flood_zones_in_" + name
    floodwaters_in_geography = geography_specific_analysis_dir + "\\" + geography_gdb + "\\Event_" + flood_event_id + "_floodwaters_in_" + name
    floodwaters_in_geography_polygon = geography_specific_analysis_dir + "\\" + geography_gdb + "\\Event_" + flood_event_id + "_floodwaters_in_" + name + "_poly"
    floodwaters_in_geography_outside_of_FEMA_flood_zones = geography_specific_analysis_dir + "\\" + geography_gdb + "\\Event_" + flood_event_id + "_floodwaters_outside_FEMA_floodzones_" + name
    total_flooded_area_in_geography = geography_specific_analysis_dir + "\\" + geography_gdb + "\\Event_" + flood_event_id + "_total_flooded_area_in_" + name
    total_flooded_area_outside_FEMA_flood_zones_in_geography = geography_specific_analysis_dir + "\\" + geography_gdb + "\\Event_" + flood_event_id + "_total_flooded_area_outside_FEMA_floodzones_in_" + name

    #Process: Clip Event FEMA Flood Zones to Geography
    #first create geography feature layer
    geography_lyr="geography_lyr"
    arcpy.MakeFeatureLayer_management(geography_fc,geography_lyr,qry)
    n = arcpy.GetCount_management(geography_lyr)
    print ("Copying " + str(n) + " rows to " + event_FEMA_geography)
    arcpy.CopyFeatures_management(geography_lyr,event_FEMA_geography)
    print ("Clipping " + event_FEMA_flood_zones + " to " + event_FEMA_geography)
    arcpy.Clip_analysis(event_FEMA_flood_zones, event_FEMA_geography, event_FEMA_flood_zones_in_geography, "")
    
    print ("Extracting raster floodwaters in " + name)
    arcpy.gp.ExtractByMask_sa(flood_event_raster , geography_lyr, floodwaters_in_geography)
    
    print ("Converting floodwaters raster to polygon")
    arcpy.RasterToPolygon_conversion(floodwaters_in_geography, floodwaters_in_geography_polygon, "NO_SIMPLIFY", "Value")
    
    print ("Calculating total flooded area in " + name)
    arcpy.Statistics_analysis(floodwaters_in_geography_polygon, total_flooded_area_in_geography, "Shape_Area SUM", "")
    
    print ("Generating floodwaters oustide of FEMA floodzones in " + name)
    arcpy.Erase_analysis(floodwaters_in_geography_polygon, event_FEMA_flood_zones_in_geography, floodwaters_in_geography_outside_of_FEMA_flood_zones, "")
        
    print ("Calculating total area of floodwater outside FEMA floodzones in " + name)
    arcpy.Statistics_analysis(floodwaters_in_geography_outside_of_FEMA_flood_zones, total_flooded_area_outside_FEMA_flood_zones_in_geography, "Shape_Area SUM", "")
    
    total_flooded_area_in_geography_value = 0
    cursor = arcpy.da.SearchCursor(total_flooded_area_in_geography,field_names=["SUM_Shape_Area"])
    for row in cursor:
    	total_flooded_area_in_geography_value = row[0]
    print("Total flooded are in " + name  + ": " + str(total_flooded_area_in_geography_value))
    
    total_flooded_area_outside_FEMA_flood_zones_in_geography_value = 0
    cursor = arcpy.da.SearchCursor(total_flooded_area_outside_FEMA_flood_zones_in_geography,field_names=["SUM_Shape_Area"])
    for row in cursor:
        total_flooded_area_outside_FEMA_flood_zones_in_geography_value = row[0]
    print("Total flooded are outside FEMA flood zones in " + name + ": " + str(total_flooded_area_outside_FEMA_flood_zones_in_geography_value))
    
    percent_of_flooded_area_outside_of_FEMA_floodzones_in_geography = total_flooded_area_outside_FEMA_flood_zones_in_geography_value / total_flooded_area_in_geography_value
    print("fraction:" + str(percent_of_flooded_area_outside_of_FEMA_floodzones_in_geography))
    
estimate_percent_of_flood_within_flood_zone(4348,"county","48473")


