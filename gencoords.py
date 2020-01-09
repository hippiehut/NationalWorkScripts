# Generate SQL to create COORDS_999 table

import sys
import mysql.connector
from mysql.connector import errorcode

if len(sys.argv)<4:
    print "Specify state abbreviation, layer list file, and parcel ID file."
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

layerFile = sys.argv[2]
idFile = sys.argv[3]

iql = list()

iql.append("DROP TABLE IF EXISTS " + dbName + ".COORDS_999;\n")
iql.append("CREATE TABLE " + dbName + ".COORDS_999 LIKE NATIONAL_BASE.COORDS_DISSOLVED_TEMPLATE;\n")

qbase = ( "INSERT IGNORE INTO " + dbName + ".COORDS_999 (PARCEL_ID, STATE_FIPS, "
          "COUNTY_FIPS, PARCEL_LATITUDE, PARCEL_LONGITUDE, PARCEL_SHAPE, "
          "PARCEL_ENVELOPE, PARCEL_CENTROID) SELECT CONCAT('%SFIPS%%CFIPS%', '_', "
          "%PFIELD%), '%SFIPS%', '%CFIPS%', PARCEL_LATITUDE, PARCEL_LONGITUDE, "
          "SHAPE, ENVELOPE(SHAPE), CENTROID(SHAPE) FROM " + dbName + ".%TNAME%;\n" )

ofile = open("gencoords.sql", "w")

for q in iql:
    ofile.write(q)

# layer list file as output by layerlist.py 
lfile = open(layerFile, "r")

tlist = list()
pdict = dict()

for dline in lfile:
    data = dline.rstrip("\n").strip()
    da = data.split("|")
    table = da[1]
    if table.upper().find("DISSOLVED") > 0:
        tlist.append(table)

lfile.close()

lfile = open(idFile, "r")

for dline in lfile:
    data = dline.rstrip("\n").strip()
    da = data.split("=")
    ca = da[0].split("_")
    cfips = ca[1]
    pfield = da[1]
    pdict[cfips] = pfield

for t in tlist:
    ta = t.split("_")
    cfips = ta[1]
    qstring = qbase.replace("%TNAME%", t).replace("%CFIPS%", cfips).replace("%SFIPS%", stateFips).replace("%PFIELD%", pdict[cfips])
    ofile.write(qstring)

ofile.close()
