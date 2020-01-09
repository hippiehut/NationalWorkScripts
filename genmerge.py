# Generate SQL statements to merge normalized county tables into state table

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

ofile = open("stmerge.sql", "w")

qlist = list()

qlist.append("DROP TABLE IF EXISTS " + dbName + ".NORMAL_999;\n")
qlist.append("CREATE TABLE " + dbName + ".NORMAL_999 LIKE NATIONAL_BASE.NORMAL_TEMPLATE;\n")
qlist.append("ALTER TABLE " + dbName + ".NORMAL_999 DISABLE KEYS;\n")

for q in qlist:
    ofile.write(q)
    
qbase="INSERT INTO " + dbName + ".NORMAL_999 SELECT * FROM " + dbName + ".NORMAL_%CFIPS%;\n"

aqstring="ALTER TABLE " + dbName + ".NORMAL_999 ENABLE KEYS;\n"

for c in clist:
    qstring = qbase.replace("%CFIPS%", c)
    ofile.write(qstring)
    
ofile.write(aqstring)

ofile.close()
