# Generate table creation SQL files for parsing by orgparse

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

tableQuery = "SHOW TABLES FROM " + dbName + " LIKE 'PARCELS\\_%';"

dbQuery.execute(tableQuery)

tlist = list()

row = dbQuery.fetchone()

if row is None:
    print "No tables found."
    dbConn.close()
    sys.exit(1)

while row is not None:
    tlist.append(row[0])
    row = dbQuery.fetchone()

qcbase = "SHOW CREATE TABLE " + dbName + ".%TNAME%;"

for t in tlist:
    if t.upper().find("DISSOLVE") > 0:
        continue

    ofname = "cr_" + t + ".sql"
    
    qstring = qcbase.replace("%TNAME%", t)

    dbQuery.execute(qstring)

    ofile = open(ofname, "w")

    rows = dbQuery.fetchone()
    
    tdesc = rows[1]

    ofile.write(tdesc + "\n")
    
    ofile.close()

dbConn.close()
