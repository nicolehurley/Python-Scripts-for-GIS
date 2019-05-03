# Nicki Hurley
# 09/15/2017

# This script runs through all the MXDs in the given folder path and replaces the source location of all the layers in the MXD
# to that of the desired File GDB (where the name of the .shp is the same as the name of a feature class in the File GDB.
# Multiple GDB locations can be used. Data in the MXD not included in the GDB are ignored (data links not broken). Resulting MXDs
# are saved to a new folder called "Updated".  Original MXDs are not modified. To use, add the file path to the folder containing
# the MXDs to be updated, then add the location of the GDBs the data layers will be re-sourced to.

import arcpy, os

# File path for MDXs to be updated
MXD_Folder_Path = r"M:\file_location"

# File paths for GDB that data will be re-sourced to
newBackgroundGDB = r"\\file_location"
newProjectData = r"M:\file_location"

# Set workspace for MXDs and loop through files
arcpy.env.workspace = MXD_Folder_Path
mxd_list = arcpy.ListFiles("*.mxd")

date = datetime.datetime.today().strftime("%Y%m%d")
os.makedirs(MXD_Folder_Path + "\\" + date + "_Updated")

for mxd in mxd_list:
    print str("processing " + mxd)
    # read MXD
    mxd_read = arcpy.mapping.MapDocument(MXD_Folder_Path + "\\" + mxd)
    # replace data included in first GDB
    mxd_read.replaceWorkspaces("", "NONE", newBackgroundGDB, "FILEGDB_WORKSPACE")
    # replace data included in second GDB
    mxd_read.replaceWorkspaces("", "NONE", newSDSFIE, "FILEGDB_WORKSPACE")
    # can repeat lines above if there are multiple GDBs
    # save a copy to new folder
    mxd_read.saveACopy(MXD_Folder_Path + "\\" + date + "_Updated\\" + mxd)

print "Completed"
