from IM_Climate_py.ACIS_StationFinder import ACIS_StationFinder
from IM_Climate_py.ACIS_DataRequestor import ACIS_DataRequestor

'''
This demo script showcases the utility of the IM_Climate.py package
'''
#specify local folder where demo files will be saved
localFolder = 'c:\\temp\\'

#***************
# STATION FINDER
sf = ACIS_StationFinder()

#Test #1: All stations around NOCA within a 30km buffer. Save returned results
    #locally as SF01.csv MABI
wxStations = sf.findStation(unitCode = 'MABI', distance = 30, sDate = '1940-01-01', eDate = '1940-01-01')
wxStations.export(localFolder + 'SF01.csv')

#Test #2: All stations around ACAD recording minimum temperature; distance = 10km
wxStations = sf.findStation(unitCode = 'ACAD', distance = 10, climateParameters = 'mint')
wxStations.export(localFolder + 'SF02.csv')

#Test 3: All stations around ROMO recording maximum OR minimum temperature; distance = 40km
        #with option to save file
wxStations = sf.findStation(unitCode = 'ROMO', distance = 40, climateParameters = 'maxt, mint'
        ,filePathAndName = localFolder + 'SF03.csv')

#Test #4: View Station Properties for station uid=4211
station = wxStations[4211]
print station.name
print station.latitude
print station.longitude
print station.sids
print station.state
print station.elev
print station.uid
print station

#Test #5: Acccess/View UnitCode Query Parameter
print wxStations.queryParameters['unitCode']

#Test #6: Print first five station IDs
print wxStations.stationIDs[0:5]

#Test #7: MABI AvgT -  MABI + 10km
wxStations = sf.findStation(unitCode = 'MABI', distance = 10, climateParameters = 'avgt')
wxStations.export(localFolder + 'SF07.csv') #save to file
for station in wxStations: #Iterate through list of stations and print to screen
    print(station)
print (wxStations)    #print all stations to screen

#******************************************************************************

# DATA REQUESTER

#Case #1: Get daily data for two station IDs (from list) and two parameters
# and automatically save locally
climateStations = [66176, 31746]
climateParameters = 'mint, maxt'
startDate = '2012-01-01'
endDate = '2012-02-01'
dr = ACIS_DataRequestor()
wxData = dr.getDailyWxObservations(climateParameters = climateParameters
                            ,climateStations = climateStations
                            ,startDate= startDate, endDate = endDate
                            ,filePathAndName = localFolder + 'DR01.csv')

#Case #2: Get daily data using wxStations object and one parameter
parameters = 'avgt'
wxData = dr.getDailyWxObservations(climateStations =  wxStations, climateParameters = climateParameters
                            ,startDate = startDate, endDate = endDate)
wxData.export(filePathAndName = localFolder + 'DR02.csv')

