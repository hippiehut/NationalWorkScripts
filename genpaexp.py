# Generate SQL for parcels export

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

dbName = "NATIONAL_" + stateFips

qlist = list()

qlist.append("DROP TABLE IF EXISTS " + dbName + ".PARCELS_EXPORT;\n")
qlist.append( ( "CREATE TABLE " + dbName + ".PARCELS_EXPORT\n"
                "(\n"
                "    OBJECTID            INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,\n"
                "    SHAPE               GEOMETRY,\n"
                "    PARCEL_ID           VARCHAR(128),\n"
                "    STATE_FIPS          CHAR(2),\n"
                "    COUNTY_FIPS         CHAR(3),\n"
                "    STREET_ADDRESS      VARCHAR(128)\n"
                ") Engine=MyISAM, CHARACTER SET utf8;\n" ) )
                
qlist.append( ( "INSERT INTO " + dbName + ".PARCELS_EXPORT (SHAPE, PARCEL_ID, "
                "STATE_FIPS, COUNTY_FIPS, STREET_ADDRESS)\n"
                "SELECT CTA.PARCEL_SHAPE, CTA.PARCEL_ID, CTA.STATE_FIPS, CTA.COUNTY_FIPS, "
                "DTA.PARCEL_ADDRESS\n"
                "FROM " + dbName + ".COORDS_999 CTA LEFT JOIN " + dbName + 
                ".NORMAL_999 DTA USING(PARCEL_ID);\n" ) )

ofile = open("paexp.sql", "w")

for q in qlist:
    ofile.write(q)

ofile.close()

cmdbase = ( "ogr2ogr.exe -nlt MULTIPOLYGON -overwrite -skipfailures -a_srs EPSG:6350 "
            "-s_srs EPSG:6350 -f FileGDB \"%PGDB%\" -nln parcels MYSQL:" + dbName + 
            ",host=" + dbHost + ",port=" + str(dbPort) + ",user=" + dbUser + 
            ",password=" + dbPassword + " PARCELS_EXPORT\n" )

cmdlist = list()

cmdlist.append("@echo off\n")
cmdlist.append(cmdbase.replace("%PGDB%", pgdb))

ofile = open("paexp.cmd", "w")

for c in cmdlist:
    ofile.write(c)
    
ofile.close()
