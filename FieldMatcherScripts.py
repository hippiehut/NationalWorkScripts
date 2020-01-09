from resowner import ResidentOwner
# siteAddress = !house_no!
siteAddress = !house_no! + " " + !street_nam!
ownerAddress1 = !address2!
# ownerAddress2 = !add2!
ownerCity = !city!

if ownerAddress2 != "":
	ownerAddress = ownerAddress2
else:
	ownerAddress = ownerAddress1

if ResidentOwner(ownerAddress, siteAddress):
	WTGFV.Value = ownerCity
else:
	WTGFV.Value = None

#=======


from resowner import ResidentOwner
siteAddress = !prop_street_number! + " " + !prop_street!
ownerAddress1 = !street!
ownerCity = !city!


if ResidentOwner(ownerAddress, siteAddress):
	WTGFV.Value = ownerCity
else:
	WTGFV.Value = None

#=======


from resowner import ResidentOwner
siteAddress = !loc_addres! 
ownerAddress = !addr1!
# ownerAddress2 = !address2!
ownerCity = !addr2!.replace(" PA","")

# if ownerAddress2.strip() != "":
# 	ownerAddress = ownerAddress2
# else:
# 	ownerAddress = ownerAddress1


if ResidentOwner(ownerAddress, siteAddress):
	WTGFV.Value = ownerCity
else:
	WTGFV.Value = None


#=======


# cityList = ["Poth", "Floresville", "Stockdale", "La Vernia", "Adkins", "San Antonio", "Falls City", "Mc Coy", "Nixon", "Pandora", "Sutherland Sprgs", "Pleasanton", "Elmendorf"]

cityList = ["Garwood", "Eagle Lake", "Columbus", "Weimar", "Altair", "Alleyton", "Chesterville", "Sheridan", "Rock Island" ]

addr = !calhoun_dbo_web_map_property_situs!
for x in cityList:
    if addr.lower().find(x.lower()) > 0:
        street = addr.lower().split(x.lower())[0]

if street:
    WTGFV.Value =  street.title()
else:
    WTGFV.Value = None

# ==========
from datetime import datetime

ms = int(WTGFV.Value)

if ms > 0:
    ts = ms / 1000 + (5 * 3600)
    dt = datetime.fromtimestamp(ts)
    dstring = dt.strftime("%m/%d/%Y")
    WTGFV.Value = dstring
else:
    WTGFV.Value = None
