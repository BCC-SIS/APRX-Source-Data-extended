# APRX-Source-Data-extended

Title:            APRX_Source_Data_extended_3_6_01.py
Description:      This script is an extension of APRX_Source_Data_3_6_02.py
                  and crawls a supplied directory and lists all the following
                  information for any APRX in that directory:
                  
                  - Project Name
                  - Project Path
                  - Map name/s
                  - Layer names
                  - Layer Data Sources
                  - has Labels

Author:           Martin Best
Date:             01st August 2020

Required Modules: arcpy   Version 3.6(Installed with ArcGIS Pro)
                  os (native)
                  csv

Amendments:       3.6.01  Extended original APRX_Source_Data_3_6_02.py script
                          - added code to determine if layer has labels defined
                          (Pete Smyth - 24th May 2022 08:2
