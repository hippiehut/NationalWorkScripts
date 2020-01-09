import arcpy
import sys
import errno
import mysql.connector

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

def LayerSortVal(inString):
    sa = inString.split("_")
    cfips = sa[1]
    rval = cfips.zfill(3)
    return rval

olist = list()

try:
    # list all layers
    print "Fetching layer list..."
    sys.stdout.flush()
    featList = arcpy.ListFeatureClasses("Parcels_*", "Polygon")
    
    for lyr in featList:
        # assume incorporated place joins were done
        if lyr.find("_IPC") < 0:
            continue
        pa = lyr.split("_")
        cfips = pa[1]
        tname = "PARCELS_" + cfips.zfill(3)
        if lyr.find("Dissolved") > 0:
            tname += "_DISSOLVED"
        oline = lyr + "|" + tname + "\n"
        olist.append(oline)

    olist.sort(key=LayerSortVal)

    lfile = open("allLayers.txt", "w")
    
    for l in olist:
        lfile.write(l)
    
    lfile.close()

except arcpy.ExecuteError:
    print arcpy.GetMessages(2)
except Exception as ex:
    print ex.args[0]
