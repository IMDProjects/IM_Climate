from IM_Climate.StationFinder import StationFinder
from IM_Climate.DataRequestor import DataRequestor
from IM_Climate.NPS_Plotter import NPS_Plotter

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
data = dr.getMonthySummary(stations = stations, wxElement = 'avgt', reduceCode = 'mean', startYear = '1980', endYear = '1985')

#The data object has two components, metadata and data
print data.metadata  #All metadata
print data.dateList  #The dateList
print data.getStationData(data.stationIDList[0]) #Get data for first station

#One extended method is the JSON export
print data.toJSON()


cg = NPS_Plotter(xAxis = range(1,len(data.dateList)+1)
                 ,yData = map(float, data.getStationData(data.stationIDList[0]))
                 ,Title = 'Mean Monthly Average Temperature (F)'
                 ,xLabel = 'Year-Month'
                 ,yLabel = 'Temperature (F)')
