import arcpy
import sys
import mysql.connector
from mysql.connector import errorcode

if len(sys.argv)<3:
    print "Specify state abbreviation and join layer list."
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

class County:
    def __init__(self, cname, cfips, pField, jField, cField):
        self.countyName = cname
        self.countyFips = cfips
        self.parcelField = pField
        self.joinField = jField
        self.checkField = cField

        self.layerName = "Parcels_" + self.countyFips + "_" + self.countyName + "_Albers"

        self.joinLayer = "Points_" + self.countyFips + "_" + self.countyName + "_Albers"

        self.destLayer = self.layerName + "_Joined"

        self.indexName = self.parcelField + "_IDX"
        self.joinIndexName = self.joinField + "_IDX"

    def Label(self):
        rval = self.countyFips + "_" + self.countyName
        return rval

# expects file with join field information
# 001_Albany|PARCELFIELD|JOINFIELD|CHECKFIELD
ajf = open(inputFile, "r")

clist = list()

for dline in ajf:
    da = dline.rstrip("\n").split("|")

    cval = da[0]
    pfield = da[1]
    jfield = da[2]

    ca = cval.split("_")

    cfips=ca[1]
    cname=ca[2]

    for cr in ca[3:]:
        cname = cname + "_" +cr

    cty = County(cname, cfips, jfield)

    clist.append(cty)

try:
    print "Fetching list of layers..."
    sys.stdout.flush()
    jList = arcpy.ListFeatureClasses("Parcels_*_Joined", "Polygon")

    for c in clist:
        idxList = [idx.name for idx in arcpy.ListIndexes(c.layerName)]

        # add index on parcel ID field to original layer
        if not c.indexName in idxList:
            print "Adding index on " + c.parcelField + " to " + c.layerName + "..."
            sys.stdout.flush()
            arcpy.AddIndex_management(c.layerName, c.parcelField, c.indexName)
            print arcpy.GetMessages()
            sys.stdout.flush()

        # copy source layer to destination layer
        if not c.destLayer in jList:
            print "Copying " + c.layerName + " to " + c.destLayer + "..."
            sys.stdout.flush()
            arcpy.CopyFeatures_management(c.layerName, c.destLayer)
            print arcpy.GetMessages()
            sys.stdout.flush()

        idxList = [idx.name for idx in arcpy.ListIndexes(c.destLayer)]

        # add index on parcel ID field to destination layer
        if not c.indexName in idxList:
            print "Adding index on " + c.parcelField + " to " + c.destLayer + "..."
            sys.stdout.flush()
            arcpy.AddIndex_management(c.destLayer, c.parcelField, c.indexName)
            print arcpy.GetMessages()
            sys.stdout.flush()

        idxList = [idx.name for idx in arcpy.ListIndexes(c.joinLayer)]

        # add index on join field to join layer
        if not c.joinIndexName in idxList:
            print "Adding index on " + c.joinField + " to " + c.joinLayer + "..."
            sys.stdout.flush()
            arcpy.AddIndex_management(c.joinLayer, c.joinField, c.joinIndexName)
            print arcpy.GetMessages()
            sys.stdout.flush()

        fieldList = [field.name for field in arcpy.ListFields(c.destLayer)]

        # if check field not present, join hasn't been completed
        if not c.checkField in fieldList:
            print "Joining " + c.layerName + " to " + c.joinLayer + "..."
            sys.stdout.flush()
            arcpy.JoinField_management(c.destLayer, c.parcelField, c.joinLayer, c.joinField)
            print arcpy.GetMessages()
            sys.stdout.flush()

except arcpy.ExecuteError:
    print arcpy.GetMessages(2)
except Exception as ex:
    print ex.args[0]
