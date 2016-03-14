from IM_Climate.StationFinder import StationFinder
from IM_Climate.DataRequestor import DataRequestor

#Find Stations meeting specified criteria
sf = StationFinder()

#The find method returns a stationInfo dictionary object with extended methods
stations = sf.find(state = 'CO', wxElement = 'gdd', countyCode = '08117')
print stations.stationIDs
print stations.stationNames

#Request data for the respective stations
dr = DataRequestor()
#All methods of DataRequestor return a WxData dictionary object
data = dr.getMonthySummary(stations = stations, wxElement = 'avgt', reduceCode = 'mean', startYear = '1980', endYear = '1981')
print data['meta']
print data['data']
print data.toJSON()