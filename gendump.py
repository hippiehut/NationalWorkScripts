# Generate mysqldump command to dump tables

import sys
import mysql.connector
from mysql.connector import errorcode

if len(sys.argv)<3:
    print "Specify state abbreviation and county list file."
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

inFile = sys.argv[2]

cfile = open(inFile, "r")

cset = set()

for l in cfile:
    da = l.split("_")
    cfips = da[1]
    cset.add(cfips)
    
cfile.close()

clist = list()

for c in cset:
    clist.append(c)
    
clist.sort()

tlist = list()

for c in clist:
    tlist.append("NORMAL_" + c)
    
tlist.append("NORMAL_999")
tlist.append("COORDS_999")

ofile = open("dumpall.cmd", "w")

ofile.write("@echo off\n")

cmdbase = ( "mysqldump -u " + dbUser + " --password=" + dbPassword + 
            " --pipe " + dbName + " %TLIST% > " + stateAbbrev.lower() + "_national.sql\n" )

tls = ""

for t in tlist:
    tls += " " + t
    
cmdline = cmdbase.replace("%TLIST%", tls.strip())

ofile.write(cmdline)

ofile.close()
