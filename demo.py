from IM_Climate_py.StationFinder import StationFinder
from IM_Climate_py.DataRequestor import DataRequestor

'''
This demo script showcases the utility of the IM_Climate.py package
'''
#specify local folder where demo files will be saved
localFolder = 'c:\\temp\\'

#***************
# STATION FINDER
sf = StationFinder()

#Test #1: All stations around NOCA; default to 30km buffer. Save returned results
    #locally as SF01.csv
wxStations = sf.findStation(unitCode = 'MABI')
wxStations.export(localFolder + 'SF01.csv')

#Test #2: All stations around ACAD recording minimum temperature; distance = 10km
wxStations = sf.findStation(unitCode = 'ACAD', distance = 10, parameter = 'mint')
wxStations.export(localFolder + 'SF02.csv')

#Test 3: All stations around ROMO recording maximum OR minimum temperature; distance = 40km
        #with option to save file
wxStations = sf.findStation(unitCode = 'ROMO', distance = 40, parameter = 'maxt, mint'
        ,filePathAndName = localFolder + 'SF03.csv')

#Test #4: View Station Properties for station uid=4211
station = wxStations[4211]
print station.name
print station.latitude
print station.longitude
print station.sids
print station.stateCode
print station.elev
print station.uid
print station

#Test #5: Acccess/View UnitCode Query Parameter
print wxStations.queryParameters['unitCode']

#Test #6: Print first five station IDs
print wxStations.stationIDs[0:5]

#Test #7: MABI AvgT - Iterate through list of stations having avg temperature at MABI
wxStations = sf.findStation(unitCode = 'MABI', parameter = 'avgt')
for station in wxStations:
    print station


#******************************************************************************

# DATA REQUESTER

#Case #1: Get daily data for two station IDs (from list) and two parameters
# and automatically save locally
stationIDs = [66176, 31746]
parameters = 'mint, maxt'
startDate = '2012-01-01'
endDate = '2012-02-01'
dr = DataRequestor()
wxData = dr.getDailyWxObservations(stationIDs, parameters
                            ,startDate= startDate, endDate = endDate
                            ,filePathAndName = localFolder + 'DR01.csv')


#Case #2: Get daily data using wxStations object and one parameter
parameters = 'avgt'
wxData = dr.getDailyWxObservations(wxStations, parameters
                            ,startDate= startDate, endDate = endDate)
wxData.export(filePathAndName = localFolder + 'DR02.csv')