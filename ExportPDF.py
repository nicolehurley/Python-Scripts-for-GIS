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
arcpy.env.workspace = r"M:\Portland\USFS_Phosphate_Mines\Maps_All\MXDs"
Workspace = arcpy.env.workspace 




# -------------No edits needed beyond this point----------------

# Creates list of mxds in workspace
mxd_list = arcpy.ListFiles("*.mxd")


# Loops through all the mxds in folder
print "Collecting data from MXDs..."
for mxd in mxd_list:
    # prints status
    print str("processing " + mxd)
    # reads MXD
    mxd_read = arcpy.mapping.MapDocument(os.path.join(Workspace, mxd))
    pdf_name = mxd[:-4] + ".pdf"
    arcpy.mapping.ExportToPDF(mxd_read, pdf_name)


# All set!          
print "Completed"
