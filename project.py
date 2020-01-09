import arcpy
import sys
import re
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

arcpy.env.overwriteOutput = True

outSr = arcpy.SpatialReference("NAD 1983 (2011) Contiguous USA Albers")

print "Fetching layer list..."
sys.stdout.flush()
featList = arcpy.ListFeatureClasses("*") 

# get a list of all point and polygon layers using standard naming conventions

ptLayers = list()
shLayers = list()

for f in featList:
    if not re.search("(?i)points_.*", f) is None:
        ptLayers.append(f)
    elif not re.search("(?i)parcels_.*", f) is None:
        shLayers.append(f)

# get a list of all already-projected layers, to avoid duplicating work

ptdLayers = list()
shdLayers = list()

for f in featList:
    if not re.search("(?i)points_.*_albers", f) is None:
        ptdLayers.append(f)
    elif not re.search("(?i)parcels_.*_albers", f) is None:
        shdLayers.append(f) 

try:
    for ptc in ptLayers:
        destLayer=ptc + "_Albers"
        if destLayer in ptdLayers:
            continue

        print "Projecting " + ptc + "..."
        sys.stdout.flush()
        arcpy.Project_management(ptc, destLayer, outSr)
        print arcpy.GetMessages()
        sys.stdout.flush()

    for shc in shLayers:
        destLayer=shc + "_Albers"
        if destLayer in shdLayers:
            continue

        print "Projecting " + shc + "..."
        sys.stdout.flush()
        arcpy.Project_management(shc, destLayer, outSr)
        print arcpy.GetMessages()
        sys.stdout.flush()

except arcpy.ExecuteError:
    print arcpy.GetMessages(2)
except Exception as ex:
    print ex.args[0]
