# N. Hurley, 1/2/2018
# This script runs through all the mxds in a folder and exports them to a pdf.

import arcpy, os, sys

# Set workspace. Filepath for the folder of existing mxds from which to pull
# data.  Be sure to leave the 'r', i.e. r"C:\MyFilePath".
arcpy.env.workspace = r"M:\file_location"
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
