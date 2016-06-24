from IM_Climate_py.StationFinder import StationFinder
from IM_Climate_py.DataRequestor import DataRequestor


# STATION FINDER
localFolder = 'c:\\temp\\'
sf = StationFinder()

#Case #1: All stations around NOCA; default to 30km buffer
data = sf.findStation(unitCode = 'MABI')
data.export(localFolder + 'MABI_Stations.txt')

#Case #2: All stations around ACAD recording minimum temperature; distance = 10km
data = sf.findStation(unitCode = 'ACAD', distance = 10, parameter = 'mint')
data.export(localFolder + 'ACAD_minT_Stations.txt')

#Case 3: All stations around ROMO recording maximum temperature; distance = 40km
        #with option to save file
data = sf.findStation(unitCode = 'ROMO', distance = 40, parameter = 'maxt'
        ,filePathAndName = localFolder + 'ROMO_maxT_Stations.txt')

#Case #4: View Station Properties for station uid=4211
station = data[4211]
print station.name
print station.latitude
print station.longitude
print station.sids
print station.stateCode
print station.elev
print station.uid

#Case #5: View UnitCode Query Parameter
print data.metadata.queryParameters['unitCode']

#Case #6: Print first five station IDs
print data.stationIDs[0:5]


#******************************************************************************

# DATA REQUESTER

#Case #1: Get daily data for two station IDs (from list) and two parameters
# and save locally
stationIDs = [66176, 31746]
parameters = 'mint, maxt'
startDate = '2012-01-01'
endDate = '2012-02-01'
dr = DataRequestor()
wxData = dr.getDailyWxObservations(data, parameters
                            ,startDate= startDate, endDate = endDate)
wxData.export(filePathAndName = localFolder + 'Case02_dailyData.csv')


#Case #2: Get daily data using stationFinder object and one parameter
# and save locally
parameters = 'avgt'
wxData = dr.getDailyWxObservations(stationIDs, parameters
                            ,startDate= startDate, endDate = endDate)