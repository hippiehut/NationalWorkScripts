import arcpy
import sys
import mysql.connector
from mysql.connector import errorcode

if len(sys.argv)<2:
    print "Specify state abbreviation."
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

def fieldExists(lname, fname):
    for f in [field.name for field in arcpy.ListFields(lname)]:
        if f == fname:
            return True
    return False

# use geographic coordinate system so output is latitude and longitude
outSr = arcpy.SpatialReference("NAD 1983 (2011)")

arcpy.env.outputCoordinateSystem = outSr

try:
    # list all dissolved layers
    print "Fetching layer list..."
    sys.stdout.flush()
    dList = arcpy.ListFeatureClasses("Parcels_*_Dissolved", "Polygon")
    
    for lyr in dList:
        fieldList = [field.name for field in arcpy.ListFields(lyr)]
        
        if not fieldExists(lyr, "PARCEL_LATITUDE"):
            print "Adding centroid geometry to " + lyr + "..."
            sys.stdout.flush()
            arcpy.AddGeometryAttributes_management(lyr, "CENTROID")
            print arcpy.GetMessages()
            sys.stdout.flush()

            print "Renaming fields for " + lyr + "..."
            sys.stdout.flush()
            arcpy.AlterField_management(lyr, "CENTROID_X", "PARCEL_LONGITUDE")
            print arcpy.GetMessages()
            sys.stdout.flush()
            arcpy.AlterField_management(lyr, "CENTROID_Y", "PARCEL_LATITUDE")
            print arcpy.GetMessages()
            sys.stdout.flush()

except arcpy.ExecuteError:
    print arcpy.GetMessages(2)
except Exception as ex:
    print ex.args[0]
