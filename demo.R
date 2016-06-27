library(IMClimateR)

# ACIS Data Service Docs: http://www.rcc-acis.org/docs_webservices.html

findStation(parkCodes = "MABI", climateParams=list('pcpn'))
findStation(parkCodes = "MABI", distance=10, climateParams=list('pcpn'))
findStation(parkCodes = "MABI", distance=10, climateParams=list('pcpn'), filePathAndName = "mabi.csv")
getDailyWxObservations(list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), 25056, "20150801", "20150831")
getDailyWxObservations(list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), 17611, "20150801", "20150831")
getDailyWxObservations(list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), 25056, "20150801", "20150810", filePathAndName = "dailyWx.csv")
getDailyWxObservations(list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), 60903)