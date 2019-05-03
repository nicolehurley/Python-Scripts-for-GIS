# N. Hurley, 1/2/2018
# This script runs through all the mxds in a folder and imports the shapefiles
# in those mxds into a new file geodatabase. The script skips data already
# located in gdb. The script uses a project area shapefile to identify the
# appropriate spatial reference information and can clip all data imported to
# a buffered extent of that project area. After running this script, use
# ReplaceWorkspaces.py to re-source all your MXDs to the new geodatabase.

import arcpy, os, sys

# Set workspace. Filepath for the folder of existing mxds from which to pull
# data.  Be sure to leave the 'r', i.e. r"C:\MyFilePath".
arcpy.env.workspace = r"M:\Office\Project\Maps\MXDs"
Workspace = arcpy.env.workspace 

# Filepath for the location of the new gdb. No 'r' required.
out_folder_path = "M:\Office\Project\Data"

# Grabs the current date to append to the gdb name
date = datetime.datetime.today().strftime("%Y%m%d")

# Name of the new gdb.
out_name = str("PackagedData_" + date + ".gdb")

# Name of feature dataset.
Dataset = "Common"

# Filepath for the project area shapefile.
ProjectArea = "M:\Office\Project\Data\ProjectFeatures\Project_Area.shp"

# Determines if imported data is clipped. Type True or False.
Buffered = True

# Desired buffer distance and units. Change only needed if Buffered = True
Buffer_Distance = "100"
Buffer_Units = "MILES"

# -------------No edits needed beyond this point----------------

# Creates list of mxds in workspace
mxd_list = arcpy.ListFiles("*.mxd")

# Empty list for shapefile included in mxds
SourceList = []

# Create a spatial reference object
sr = arcpy.SpatialReference(ProjectArea[:-4] + ".prj")

# Execute CreateFileGDB
arcpy.CreateFileGDB_management(out_folder_path, out_name)

# Execute Create Feature Dataset
arcpy.CreateFeatureDataset_management(os.path.join(out_folder_path, out_name), Dataset, sr)

# Loops through all the mxds in folder
print "Collecting data from MXDs..."
for mxd in mxd_list:
    # prints status
    print str("processing " + mxd)
    # reads MXD
    mxd_read = arcpy.mapping.MapDocument(os.path.join(Workspace, mxd))
    # Loops through data frames in mxd
    for df in arcpy.mapping.ListDataFrames(mxd_read, ""):
        # Loops through layers in data frame
        for lyr in arcpy.mapping.ListLayers(mxd_read, ""):
            # Determines if item is valid
            if lyr.supports("dataSource"):
                # Checks if item is already in list
                if lyr.dataSource in SourceList:
                    pass
                # If not, adds to list
                else:
                    SourceList.append(lyr.dataSource)

# Buffers project area by chosen amount
if Buffered:
    extent = arcpy.Buffer_analysis(ProjectArea, os.path.join(out_folder_path, out_name) + "\\" + "ProjectArea_Buffer", str(Buffer_Distance + " " + Buffer_Units), "FULL", "", "ALL") 

# Loops through data pulled from mxds
if Buffered:
    print str("Clipping and importing data into " + out_name + "...")
else:
    print str("Importing data into " + out_name + "...")
    
for data in SourceList:
    # if variable 'Buffered' was made True, then all data sources are clipped to the identified buffer distance around project area
    if Buffered:
        print str("processing" + " " + data)
        # selects proper naming convention based on whether or not file ends in .shp, then clips to buffer
        if data[-4:] == ".shp":
            clipped_data = arcpy.Clip_analysis(data, extent, Workspace + "\\" + data[:-4].rsplit('\\',1)[-1])
        else:
            clipped_data = arcpy.Clip_analysis(data, extent, Workspace + "\\" + data.rsplit('\\',1)[-1])
        # clipped features are imported into geodatabase
        arcpy.FeatureClassToGeodatabase_conversion(clipped_data, os.path.join(out_folder_path, out_name) + "\\" + Dataset)
        # extraneous clipped shaepfile deleted
        arcpy.Delete_management(clipped_data)
    else:
        print str("processing" + " " + data)
        # if no clipping selected, original shapes are imported directly into gdb
        arcpy.FeatureClassToGeodatabase_conversion(data, os.path.join(out_folder_path, out_name) + "\\" + Dataset)

# All set!          
print "Completed"
