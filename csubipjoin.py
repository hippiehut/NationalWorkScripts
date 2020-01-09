import arcpy
import sys
import re
import mysql.connector
from mysql.connector import errorcode

if len(sys.argv)<3:
    print "Specify state abbreviation and layer list."
    sys.exit(1)

stateAbbrev = sys.argv[1]

if len(stateAbbrev) != 2:
    print "State abbreviations have exactly two characters.  Unlike what you typed."
    sys.exit(1)

dbUser =  "root"
dbPassword =  "jw4B1t0Sh"
dbHost =  "localhost"
dbDatabase =  "NATIONAL_BASE"
dbPort =  3392

destBase="D:/NationalWork/"

try:
    dbConn = mysql.connector.connect(user=dbUser, password=dbPassword,
        host=dbHost, database=dbDatabase, port=dbPort)
except mysql.connector.Error as exc:
    if exc.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print "Authentication failed."
    elif exc.errno == errorcode.ER_BAD_DB_ERROR:
        print "Invalid database."
    else:
        print exc
    sys.exit(1)
except Exception as exc:
    print exc.args[0]
    sys.exit(1)

stateQuery = ("SELECT STATE_NAME, FIPS_ID FROM NATIONAL_BASE.STATES "
    "WHERE STATE_ABBREV='" + stateAbbrev + "';")

dbQuery = dbConn.cursor()

dbQuery.execute(stateQuery)

rows = dbQuery.fetchone()

if rows is None:
    print "Unknown state."
    dbConn.close()
    sys.exit(1)

stateName = rows[0]
stateFips = rows[1]

gdb=destBase + stateFips + "_" + stateName.replace(" ", "_") + "/" + stateName + "_Layers.gdb"

arcpy.env.workspace = gdb

inputFile = sys.argv[2]

arcpy.env.overwriteOutput = True

# list of layers that should be joined
# e.g. Parcels_001_Albany_Albers
sjf = open(inputFile, "r")

llist = list()

for dline in sjf:
    layer = dline.rstrip("\n")
    llist.append(layer)

sjf.close()

try:
    print "Fetching list of layers..."
    sys.stdout.flush()
    featList = arcpy.ListFeatureClasses("*", "Polygon")

    csList = list() # completed CSub layers
    ipList = list() # completed IPC layers
    ccList = list() # complete CC layers
    
    for f in featList:
        if not re.search("(?i)parcels_.*_csub$", f) is None:
            csList.append(f)
        elif not re.search("(?i)parcels_.*_ipc$", f) is None:
            ipList.append(f)
        elif not re.search("(?i)parcels_.*_cc$", f) is None:
            ccList.append(f)
    
    for lyr in llist:
        joinLayer = stateName.replace(" ", "_") + "_County_Subdivision"

        targLayer = lyr
        
        destLayer = targLayer + "_CSub"

        if not destLayer in csList:
            print "Joining " + targLayer + " with County Subdivision..."
            sys.stdout.flush()

            fmaps = arcpy.FieldMappings()

            fmaps.addTable(targLayer)

            geoid = arcpy.FieldMap()

            geoid.addInputField(joinLayer, "GEOID")
            gout = geoid.outputField
            gout.name = "GEOID_CSUB"
            gout.aliasName = "GEOID_CSUB"
            geoid.outputField = gout

            fmaps.addFieldMap(geoid)

            print "Performing join..."
            sys.stdout.flush()

            arcpy.SpatialJoin_analysis(target_features=targLayer,
                join_features=joinLayer, out_feature_class=destLayer,
                join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL",
                match_option="HAVE_THEIR_CENTER_IN", field_mapping=fmaps)

            print arcpy.GetMessages()
            sys.stdout.flush()

        joinLayer = stateName.replace(" ", "_") + "_Incorporated_Place"

        targLayer = destLayer

        destLayer = targLayer + "_IPC"

        if not destLayer in ipList:
            print "Joining " + targLayer + " with Incorporated Place..."
            sys.stdout.flush()

            fmaps = arcpy.FieldMappings()

            fmaps.addTable(targLayer)

            geoid = arcpy.FieldMap()

            geoid.addInputField(joinLayer, "GEOID")
            gout = geoid.outputField
            gout.name = "GEOID_IPC"
            gout.aliasName = "GEOID_IPC"
            geoid.outputField = gout

            fmaps.addFieldMap(geoid)

            arcpy.SpatialJoin_analysis(target_features=targLayer,
                join_features=joinLayer, out_feature_class=destLayer,
                join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL",
                match_option="HAVE_THEIR_CENTER_IN", field_mapping=fmaps)

            print arcpy.GetMessages()
            sys.stdout.flush()

        joinLayer = stateName.replace(" ", "_") + "_Consolidated_City"

        if not joinLayer in featList:
            print "No Consolidated City layer to join."
        else:
            targLayer = destLayer
    
            destLayer = targLayer + "_CC"
    
            if not destLayer in ccList:
                print "Joining " + targLayer + " with Consolidated City..."
                sys.stdout.flush()
    
                fmaps = arcpy.FieldMappings()
    
                fmaps.addTable(targLayer)

                geoid = arcpy.FieldMap()
    
                geoid.addInputField(joinLayer, "GEOID")
                gout = geoid.outputField
                gout.name = "GEOID_CC"
                gout.aliasName = "GEOID_CC"
                geoid.outputField = gout
    
                fmaps.addFieldMap(geoid)
    
                arcpy.SpatialJoin_analysis(target_features=targLayer,
                    join_features=joinLayer, out_feature_class=destLayer,
                    join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL",
                    match_option="HAVE_THEIR_CENTER_IN", field_mapping=fmaps)
    
                print arcpy.GetMessages()
                sys.stdout.flush()

except arcpy.ExecuteError:
    print arcpy.GetMessages(2)
except Exception as ex:
    print ex.args[0]
