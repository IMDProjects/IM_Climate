from IM_Climate.StationFinder import StationFinder
from IM_Climate.DataRequestor import DataRequestor

import datetime

#Get all stations within a HUC
sf = StationFinder()
stationInfo = sf.find(HUC = 14010001)


dr = DataRequestor()
print 'Calculate monthly summaries using MultiStation'
begin =  datetime.datetime.now()
wd = dr.monthySummary(stations = stationInfo,  wxElement = 'avgt', reduceCode = 'mean', startYear = '1960', endYear = '2015')
end =  datetime.datetime.now()
print 'Request time = ' + str((end-begin).seconds) + ' seconds'

print 'Calculate monthly summaries using SingleStation'
begin =  datetime.datetime.now()
wd = dr.monthySummary_SINGLE(stations = stationInfo,  wxElement = 'avgt', reduceCode = 'mean', startYear = '1960', endYear = '2015')
end =  datetime.datetime.now()
print 'Request time = ' + str((end-begin).seconds) + ' seconds'

