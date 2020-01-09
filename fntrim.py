import arcpy
import sys
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

class FixLayer:
    def __init__(self, layerName, trimStrings):
        self.layerName = layerName
        self.trimStrings = trimStrings

        self.valid = self.FindLayer()
        
    def FindLayer(self):
        if featList is None:
            print "No feature list present."
            exit(1)

        if self.layerName in featList:
            return True
        else:
            return False

def DupeFree(startName, fieldList):
    ndd = 0
    rval = startName
    while rval in fieldList:
        ndd += 1
        rval = startName + "_" + str(ndd)
    return rval

# expect file formatted like this:
# Parcels_001_County_Name|<string_to_remove>[;string_to_remove]
cf = open(inputFile, "r")

llist = list()

print "Fetching layer list..."
sys.stdout.flush()
featList = arcpy.ListFeatureClasses("Parcels_*", "Polygon")

for dline in cf:
    la = dline.rstrip("\n").split("|")

    lname = la[0]
    
    sa = la[1].split(";")
    
    lyr = FixLayer(lname, sa)

    if lyr.valid:
        llist.append(lyr)

cf.close()
        
try:
    for l in llist:
        print "Checking " + l.layerName + "..."
        sys.stdout.flush()
        fieldList = [field.name for field in arcpy.ListFields(l.layerName)]
        for f in fieldList:
            newName = f
            for s in l.trimStrings:
                newName = newName.replace(s, "") 
            if not newName == f:
                newName = DupeFree(newName, fieldList)
                print "Renaming " + f + " to " + newName + "..."
                sys.stdout.flush()
                arcpy.AlterField_management(in_table=l.layerName, field=f, new_field_name=newName, new_field_alias=newName)
                print arcpy.GetMessages()
                sys.stdout.flush()
                
except arcpy.ExecuteError:
    print arcpy.GetMessages(2)
except Exception as ex:
    print ex.args[0]
