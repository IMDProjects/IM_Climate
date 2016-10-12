from IM_Climate_py.StationFinder import StationFinder
from IM_Climate_py.StationDataRequestor import StationDataRequestor
from IM_Climate_py.GridRequestor import GridRequestor

'''
This demo script showcases the utility of the IM_Climate.py package
'''
#specify local folder where demo files will be saved
localFolder = 'c:\\temp\\'

##******************************************************************************
##*****************************************************************************
# STATION FINDER - Module to find/locate stations
# FIND STATION - method to locate stations

sf = StationFinder()
#Locate all stations around MABI within a 30km buffer. Save results as MABI_Stations.csv
wxStations = sf.findStation(unitCode = 'MABI', distance = 30, climateParameters = 'mint, maxt'
    , filePathAndName = localFolder + 'MABI_Stations.csv')

#print all stations to screen
print (wxStations)

#save station list to a comma-delimited text file
wxStations.export(filePathAndName = localFolder + 'MABI_Stations.csv')

#view station IDs from search results
print (wxStations.stationIDs)

#view query parameters
print (wxStations.queryParameters)

#iterate through list of stations
for station in wxStations:
    print(station.name)

#view station properties for station uid=17605
station = wxStations[17605]

#view station name
print (station.name)

#view all station properties
print (station)

##******************************************************************************
##*****************************************************************************
# STATION DATA REQUESTER - Module to request station data

#*GET DAILY WX OBSERVATIONS - Method to request daily wx data

#Example #1: Get daily data for two station IDs (from list) and two parameters
# and automatically save locally
climateStations = [66176, 31746]

dr = StationDataRequestor()
#Get wxData for two stations
wxData = dr.getDailyWxObservations(climateStations = [66176, 31746],
    climateParameters = 'mint, maxt', sdate= '2012-01-01' , edate = '2012-02-01')

#get daily data using wxStations object (from Example #1) for average termperature
wxData = dr.getDailyWxObservations(climateStations =  wxStations, climateParameters = 'mint, maxt'
                            ,sdate = '2012-01-01', edate = '2012-02-01')

#view data
print (wxData)

#export weather data
wxData.export(localFolder + 'DR02.csv')

#view minimum temperature data for station 25047 on 2012-01-01
print (wxData[25047].data['mint']['2012-01-01'])

#*GET MONTHLY WEATHER SUMMARY BY YEAR

#get monthly summary for minimum and maximum temperature for two climate stations
# from January 2012 to most current record. Use default of maximum missing days of 1.
wxData = dr.getMonthlyWxSummaryByYear(climateStations = '66176, 31746',
    climateParameters = 'mint, maxt', reduceCodes = 'min', sdate = '2012-01')

print (wxData)

#******************************************************************************
#*****************************************************************************
# GRID REQUESTER - Module to request gridded data

gr = GridRequestor()

#get daily PRISM grids for GRKO and 10-km buffer for minimum temperature
grids=  gr.getDailyGrids(sdate = '2015-01-01', edate = '2015-01-10', unitCode = 'GRKO'
    ,distance = 10, climateParameters = 'mint')

#view gridded data
print (grids)

#view all parameters
print grids.climateParameters

#view all dates
print (grids.dates)

#print the grid for minimum temperature on 1/3/2015
print grids['mint']['2015-01-03']

#export all grids (file names are automatically created)
grids.export(filePath = localFolder)

#export a single grid - note that filename is required. The prj file is automatically created
grids['mint']['2015-01-01'].export(localFolder + 'GRKO_PRISM_mint_20150101.asc')