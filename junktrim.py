import arcpy
import sys
import mysql.connector
from mysql.connector import errorcode

if len(sys.argv)<2:
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

selLayer = "JunkParcels"

try:
    # list all dissolved layers
    print "Fetching layer list..."
    sys.stdout.flush()
    dList = arcpy.ListFeatureClasses("Parcels_*_Dissolved", "Polygon")
    
    for lyr in dList:
        
        klist = list()

        # find all multipolygons with more than 1000 parts        
        for row in arcpy.da.SearchCursor(lyr, ["OID@", "SHAPE@"]):
            if row[1].partCount > 1000:
                print "Object ID " + str(row[0]) + " = " + str(row[1].partCount) + " parts, queued for kill"
                sys.stdout.flush()
                klist.append(str(row[0]))

        if len(klist) > 0:        
            oidField = arcpy.Describe(lyr).OIDFieldName
            
            qWhere = oidField + " IN ("
            
            for k in klist:
                qWhere += str(k) + ", "
                
            qWhere = qWhere[:len(qWhere)-2] + ")"
            
            arcpy.MakeFeatureLayer_management(lyr, selLayer)
            print "Selecting junk parcels..."
            sys.stdout.flush()
            arcpy.SelectLayerByAttribute_management(selLayer, 'NEW_SELECTION', qWhere)
            print "Deleting junk parcels..."
            sys.stdout.flush()
            arcpy.DeleteFeatures_management(selLayer)
            
except arcpy.ExecuteError:
    print arcpy.GetMessages(2)
except Exception as ex:
    print ex.args[0]

