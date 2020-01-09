# Add state and county FIPS codes to dissolved layers

import arcpy
import sys
import errno
import mysql.connector

def fieldExists(lname, fname):
    for f in [field.name for field in arcpy.ListFields(lname)]:
        if f == fname:
            return True
    return False

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

layerFile = sys.argv[2]

cfile = open(layerFile, "r")

cdict = dict()
clist = list()

for dline in cfile:
    data = dline.rstrip("\n").strip()
    if not data.upper().find("DISSOLVED") > 0:
        continue
    da = data.split("|")
    layer = da[0]
    ca = layer.split("_")
    cfips = ca[1]
    cdict[cfips]=layer
    clist.append(cfips)
    
cfile.close()

clist.sort()

try:
    for c in clist:
        if not fieldExists(cdict[c], "STATE_FIPS"):
            print "Adding state FIPS field to " + cdict[c] + "..."
            sys.stdout.flush()
            arcpy.AddField_management(cdict[c], "STATE_FIPS", "TEXT", 0, 0, 2)
            print arcpy.GetMessages()
            sys.stdout.flush()
        if not fieldExists(cdict[c], "COUNTY_FIPS"):
            print "Adding county FIPS field to " + cdict[c] + "..."
            sys.stdout.flush()
            arcpy.AddField_management(cdict[c], "COUNTY_FIPS", "TEXT", 0, 0, 3)
            print arcpy.GetMessages()
            sys.stdout.flush()
        print "Calculating state FIPS values..."
        sys.stdout.flush()
        arcpy.CalculateField_management(cdict[c], "STATE_FIPS", "'" + stateFips + "'", "PYTHON")
        print arcpy.GetMessages()
        sys.stdout.flush()
        print "Calculating county FIPS values..."
        sys.stdout.flush()
        arcpy.CalculateField_management(cdict[c], "COUNTY_FIPS", "'" + c + "'", "PYTHON")
        print arcpy.GetMessages()

except arcpy.ExecuteError:
    print arcpy.GetMessages(2)
except Exception as ex:
    print ex.args[0]
