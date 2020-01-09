# Generate SQL to create original and template tables for field mapping

import sys
import glob
import mysql.connector
from mysql.connector import errorcode

if len(sys.argv)<3:
    print "Specify state abbreviation and unique fields file."
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

unFile = sys.argv[2]

dbName = "NATIONAL_" + stateFips

cfile = open(unFile, "r")

kdict = dict()

for dline in cfile:
    ca = dline.rstrip("\n").split("=")

    cfa = ca[0].split("_")
    
    cfips = cfa[1]
    
    kfield = ca[1]

    kdict[cfips] = kfield

cfile.close()

iqbase = ( "INSERT IGNORE INTO NATIONAL_" + stateFips + ".%OTNAME% (%FLIST%) SELECT %FLIST% "
           "FROM NATIONAL_" + stateFips + ".PARCELS_%TFORM%;\n" )

flist = glob.glob("cr_*.sql")

orglist = list()

for f in flist:
    print "Processing " + f +  "..."
    sys.stdout.flush()

    ca = f.split("_")

    cfips = ca[2][:3]

    if not cfips in kdict.keys():
        print "Parcel ID field for " + f + " not specified."
        sys.stdout.flush()
        continue
    
    keyField = kdict[cfips]
   
    sfile = open(f, "r")

    fnlist = list()
    fdlist = list()    

    for l in sfile:
        data = l.rstrip("\n")
        if data.strip()[:6] == "CREATE":
            tval = data[data.find("TABLE `")+7:]
            tval = tval[:tval.find("`")]
            ta = tval.split("_")
            tbase = ta[0]
            tform = ta[1]
        elif data.strip()[:1] == "`":        
            fname = data[data.find("`")+1:]
            fname = fname[:fname.find("`")].upper()
            if fname[:10] == "JOIN_COUNT":
                pass
            elif fname[:10] == "TARGET_FID":
                pass
            elif fname == "OBJECTID":
                pass
            elif fname == "SHAPE":
                pass
            else:
                if fname == keyField.upper():
                    ka = data.replace("DEFAULT NULL", "").split(",")
                    odata = ka[0] + " PRIMARY KEY,"
                else:
                    odata = data
                odata = odata.replace("AUTO_INCREMENT", "")
                fnlist.append(fname)
                fdlist.append(odata)
    
    sfile.close()
    
    ftail = f[f.find("_")+1:]
    ftail = ftail[ftail.find("_")+1:]
    
    ofname = "org_" + ftail
    
    orglist.append(ofname)
    
    ofile = open(ofname, "w")
    
    tname = "ORIGINAL_TEMPLATE_" + tform

    oline = "DROP TABLE IF EXISTS " + dbName + "." + tname + ";\n"

    ofile.write(oline)
    
    otname = "ORIGINAL_" + tform
    
    oline = "DROP TABLE IF EXISTS " + dbName + "." + otname + ";\n"
    
    ofile.write(oline)
    
    ofile.write("\n")
    
    oline = "CREATE TABLE " + dbName + "." + tname + "\n"
    
    ofile.write(oline)

    ofile.write("(\n")
  
    flist = "`" + fnlist[0] + "`"
  
    for fdx in xrange(1, len(fnlist)):
        flist += ", `" + fnlist[fdx] + "`"
       
    for fdx in xrange(0, len(fdlist)):
        oline = fdlist[fdx]
        if fdx == len(fdlist)-1:
            oline = oline.replace(",", "")
        ofile.write(oline + "\n")
    
    ofile.write(") Engine=MyISAM, CHARACTER SET utf8;\n\n")
    
    oline = "CREATE TABLE " + dbName + "." + otname + " LIKE " + dbName + "." + tname + ";\n"

    ofile.write(oline)
    
    qstring = iqbase.replace("%TFORM%", tform).replace("%FLIST%", flist).replace("%OTNAME%", otname)
    
    ofile.write(qstring + "\n")
    
    ofile.close()

ofile = open("org_all.sql", "w")

for o in orglist:
    oline = "source " + o
    ofile.write(oline + "\n")

ofile.close()
