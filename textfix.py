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

arcpy.env.workspace = gdb

arcpy.env.overwriteOutput = True

# list of layers that should be fixed
# e.g. Parcels_001_Albany_Albers
sjf = open(inputFile, "r")

llist = list()

for dline in sjf:
    layer = dline.rstrip("\n")
    llist.append(layer)

sjf.close()

try:

    print "Fetching layer list..."
    sys.stdout.flush()
    
    featList = arcpy.ListFeatureClasses("*_Albers")

    for inLayer in llist:
        if inLayer.find("_Fixed") > 0:
            continue
        
        outLayer = inLayer.replace("_Albers", "_Fixed_Albers")

        if outLayer in featList:
            continue

        print "Processing " + inLayer + "..."
        sys.stdout.flush()

        lpath = arcpy.env.workspace + "/" + inLayer

        fd = dict()

        fms = arcpy.FieldMappings()

        fieldList = arcpy.ListFields(inLayer)
    
        for f in fieldList:
            if f.name.upper() == "SHAPE" or f.name.upper() == "OBJECTID":
                continue
    
            print "Setting mapping for " + f.name
            sys.stdout.flush()
    
            fd[f.name] = arcpy.FieldMap()
    
            fd[f.name].addInputField(lpath, f.name)
    
            of = fd[f.name].outputField
    
            of.type = f.type

            print of.type

            if of.type == "String":
                if of.length >= 8000:
                    of.length = 500
                
            print "Output name = " + of.name
            sys.stdout.flush()

            print "Output type = " + of.type
            sys.stdout.flush()
                
            print "Output size = " + str(of.length)
            sys.stdout.flush()
    
            fd[f.name].outputField = of
    
            fms.addFieldMap(fd[f.name])
    
        print "Exporting to reduce field size..."
        sys.stdout.flush()
        arcpy.FeatureClassToFeatureClass_conversion(in_features=inLayer,
            out_path=arcpy.env.workspace, out_name=outLayer, field_mapping=fms)
        print arcpy.GetMessages()
        sys.stdout.flush()

except arcpy.ExecuteError:
    print arcpy.GetMessages(2)
except Exception as ex:
    print ex.args[0]
