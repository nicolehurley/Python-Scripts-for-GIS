# N. Hurley, 12/12/2017

# This script adds a new field to all feature classes in a file location and
# populates it with the name of the file.  To be used as a preliminary step
# before merging multiple files together to retain source information. Modify
# the workspace directory to use.


# Import standard library modules
import arcpy, os, sys
from arcpy import env

# Allow for file overwrite
arcpy.env.overwriteOutput = True

# Set the workspace directory 
env.workspace = r"M:\Tallahassee\NSA_Panama_City\Output\SDSFIE\TEMP\staging_area.gdb" 

# Get the list of the featureclasses to process
fc_tables = arcpy.ListFeatureClasses()

# Loop through each file and perform the processing
for fc in fc_tables:
    print str("processing " + fc)

    # Define field name and expression
    field = "DQ"
    expression = str(fc) #populates field   

    # Create a new field with a new name
    arcpy.AddField_management(fc,field,"TEXT")

    # Calculate field here
    arcpy.CalculateField_management(fc, field, '"'+expression+'"', "PYTHON")

print "Completed"
