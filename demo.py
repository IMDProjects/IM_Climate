from IM_Climate.StationFinder import StationFinder
from IM_Climate.DataRequestor import DataRequestor


sf = StationFinder()
#list county codes to aid in searching
print(sf.countyCodes(state = 'CO'))
#list valid weather elements to search by
print(sf.parameters)

#Find Stations meeting specified criteria
#Find all stations in Summit County, CO with average temperature
stationInfo = sf.find(wxElement = 'avgt', countyCode = '08117')

#The find method returns a stationInfo dictionary object with extended methods
# and properties
print(stationInfo.stationIDs)
print(stationInfo.stationNames)
print(stationInfo.metadata)
print(stationInfo.toJSON())


#Request data for the respective stations
dr = DataRequestor()

#Get mean monthly values of average temperature from 1970-1975. The stationIfno
#object can be used as the argument for the stations
wxdata = dr.monthySummaryByYear(stationIDs = stationInfo, parameter = 'avgt',
    reduceCode = 'mean', startDate = '1970-01', endDate = '1995-12')

#Get yearly summary
wxdata_yearly = dr.yearlySummary(stationIDs = stationInfo, parameter = 'avgt',
    reduceCode = 'mean', startYear = '1970', endYear = '2005')

#Get the daily average temperatures observations, inlcuding flags, for set of stations.
wxdataData_daily = dr.dailyWxObservations(stationIDs = stationInfo,
    parameter = 'avgt', startDate = '1990-01-01', endDate = '1990-02-05')


#All methods of DataRequestor return a WxData dictionary object with extended
# methods and preoperties
print(wxdata.metadata)  #All metadata
print(wxdata.getStationData(wxdata.stationIDs[0], parameter = 'avgt')) #Get data for first station
print(wxdata.toJSON()) #Export object back to JSON


