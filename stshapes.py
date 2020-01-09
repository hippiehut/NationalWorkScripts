import arcpy
import sys
import mysql.connector
from mysql.connector import errorcode

if len(sys.argv)<2:
    print "Specify state abbreviation."
    sys.exit(1)

stateAbbrev=sys.argv[1]

if len(stateAbbrev) != 2:
    print "State abbreviations have exactly two characters.  Unlike what you typed."
    sys.exit(1)

dbUser =  "root"
dbPassword =  "jw4B1t0Sh"
dbHost =  "localhost"
dbDatabase =  "NATIONAL_BASE"
dbPort =  3392

srcGdb="D:/GISData/Boundary/tlgdb_2019_a_us_substategeo.gdb"

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

createQuery = ("CREATE DATABASE IF NOT EXISTS NATIONAL_" + stateFips + ";")

print "Creating MySQL database (if it doesn't exist)..."
sys.stdout.flush()

dbQuery.execute(createQuery)

dbQuery.close()

dbConn.close()

srcLayers = list()

srcLayers.append("State")
srcLayers.append("County")
srcLayers.append("County_Subdivision")
srcLayers.append("Incorporated_Place")
srcLayers.append("Consolidated_City")

destGdb=destBase + stateFips + "_" + stateName.replace(" ", "_") + "/" + stateName + "_Layers.gdb"

outSr = arcpy.SpatialReference("NAD 1983 (2011) Contiguous USA Albers")

arcpy.env.workspace = srcGdb
arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = outSr

selLayer="curSelLayer"

try:
    if not arcpy.Exists(destGdb):
        print "Creating file geodatabase " + destGdb + "..."
        sys.stdout.flush()
        ga = destGdb.replace("\\", "/").split("/")
        gdbPath = ga[0]
        for p in xrange(1, len(ga)-1):
            gdbPath += "/" + ga[p]
        gdbName = ga[len(ga)-1]
        arcpy.CreateFileGDB_management(gdbPath, gdbName)
        print arcpy.GetMessages()
        sys.stdout.flush()

    for srcLayer in srcLayers:
        outLayer=destGdb + "/" + stateName.replace(" ", "_") + "_" + srcLayer

        print "Selecting " + stateName + " from " + srcLayer + "..."
        sys.stdout.flush()
        arcpy.MakeFeatureLayer_management(srcLayer, selLayer)
        print arcpy.GetMessages()
        sys.stdout.flush()

        arcpy.SelectLayerByAttribute_management(selLayer, 'NEW_SELECTION', '"GEOID" LIKE ' + "'" + stateFips + "%'")
        print arcpy.GetMessages()
        sys.stdout.flush()

        lcres = arcpy.GetCount_management(selLayer)
        if int(lcres[0]) == 0:
            print "No matching features from " + srcLayer
            continue

        print "Exporting " + stateName + " from " + srcLayer + "..."
        sys.stdout.flush()
        arcpy.CopyFeatures_management(selLayer, outLayer)
        print arcpy.GetMessages()

except arcpy.ExecuteError:
    print arcpy.GetMessages(2)
except Exception as ex:
    print ex.args[0]
