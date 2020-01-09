from num2words import num2words

# convert all abbreviations, standard and non-standard, to full values
def MakeFull(inString):
    wstring = inString.upper()

    wstring = wstring.replace(".", "")

    if wstring == "E": rstring="EAST"
    elif wstring == "N": rstring="NORTH"
    elif wstring == "W": rstring="WEST"
    elif wstring == "S": rstring="SOUTH"
    elif wstring == "NO": rstring="NORTH"
    elif wstring == "SO": rstring="SOUTH"
    elif wstring == "ALY": rstring="ALLEY"
    elif wstring == "ANX": rstring="ANNEX"
    elif wstring == "APT": rstring="APARTMENT"
    elif wstring == "ARC": rstring="ARCADE"
    elif wstring == "AVE": rstring="AVENUE"
    elif wstring == "BSMT": rstring="BASEMENT"
    elif wstring == "BYU": rstring="BAYOU"
    elif wstring == "BCH": rstring="BEACH"
    elif wstring == "BND": rstring="BEND"
    elif wstring == "BLF": rstring="BLUFF"
    elif wstring == "BTM": rstring="BOTTOM"
    elif wstring == "BLVD": rstring="BOULEVARD"
    elif wstring == "BR": rstring="BRANCH"
    elif wstring == "BRG": rstring="BRIDGE"
    elif wstring == "BRK": rstring="BROOK"
    elif wstring == "BLDG": rstring="BUILDING"
    elif wstring == "BG": rstring="BURG"
    elif wstring == "BYP": rstring="BYPASS"
    elif wstring == "CP": rstring="CAMP"
    elif wstring == "CYN": rstring="CANYON"
    elif wstring == "CPE": rstring="CAPE"
    elif wstring == "CSWY": rstring="CAUSEWAY"
    elif wstring == "CTR": rstring="CENTER"
    elif wstring == "CIR": rstring="CIRCLE"
    elif wstring == "CLFS": rstring="CLIFFS"
    elif wstring == "CLB": rstring="CLUB"
    elif wstring == "COR": rstring="CORNER"
    elif wstring == "CORS": rstring="CORNERS"
    elif wstring == "CRSE": rstring="COURSE"
    elif wstring == "CT": rstring="COURT"
    elif wstring == "CTS": rstring="COURTS"
    elif wstring == "CV": rstring="COVE"
    elif wstring == "CRK": rstring="CREEK"
    elif wstring == "CRES": rstring="CRESCENT"
    elif wstring == "XING": rstring="CROSSING"
    elif wstring == "DL": rstring="DALE"
    elif wstring == "DM": rstring="DAM"
    elif wstring == "DEPT": rstring="DEPARTMENT"
    elif wstring == "DV": rstring="DIVIDE"
    elif wstring == "DR": rstring="DRIVE"
    elif wstring == "EST": rstring="ESTATE"
    elif wstring == "EXPY": rstring="EXPRESSWAY"
    elif wstring == "EXT": rstring="EXTENSION"
    elif wstring == "FLS": rstring="FALLS"
    elif wstring == "FRY": rstring="FERRY"
    elif wstring == "FLD": rstring="FIELD"
    elif wstring == "FLDS": rstring="FIELDS"
    elif wstring == "FLT": rstring="FLAT"
    elif wstring == "FL": rstring="FLOOR"
    elif wstring == "FRD": rstring="FORD"
    elif wstring == "FRST": rstring="FOREST"
    elif wstring == "FRG": rstring="FORGE"
    elif wstring == "FRK": rstring="FORK"
    elif wstring == "FRKS": rstring="FORKS"
    elif wstring == "FT": rstring="FORT"
    elif wstring == "FWY": rstring="FREEWAY"
    elif wstring == "FRNT": rstring="FRONT"
    elif wstring == "GDNS": rstring="GARDEN"
    elif wstring == "GDNS": rstring="GARDENS"
    elif wstring == "GTWY": rstring="GATEWAY"
    elif wstring == "GLN": rstring="GLEN"
    elif wstring == "GRN": rstring="GREEN"
    elif wstring == "GRV": rstring="GROVE"
    elif wstring == "HNGR": rstring="HANGER"
    elif wstring == "HBR": rstring="HARBOR"
    elif wstring == "HVN": rstring="HAVEN"
    elif wstring == "HTS": rstring="HEIGHTS"
    elif wstring == "HWY": rstring="HIGHWAY"
    elif wstring == "HL": rstring="HILL"
    elif wstring == "HLS": rstring="HILLS"
    elif wstring == "HOLW": rstring="HOLLOW"
    elif wstring == "INLT": rstring="INLET"
    elif wstring == "IS": rstring="ISLAND"
    elif wstring == "ISS": rstring="ISLANDS"
    elif wstring == "JCT": rstring="JUNCTION"
    elif wstring == "KY": rstring="KEY"
    elif wstring == "KNLS": rstring="KNOLL"
    elif wstring == "KNLS": rstring="KNOLLS"
    elif wstring == "LK": rstring="LAKE"
    elif wstring == "LKS": rstring="LAKES"
    elif wstring == "LNDG": rstring="LANDING"
    elif wstring == "LN": rstring="LANE"
    elif wstring == "LGT": rstring="LIGHT"
    elif wstring == "LF": rstring="LOAF"
    elif wstring == "LBBY": rstring="LOBBY"
    elif wstring == "LCKS": rstring="LOCK"
    elif wstring == "LCKS": rstring="LOCKS"
    elif wstring == "LDG": rstring="LODGE"
    elif wstring == "LOWR": rstring="LOWER"
    elif wstring == "MNR": rstring="MANOR"
    elif wstring == "MDWS": rstring="MEADOW"
    elif wstring == "MDWS": rstring="MEADOWS"
    elif wstring == "ML": rstring="MILL"
    elif wstring == "MLS": rstring="MILLS"
    elif wstring == "MSN": rstring="MISSION"
    elif wstring == "MT": rstring="MOUNT"
    elif wstring == "MTN": rstring="MOUNTAIN"
    elif wstring == "NCK": rstring="NECK"
    elif wstring == "OFC": rstring="OFFICE"
    elif wstring == "ORCH": rstring="ORCHARD"
    elif wstring == "PK": rstring="PIKE"
    elif wstring == "PKWY": rstring="PARKWAY"
    elif wstring == "PH": rstring="PENTHOUSE"
    elif wstring == "PNES": rstring="PINE"
    elif wstring == "PNES": rstring="PINES"
    elif wstring == "PL": rstring="PLACE"
    elif wstring == "PLN": rstring="PLAIN"
    elif wstring == "PLNS": rstring="PLAINS"
    elif wstring == "PLZ": rstring="PLAZA"
    elif wstring == "PT": rstring="POINT"
    elif wstring == "PRT": rstring="PORT"
    elif wstring == "PR": rstring="PRAIRIE"
    elif wstring == "RADL": rstring="RADIAL"
    elif wstring == "RNCH": rstring="RANCH"
    elif wstring == "RPDS": rstring="RAPID"
    elif wstring == "RPDS": rstring="RAPIDS"
    elif wstring == "RST": rstring="REST"
    elif wstring == "RDG": rstring="RIDGE"
    elif wstring == "RIV": rstring="RIVER"
    elif wstring == "RD": rstring="ROAD"
    elif wstring == "RM": rstring="ROOM"
    elif wstring == "RTE": rstring="ROUTE"
    elif wstring == "RT": rstring="ROUTE"
    elif wstring == "SHL": rstring="SHOAL"
    elif wstring == "SHLS": rstring="SHOALS"
    elif wstring == "SHR": rstring="SHORE"
    elif wstring == "SHRS": rstring="SHORES"
    elif wstring == "SPC": rstring="SPACE"
    elif wstring == "SPG": rstring="SPRING"
    elif wstring == "SPGS": rstring="SPRINGS"
    elif wstring == "SQ": rstring="SQUARE"
    elif wstring == "STA": rstring="STATION"
    elif wstring == "STRA": rstring="STRAVENUE"
    elif wstring == "STRM": rstring="STREAM"
    elif wstring == "ST": rstring="STREET"
    elif wstring == "STE": rstring="SUITE"
    elif wstring == "SMT": rstring="SUMMIT"
    elif wstring == "TER": rstring="TERRACE"
    elif wstring == "TRCE": rstring="TRACE"
    elif wstring == "TRAK": rstring="TRACK"
    elif wstring == "TRFY": rstring="TRAFFICWAY"
    elif wstring == "TRL": rstring="TRAIL"
    elif wstring == "TRLR": rstring="TRAILER"
    elif wstring == "TUNL": rstring="TUNNEL"
    elif wstring == "TPKE": rstring="TURNPIKE"
    elif wstring == "UN": rstring="UNION"
    elif wstring == "UPPR": rstring="UPPER"
    elif wstring == "VLY": rstring="VALLEY"
    elif wstring == "VIA": rstring="VIADUCT"
    elif wstring == "VW": rstring="VIEW"
    elif wstring == "VLG": rstring="VILLAGE"
    elif wstring == "VL": rstring="VILLE"
    elif wstring == "VIS": rstring="VISTA"
    elif wstring == "WAY": rstring="WAY"
    elif wstring == "WLS": rstring="WELL"
    elif wstring == "WLS": rstring="WELLS"
    elif wstring == "STR": rstring="STREET"
    elif wstring == "STRE": rstring="STREET"
    elif wstring == "STREE": rstring="STREET"
    elif wstring == "AVENU": rstring="AVENUE"
    elif wstring == "AVEN": rstring="AVENUE"
    elif wstring == "AV": rstring="AVENUE"
    elif wstring == "A": rstring="AVENUE"
    elif wstring == "BLV": rstring="BOULEVARD"
    elif wstring == "COUR": rstring="COURT"
    elif wstring == "COU": rstring="COURT"
    elif wstring == "CO": rstring="COURT"
    elif wstring == "CR": rstring="COURT"
    elif wstring == "RO": rstring="ROAD"
    elif wstring == "ROA": rstring="ROAD"
    elif wstring == "R": rstring="ROAD"
    elif wstring == "DRI": rstring="DRIVE"
    elif wstring == "DRIV": rstring="DRIVE"
    elif wstring == "DRV": rstring="DRIVE"
    elif wstring == "L": rstring="LANE"
    elif wstring == "LAN": rstring="LANE"
    elif wstring == "LA": rstring="LANE"
    elif wstring == "PLA": rstring="PLACE"
    elif wstring == "PLAC": rstring="PLACE"
    elif wstring == "CNTR": rstring="CENTER"
    elif wstring == "HWAY": rstring="HIGHWAY"
    elif wstring == "HIGHWA": rstring="HIGHWAY"
    elif wstring == "HIGHW": rstring="HIGHWAY"
    elif wstring == "HIG": rstring="HIGHWAY"
    elif wstring == "SQU": rstring="SQUARE"
    elif wstring == "SQR": rstring="SQUARE"
    elif wstring == "TERR": rstring="TERRACE"
    elif wstring == "TR": rstring="TERRACE"
    elif wstring == "TPK": rstring="TURNPIKE"
    elif wstring == "TNPK": rstring="TURNPIKE"
    elif wstring == "TNPIKE": rstring="TURNPIKE"
    elif wstring == "TURNPIK": rstring="TURNPIKE"
    elif wstring == "TURNPI": rstring="TURNPIKE"
    elif wstring == "TURNP": rstring="TURNPIKE"
    elif wstring == "TPIKE": rstring="TURNPIKE"
    elif wstring == "PKWAY": rstring="PARKWAY"
    elif wstring == "PWAY": rstring="PARKWAY"
    elif wstring[0].isdigit() and not wstring[-1:].isdigit():
        # convert numeric ordinal to alpha ordinal (e.g. 1ST = FIRST)
        nwstring = ""
        for c in wstring:
            if c.isdigit():
                nwstring += c
        rstring = num2words(nwstring, ordinal = True).upper()
    else:
        rstring = wstring

    return rstring;

