from IM_Climate.StationFinder import StationFinder
from IM_Climate.DataRequestor import DataRequestor


#Find Stations meeting specified criteria
sf = StationFinder()

#The find method returns a stationInfo dictionary object with extended methods
stations = sf.find(state = 'CO', wxElement = 'avgt', countyCode = '08117')
print stations.stationIDs
print stations.stationNames
print stations.toJSON()

#Request data for the respective stations
dr = DataRequestor()
#All methods of DataRequestor return a WxData dictionary object with extended methods
data = dr.getMonthySummary(stations = stations, wxElement = 'avgt', reduceCode = 'mean', startYear = '1970', endYear = '1975')

#The data object has two components, metadata and data
print data.metadata  #All metadata
print data.dateList  #The dateList
print data.getStationData(data.stationIDList[0]) #Get data for first station

#One extended method is the JSON export
print data.toJSON()


