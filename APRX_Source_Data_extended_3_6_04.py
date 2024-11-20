################################################################################
# Title:            APRX_Source_Data_extended_3_6_04.py
# Description:      This script is an extension of APRX_Source_Data_3_6_02.py
#                   and crawls a supplied directory and lists all the following
#                   information for any APRX in that directory:
#                   
#                   - Project Name
#                   - Project Path
#                   - Map name/s
#                   - Layer names
#                   - Layer Data Sources
#                   - has Labels
#                   - symbology field
#
# Author:           Martin Best
# Date:             01st August 2020
#
# Required Modules: arcpy   Version 3.6(Installed with ArcGIS Pro)
#                   os (native)
#                   csv
#
# Amendments:       3.6.01  Extended original APRX_Source_Data_3_6_02.py script
#                           - added code to determine if layer has labels defined
#                           (Pete Smyth - 24th May 2022 08:23)
#
#                   3.6.02  Added code to exclude specific subdirectories
#                           (e.g. archive, .backups and .gdb) which either contain
#                           backed up or archive copies of aprx files wich we do not
#                           want to include in the scan or is a Geodatabase file.
#                           (Pete Smyth - 17th August 2022 10:44)
#
#                   3.6.03  Added code to bypass potential errors if layer object
#                           does not support layer name method when iterating through Layerlist.
#                           Also added Comments and function documentation.
#                           (Pete Smyth - 9th August 2024 09:02)
#
#                   3.6.04  Added code to determine the fieldname/s used for symbology
#                           if the renderer type is UniqueValuesRenderer
#                           (Pete Smyth - 20th November 2024 16:20)
# 
################################################################################

print("Beginning Process")
import arcpy, os, csv
from time import strftime, localtime

def main(folder, outputfile):
    """ Writes the file information to a csv file

    Args:
        folder (str): The top level folder to search for aprx files
        outputfile (str): Name of the csv file including path

    Returns:
        csv file containing all layers and layer information.
    """
    with open(outputfile, 'w', newline='') as f:
        w = csv.writer(f)
        header = ("Project Document", "APRX Path", "Map Name", "Layer name", "Layer Datasource", "has Labels", "Symbology Field")
        w.writerow(header)
        rows = crawlaprx(folder)
        w.writerows(rows)

def crawlaprx(folder):
    ''' Gets the Aprx Name, Aprx path, Map name, layer name, datasource name
    and whether the layer has labels.

    Args:
        folder (str): The top level folder to search for aprx files
            
    Returns:
        tuple: a tuple of strings representing the data related to the
        header columns.
    '''
    # Specify a list of folder names to ignore during processing
    excludesubfolders = (".backups","archive",".gdb")
    symField = []
    # Generate the file names in a directory tree by walking the tree either top-down or bottom-up.
    # For each directory in the tree rooted at directory top (including top itself),
    # it yields a 3-tuple (dirpath, dirnames, filenames).
    for root, dirs, files in os.walk(folder):
        # Troubleshooting Print statements. Uncomment to use.
        #print(f" Root:  {root}")
        #print(f" Directories:  {dirs}")
        #print(f" Files:  {files}")
        #
        # Iterate through list of files
        for f in files:
            # ensures specified subfolders are omitted from scan
            if not root.lower().endswith(excludesubfolders):
                # Troubleshooting Print statement. Uncomment to use.
                #print(f"    Starting processing of {f}")
                #
                # Checks if current file is an ArcGIS Project
                if f.lower().endswith(".aprx"):
                    aprxName = os.path.splitext(f)[0]
                    aprxPath = os.path.join(root, f)
                    aprx = arcpy.mp.ArcGISProject (aprxPath)
                    # Iterate through maps in project
                    for m in aprx.listMaps():
                        # Iterate through layers in layer list
                        for lyr in m.listLayers():
                            lyrName = lyr.name if lyr.supports("name") else print(f"      No layer name for {lyr}")#"N/A"
                            lyrDatasource = lyr.dataSource.split(',')[-1] if lyr.supports("dataSource") else "N/A"
                            mapName = m.name
                            hasLabels = lyr.showLabels if lyr.supports("SHOWLABELS") else "FALSE"
                            if lyr.supports("SYMBOLOGY"):
                                #symType = lyr.symbology.renderer.type
                                symField = lyr.symbology.renderer.fields if lyr.symbology.renderer.type == 'UniqueValueRenderer' else 'Uses other renderer type'
                            else:
                                symField = "Symbology not Supported"
                            seq = (aprxName, aprxPath, mapName, lyrName, lyrDatasource, hasLabels, symField);
                            yield seq
                    del aprx
                    print(f"    Finished processing {f}")
            # Troubleshooting Print statement. Uncomment to use.
            #print(f"    Ignoring {f} - not an APRX")
    print("Finished Process")

if __name__ == "__main__":
    folderPath = r"D:\Data\BCC\BCC_Common_Projects\BrisMAP_Utilities" # or arcpy.GetParameterAsText(0)
##    folderPath = r"D:\Data\BCC\Tools\python\source\DynamicServiceInfo" # or arcpy.GetParameterAsText(0)
    output = r"D:\Data\BCC\Tools\python\results\aprx_DataSource_dyn_" + str(strftime("%Y%m%d_%H%M%S")) + ".csv" # or arcpy.GetParameterAsText(1)
##    output = r"D:\Data\BCC\Tools\python\results\aprx_DataSource_dyn_" + str(strftime("%Y%m%d_%H%M%S")) + ".csv" # or arcpy.GetParameterAsText(1)
    main(folderPath, output)