# normalize address
# addr - address to normalize
# awords - number of words to preserve
# skipDir - skip pre-direction (e.g. "10 E MAIN" = "10 MAIN")
def FillAddress(addr, awords, skipDir = False):
    aa = addr.split(" ")

    rval = ""
        
    fwc = 0
    
    for a in aa:
        fwc += 1
        cw = MakeFull(a)
        # avoid preserving pre-direction in second word, if skipDir
        if fwc == 2 and skipDir:
            if cw == "NORTH" or cw == "SOUTH" or cw == "EAST" or cw == "WEST":
                continue
        rval += " " + cw
        # leave loop when specified number of words have been preserved
        if (not skipDir and fwc == awords) or (skipDir and fwc == awords+1):
            break

    rval = rval.strip()

    if fwc < 2: # one-word matches are useless
        rval = ""

    return rval

def ResidentOwner(oAddr, sAddr):
    siteAddr = sAddr.strip()
    ownerAddr = oAddr.strip()

    if siteAddr == "" or ownerAddr == "":
        return False

    if not siteAddr[0].isdigit() or not ownerAddr[0].isdigit():
        return False
    
    if siteAddr == ownerAddr:
        return True

    saddr = siteAddr
    
    while saddr.find("  ") >= 0:
        saddr = saddr.replace("  ", " ")
        
    oaddr = ownerAddr
        
    while oaddr.find("  ") >= 0:
        oaddr = oaddr.replace("  ", " ")

    sa = saddr.split(" ")
    oa = oaddr.split(" ")
    
    scount = len(sa)
    ocount = len(oa)

    if scount != ocount:
        if abs(scount - ocount) > 1:
            return False

        if scount < 2 or ocount < 2:
            return False

    compCount = min(scount, ocount)

    siteFilled = FillAddress(saddr, compCount)
    ownerFilled = FillAddress(oaddr, compCount)

    if siteFilled == ownerFilled:
        return True
    else:
        # try comparing without pre-direction
        siteFilled = FillAddress(saddr, compCount, True)
        ownerFilled = FillAddress(oaddr, compCount, True)

        if siteFilled == ownerFilled:
            return True
        else:
            return False

