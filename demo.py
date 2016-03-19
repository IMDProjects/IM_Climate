from IM_Climate.StationFinder import StationFinder
from IM_Climate.DataRequestor import DataRequestor


sf = StationFinder()
#list county codes to aid in searching
print(sf.countyCodes(state = 'CO'))

#Find Stations meeting specified criteria
#Find all stations in Summit County, CO with average temperature
#The find method returns a stationInfo dictionary object with extended methods
stationInfo = sf.find(wxElement = 'avgt', countyCode = '08117')
print(stationInfo.stationIDs)
print(stationInfo.stationNames)
print(stationInfo.metadata)
print(stationInfo.toJSON())


#Request data for the respective stations
#All methods of DataRequestor return a WxData dictionary object with extended methods
dr = DataRequestor()
#Get mean monthly values of average temperature from 1970-1975. the stationIfno
#object can be used as the argument for the stations
wxdata = dr.getMonthySummary(stations = stationInfo, wxElement = 'avgt', reduceCode = 'mean', startYear = '1970', endYear = '1975')
#Get the daily average temperatures observations, inlcuding flags, for set of stations.
wxdataData_daily = dr.getDailyWxObservations(stations = stationInfo, wxElement = 'avgt', startDate = '1990-01-01', endDate = '1990-02-05')


#All returned objects (stationInfo and WxData) have metadata
print(wxdata.metadata)  #All metadata
print(wxdata.dateList)  #The dateList
print(wxdata.getStationData(wxdata.stationIDList[0])) #Get data for first station

#One extended method is the JSON export
print(wxdata.toJSON())


