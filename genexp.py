# Generate ogr2ogr commands to export data from geodatabase to MySQL

import sys
import mysql.connector
from mysql.connector import errorcode

if len(sys.argv)<2:
    print "Specify state abbreviation and layer list file."
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

dbName = "NATIONAL_" + stateFips

gdb=destBase + stateFips + "_" + stateName.replace(" ", "_") + "/" + stateName + "_Layers.gdb"

inputFile = sys.argv[2]

lfile = open(inputFile, "r")

ofile = open("pexp.cmd", "w")

ofile.write("@echo off\n")

cmdbase = ( "ogr2ogr -a_srs EPSG:6350 -s_srs EPSG:6350 -nlt MULTIPOLYGON -nln %TABLE% -overwrite -skipfailures "
           "-f MYSQL MYSQL:" + dbName + ",host=" + dbHost + ",port=" + str(dbPort) + ",user=" + dbUser + 
           ",password=" + dbPassword + " \"" + gdb + "\" %LAYER%" ) 

ld = dict()

for dline in lfile:
    data = dline.rstrip("\n").strip()
    da = data.split("|")
    layer = da[0]
    table = da[1]
    ld[layer] = table

lfile.close()

clist = list()

for lyr, tbl in ld.items():
    cmdline = cmdbase.replace("%TABLE%", tbl).replace("%LAYER%", lyr)
    clist.append(cmdline)
    
clist.sort()

for c in clist:
    ofile.write(c + "\n")
    
ofile.close()
