from IM_Climate_py.StationFinder import StationFinder
from IM_Climate_py.DataRequestor import DataRequestor

'''
This demo script showcases the utility of the IM_Climate.py package
'''
#specify local folder where demo files will be saved
localFolder = 'c:\\temp\\'

#***************
# STATION FINDER - Module to find/locate stations
sf = StationFinder()

#Example #1: All stations around NOCA within a 30km buffer. Save returned results
    #locally as SF01.csv MABI
wxStations = sf.findStation(unitCode = 'MABI', distance = 30, sDate = '1940-01-01', eDate = '1940-01-01')
wxStations.export(localFolder + 'SF01.csv')

#Example #2: All stations around ACAD recording minimum temperature; distance = 10km; save search results as file
wxStations = sf.findStation(unitCode = 'ACAD', distance = 10, climateParameters = 'mint')
wxStations.export(localFolder + 'SF02.csv')

#Example 3: All stations around ROMO recording maximum OR minimum temperature; distance = 40km
        #with option to save file
wxStations = sf.findStation(unitCode = 'ROMO', distance = 40, climateParameters = 'maxt, mint'
        ,filePathAndName = localFolder + 'SF03.csv')

#Example #4: View Station Properties for station uid=4211
station = wxStations[4211]
print station.name
print station.latitude
print station.longitude
print station.sids
print station.state
print station.elev
print station.uid
print station

#Example #5: Acccess/View Query Parameters
print wxStations.queryParameters

#Example #6: Print first five station IDs
print wxStations.stationIDs[0:5]

#Example #7: MABI AvgT -  MABI + 10km
wxStations = sf.findStation(unitCode = 'MABI', distance = 10, climateParameters = 'avgt')
wxStations.export(localFolder + 'SF07.csv') #save to file

#Example #8: #Iterate through list of stations and print to screen
for station in wxStations:
    print(station)

#Example #9:  #print all stations to screen
print (wxStations)

#******************************************************************************
#*****************************************************************************
# DATA REQUESTER - Module to request daily wx data

#Example #1: Get daily data for two station IDs (from list) and two parameters
# and automatically save locally
climateStations = [66176, 31746]
climateParameters = 'mint, maxt'
startDate = '2012-01-01'
endDate = '2012-02-01'
dr = DataRequestor()
wxData = dr.getDailyWxObservations(climateParameters = climateParameters
                            ,climateStations = climateStations
                            ,startDate= startDate, endDate = endDate
                            ,filePathAndName = localFolder + 'DR01.csv')

#Example #2: Get daily data using wxStations object (from Example #1) for average termperature
parameters = 'avgt'
wxData = dr.getDailyWxObservations(climateStations =  wxStations, climateParameters = climateParameters
                            ,startDate = startDate, endDate = endDate)
wxData.export(filePathAndName = localFolder + 'DR02.csv')


#Example #3: print/access minimum temperature data for station 25047 on 2012-01-01
print wxData[25047].data['mint']['2012-01-01']