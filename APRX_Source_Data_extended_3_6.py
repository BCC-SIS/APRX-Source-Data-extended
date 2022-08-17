################################################################################
# Title:            APRX_Source_Data_extended_3_6_01.py
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
################################################################################
print("Beginning Process")
import arcpy, os, csv
from time import strftime, localtime

def main(folder, outputfile):
    with open(outputfile, 'w', newline='') as f:
        w = csv.writer(f)
        header = ("Project Document", "APRX Path", "Map Name", "Layer name", "Layer Datasource", "has Labels")
        w.writerow(header)
        rows = crawlaprx(folder)
        w.writerows(rows)

def crawlaprx(folder):
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(".aprx"):
                aprxName = os.path.splitext(f)[0]
                aprxPath = os.path.join(root, f)
                aprx = arcpy.mp.ArcGISProject (aprxPath)                
                for m in aprx.listMaps():
                    for lyr in m.listLayers():
                        lyrName = lyr.name
                        lyrDatasource = lyr.dataSource.split(',')[-1] if lyr.supports("dataSource") else "N/A"
                        mapName = m.name
                        hasLabels = lyr.showLabels if lyr.supports("SHOWLABELS") else "FALSE"
                        seq = (aprxName, aprxPath, mapName, lyrName, lyrDatasource, hasLabels);
                        yield seq
                del aprx
                print(f"Finished processing {f}")

if __name__ == "__main__":
    folderPath = r"D:\Data\BCC\Tools\python\source\DynamicServiceInfo" # or arcpy.GetParameterAsText(0)
    #folderPath = r"D:\Data\BCC\Tools\python\source\for_SEPModelling" # or arcpy.GetParameterAsText(0)
    #output = r"C:\Temp\Test_MXDs_for_Change\aprx_DataSource.csv" # or arcpy.GetParameterAsText(1)
    output = r"D:\Data\BCC\Tools\python\results\aprx_DataSource_dyn" + str(strftime("%Y%m%d_%H%M%S")) + ".csv" # or arcpy.GetParameterAsText(1)
    main(folderPath, output)
