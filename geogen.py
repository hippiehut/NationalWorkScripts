import sys
import glob
import mysql.connector
from mysql.connector import errorcode

if len(sys.argv)<2:
    print "Specify state abbreviation, and optionally CC county list file."
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

if len(sys.argv) == 3:
    ccfname = sys.argv[2]
else:
    ccfname = None

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

cclist = list()

if not ccfname is None:
    ccfile = open(ccfname, "r")
    for dline in ccfile:
        da = dline.split("_")
        cfips = da[1]
        cclist.append(cfips)
    ccfile.close()

olist = glob.glob("org_*.sql")

clist = list()

for o in olist:
    oa = o.split("_")
    cfa = oa[1].split(".")
    cfips = cfa[0]
    if cfips.isdigit():
        clist.append(cfips)
    
ofname = "geocorrect.sql"

ofile = open(ofname, "w")

aqbase="ALTER TABLE NATIONAL_18.ORIGINAL_%CFIPS% ADD COLUMN GEOID_CORRECT CHAR(10);"

ccqbase="UPDATE NATIONAL_%SFIPS%.ORIGINAL_%CFIPS% CTA LEFT JOIN " \
"NATIONAL_BASE.MUNIS_ALL MTA ON " \
"MTA.STATE_FIPS='%SFIPS%' AND " \
"MTA.COUNTY_FIPS='%CFIPS%' AND " \
"MTA.MUNI_FIPS=RIGHT(CTA.GEOID_CC, 5) " \
"SET CTA.GEOID_CORRECT=CTA.GEOID_CC " \
"WHERE CTA.GEOID_CORRECT IS NULL AND " \
"NOT CTA.GEOID_CC IS NULL AND " \
"NOT MTA.MUNI_FIPS IS NULL;"

ipcqbase="UPDATE NATIONAL_%SFIPS%.ORIGINAL_%CFIPS% CTA LEFT JOIN " \
"NATIONAL_BASE.MUNIS_ALL MTA ON " \
"MTA.STATE_FIPS='%SFIPS%' AND " \
"MTA.COUNTY_FIPS='%CFIPS%' AND " \
"MTA.MUNI_FIPS=RIGHT(CTA.GEOID_IPC, 5) " \
"SET CTA.GEOID_CORRECT=CTA.GEOID_IPC " \
"WHERE CTA.GEOID_CORRECT IS NULL AND " \
"NOT CTA.GEOID_IPC IS NULL AND " \
"NOT MTA.MUNI_FIPS IS NULL;"

csubqbase="UPDATE NATIONAL_%SFIPS%.ORIGINAL_%CFIPS% CTA LEFT JOIN " \
"NATIONAL_BASE.MUNIS_ALL MTA ON " \
"MTA.STATE_FIPS='%SFIPS%' AND " \
"MTA.COUNTY_FIPS='%CFIPS%' AND " \
"MTA.MUNI_FIPS=RIGHT(CTA.GEOID_CSUB, 5) " \
"SET CTA.GEOID_CORRECT=CTA.GEOID_CSUB " \
"WHERE CTA.GEOID_CORRECT IS NULL AND " \
"NOT CTA.GEOID_CSUB IS NULL AND " \
"NOT MTA.MUNI_FIPS IS NULL;"

for cfips in clist:
    qstring = aqbase.replace("%SFIPS%", stateFips).replace("%CFIPS%", cfips)
    ofile.write(qstring + "\n")
    if cfips in cclist:
        qstring = ccqbase.replace("%SFIPS%", stateFips).replace("%CFIPS%", cfips)
        ofile.write(qstring + "\n")
    qstring=ipcqbase.replace("%SFIPS%", stateFips).replace("%CFIPS%", cfips)
    ofile.write(qstring + "\n")
    qstring=csubqbase.replace("%SFIPS%", stateFips).replace("%CFIPS%", cfips)
    ofile.write(qstring + "\n")

ofile.close()
