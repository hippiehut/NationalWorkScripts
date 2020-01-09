import arcpy
import sys
import re
import errno
import mysql.connector

if len(sys.argv)<3:
    print("Specify state abbreviation and layer list.")
    sys.exit(1)

stateAbbrev = sys.argv[1]

if len(stateAbbrev) != 2:
    print("State abbreviations have exactly two characters.  Unlike what you typed.")
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
        print("Authentication failed.")
    elif exc.errno == errorcode.ER_BAD_DB_ERROR:
        print("Invalid database.")
    else:
        print(exc)
    sys.exit(1)
except Exception as exc:
    print(exc.args[0])
    sys.exit(1)

stateQuery = ("SELECT STATE_NAME, FIPS_ID FROM NATIONAL_BASE.STATES "
    "WHERE STATE_ABBREV='" + stateAbbrev + "';")

dbQuery = dbConn.cursor()

dbQuery.execute(stateQuery)

rows = dbQuery.fetchone()

if rows is None:
    print("Unknown state.")
    dbConn.close()
    sys.exit(1)

stateName = rows[0]
stateFips = rows[1]

gdb=destBase + stateFips + "_" + stateName.replace(" ", "_") + "/" + stateName + "_Layers.gdb"

arcpy.env.workspace = gdb

inputFile = sys.argv[2]

class County:
    def __init__(self, cfips, kfield):
        self.countyFips = cfips
        self.keyField = kfield

        self.layerMask = "Parcels_" + self.countyFips + "_*Albers*"
        self.layerName = None
        self.dissolveLayer = None

        self.valid = self.FindLayer()
        
    def FindLayer(self):
        maxlen = 0
        lmax = None

        if featList is None:
            print("No feature list present.")
            exit(1)

        # assume longest layer name with "Albers" is correct
        for f in featList:
            # ignore dissolved layers
            if f.upper().find("DISSOLVE") >= 0:
                continue

            # do regex match based on wildcard
            if not re.search("(?i)" + self.layerMask.replace(".", "\.").replace("*", ".*").replace("?", "."), f) is None:
                clen = len(f)
                if clen > maxlen:
                    lmax = f
                    maxlen = clen

        if not lmax is None:
            self.layerName = lmax
            self.dissolveLayer = self.layerName + "_Dissolved"
            return True
        else:
            print("Layer for " + cfips + " not found.")
            return False

outSr = arcpy.SpatialReference("NAD 1983 (2011) Contiguous USA Albers")

arcpy.env.outputCoordinateSystem = outSr

# expect file formatted like this:
# 001_County_Name=keyfield
cf = open(inputFile, "r")

clist = list()

print("Fetching layer list...")
sys.stdout.flush()
featList = arcpy.ListFeatureClasses("Parcels_*", "Polygon")

for dline in cf:
    ca = dline.rstrip("\n").split("=")

    cfa = ca[0].split("_")
    
    cfips = cfa[1]
    
    kfield = ca[1]

    cty = County(cfips, kfield)

    if cty.valid:
        clist.append(cty)

cf.close()

dList = list()

# store existing dissolved layers
for f in featList:
    if f.upper().find("DISSOLVE") >= 0:
        dList.append(f)

try:
    for c in clist:
        if not c.dissolveLayer in dList:
            print("Dissolving " + c.layerName + " to " + c.dissolveLayer + "...")
            sys.stdout.flush()
            arcpy.Dissolve_management(c.layerName, c.dissolveLayer, c.keyField)
            print(arcpy.GetMessages())
            sys.stdout.flush()

except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
except Exception as ex:
    print(ex.args[0])
