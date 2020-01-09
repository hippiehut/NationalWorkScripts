# Add shape stat fields and indices to parcel geodatabase, then compact

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

pgdb = destBase + stateFips + "_" + stateName.replace(" ", "_") + "/P_" + stateFips + ".gdb"

arcpy.env.workspace = pgdb

def fieldExists(lname, fname):
    for f in [field.name for field in arcpy.ListFields(lname)]:
        if f == fname:
            return True
    return False

outSr = arcpy.SpatialReference("NAD 1983 (2011) Contiguous USA Albers")

arcpy.env.outputCoordinateSystem = outSr

layerName="parcels"

idxList = ["PARCEL_ID_IDX:PARCEL_ID", "COUNTY_FIPS_IDX:COUNTY_FIPS", "STREET_ADDRESS_IDX:STREET_ADDRESS"]

try:
    if not fieldExists(layerName, "Shape_Area"):
        print "Adding shape area to " + layerName + "..."
        sys.stdout.flush()
        arcpy.AddGeometryAttributes_management(layerName, "AREA")
        print arcpy.GetMessages()
        sys.stdout.flush()

        print "Renaming area field for " + layerName + "..."
        sys.stdout.flush()
        arcpy.AlterField_management(layerName, "POLY_AREA", "Shape_Area")
        print arcpy.GetMessages()
        sys.stdout.flush()

    if not fieldExists(layerName, "Shape_Length"):
        print "Adding shape length to " + layerName + "..."
        sys.stdout.flush()
        arcpy.AddGeometryAttributes_management(layerName, "PERIMETER_LENGTH")
        print arcpy.GetMessages()
        sys.stdout.flush()

        print "Renaming length field for " + layerName + "..."
        sys.stdout.flush()
        arcpy.AlterField_management(layerName, "PERIMETER", "Shape_Length")
        print arcpy.GetMessages()
        sys.stdout.flush()

    ida = [idx.name for idx in arcpy.ListIndexes(layerName)]

    for idx in idxList:
        ia = idx.split(':')
        iname = ia[0]
        ifield = ia[1]
        if not iname in ida:
            print "Adding index " + iname + "..."
            sys.stdout.flush()
            arcpy.AddIndex_management(layerName, ifield, iname)
            print arcpy.GetMessages()
            sys.stdout.flush()

    print "Setting coordinate system..."
    sys.stdout.flush()
    arcpy.DefineProjection_management(layerName, outSr)
    print arcpy.GetMessages()
    sys.stdout.flush()

    print "Compacting geodatabase..."
    sys.stdout.flush()
    arcpy.Compact_management(arcpy.env.workspace)
    print arcpy.GetMessages()
    sys.stdout.flush()

except arcpy.ExecuteError:
    print arcpy.GetMessages(2)
except Exception as ex:
    print ex.args[0]
