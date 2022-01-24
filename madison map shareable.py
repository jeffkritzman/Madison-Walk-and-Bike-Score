# most pieces are working, just need to assemble the list? how to iterate through...

#############################################################################################################
#
# initial setup
#
#############################################################################################################
 
import json
import numpy as np
import matplotlib.pyplot as plt
import requests

daynum = 5 # 0, 1, 2, 3 for initial map

WSapikey = 'abc123'
bingAPIkey = 'abc123'
entities = 'naturalPOI' #parameter for bing



#############################################################################################################
#
# setup lat / lon matrix
#
#############################################################################################################

grain = .001 # granularity that we'll be looping through lat / lon coordinates
#longbinsize = 45 #how many degrees longitude (three decimals) to do in one day, due to API restrictions
#daynumoffset = 2
#daynumeff = daynum - daynumoffset #had some errors, changed lat / lon partitioning mid-stream

#latitude
minlat = 43.118 # orig 43.016 
maxlat = 43.137
latgrains = abs(round((maxlat - minlat) / grain)) + 1 #plus one, as inclusive of start and end
#print(latgrains)

#longitude
#minlonginit = -89.374 # orig -89.460
#maxlonginit = -89.294 # orig -89.294
minlong =  -89.505 #round(minlonginit + (longbinsize * daynumeff * grain), 3)
maxlong = -89.285 #round(minlonginit + (((longbinsize * (daynumeff+1)) - 1) * grain), 3)
#if maxlong > maxlonginit:
 #   maxlong = maxlonginit
#longgrains = longbinsize
longgrains = abs(round((maxlong - minlong) / grain)) + 1 #plus one, as inclusive of start and end



#############################################################################################################
#
# loop, call, print
#
############################################################################################################# 

#get file, prep
filename = "madisonMapTXT" + str(daynum) + ".txt"
mainfile = open(filename, "w") #purposefully want to overwrite, hence "w"
newline = "\n"
delim = ","

# write column header
mainfile.write("latitude,longitude,water,walkScore,bikeScore")
mainfile.write(newline)
errorlog = [] #initialize error log via empty list, to hold dictionaries

# loop through lat / lon combos
for x in range(longgrains):
    for y in range(latgrains):
        # loop through lat & lon
        try: 
            lat = str(round(minlat+ (grain * y), 3))
            lon = str(round(minlong+ (grain * x), 3))
            mainfile.write(str(lat) + delim + str(lon) + delim) # lat & lon
        except:
            mainfile.write(delim + delim)       
            error = "error: lat/lon"
            print(error) 
            errordict = {"x": x, "y": y, "error": error}
            errorlog.append(errordict)
        # call Bing Location API
        try: 
            bingcall = "https://dev.virtualearth.net/REST/v1/LocationRecog/" + lat + "," + lon + "?includeEntityTypes=" + entities + "&key=" + bingAPIkey
            bingresp = requests.get(bingcall)
            bingjson = bingresp.json()
            bingx = bingjson["resourceSets"][0]["resources"][0]["naturalPOIAtLocation"]
            if len(bingx) == 0:
                EntityType = ""
            else: 
                EntityType = bingx[0]["type"]
            mainfile.write(EntityType + delim) # write water
        except:
            mainfile.write(delim)       
            error = "error: bing"
            print(error) 
            errordict = {"x": x, "y": y, "error": error}
            errorlog.append(errordict)
        # Call walk score API
        try: 
            WSapicall = "https://api.walkscore.com/score?format=json&lat=" + lat + "&lon=" + lon + "&bike=1&wsapikey=" + WSapikey
            WSresponse = requests.get(WSapicall)
            WSjson = WSresponse.json() 
        except:
            WSjson = None       
            error = "error: ws API"
            print(error) 
            errordict = {"x": x, "y": y, "error": error}
            errorlog.append(errordict)
        # WRITE WALK SCORE
        try: 
            WalkScore = WSjson["walkscore"]
            mainfile.write(str(WalkScore) + delim)
        except:
            mainfile.write(delim)
            error = "error: walk score"
            print(error) 
            errordict = {"x": x, "y": y, "error": error}
            errorlog.append(errordict)
        # WRITE BIKE SCORE
        try: 
            BikeScore= WSjson["bike"]["score"]
            mainfile.write(str(BikeScore)) 
        except:
            mainfile.write("")
            error = "error: bike score"
            print(error) 
            errordict = {"x": x, "y": y, "error": error}
            errorlog.append(errordict)
        # WRITE NEW LINE
        mainfile.write(newline)
mainfile.close() 

print(len(errorlog))

for i in errorlog:
    print(i)



#############################################################################################################
#
# debugging
#
#############################################################################################################

print(daynum)
print(lat)
print(lon)
print(grain)
#print(daynumeff)
print(longgrains)
print(latgrains)
print(minlong)
print(maxlong)
print(minlat)
print(maxlat)

#use for development, eventually will use generated ranges
# lat = str(43.060)  
# lon = str(-89.394)
# lat / lon examples
#   lake: 43.060, -89.394
#   land: 43.117, -89.295
#   bike error: 43.079, -89.46

lat = str(43.044)
lon = str(-89.373)

bingcall = "https://dev.virtualearth.net/REST/v1/LocationRecog/" + lat + "," + lon + "?includeEntityTypes=" + entities + "&key=" + bingAPIkey
bingresp = requests.get(bingcall)
bingjson = bingresp.json()
bingx = bingjson["resourceSets"][0]["resources"][0]["naturalPOIAtLocation"]
if len(bingx) == 0:
    EntityType = ""
else: 
    EntityType = bingx[0]["type"]
print(EntityType + delim) # write water


#version 2
lat = str(43.044)
lon = str(-89.374)

try: 
    bingcall = "https://dev.virtualearth.net/REST/v1/LocationRecog/" + lat + "," + lon + "?includeEntityTypes=" + entities + "&key=" + bingAPIkey
    bingresp = requests.get(bingcall)
    bingjson = bingresp.json()
    bingx = bingjson["resourceSets"][0]["resources"][0]["naturalPOIAtLocation"]
    if len(bingx) == 0:
        EntityType = ""
    else: 
        EntityType = bingx[0]["type"]
    #print(1/0)
    print(EntityType + delim) # write water
except:
    print(delim) 