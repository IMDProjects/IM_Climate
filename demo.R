library(IMClimateR)

# ACIS Data Service Docs: http://www.rcc-acis.org/docs_webservices.html

findStation(unitCode = "MABI", climateParameters=list('pcpn'), distance = 5)
findStation(unitCode = "MABI", distance=10, climateParameters=list('pcpn'), filePathAndName = "mabi.csv")
getDailyWxObservations(list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), 25056, "20150801", "20150831")
getDailyWxObservations(list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), 17611, "20150801", "20150831")
getDailyWxObservations(list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), 25056, "20150801", "20150810", filePathAndName = "dailyWx.csv")
getDailyWxObservations(list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), 60903)
stations <- findStation(unitCode = "AGFO", distance=10)
getDailyWxObservations(climateParameters=list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), climateStations=stations, sdate="20150801", edate="20150803")
getDailyGrids(unitCode = list("AGFO"), distance=10, sdate = "20150801", edate = "20150803", climateParameters = list("mint", "maxt"))
getDailyGrids(unitCode = list("AGFO"), distance=10, sdate = "20150801", edate = "20150803", climateParameters = list("mint", "maxt"), filePath = "D:\\temp\\trash")
getDailyGrids(unitCode = list("APPA"), sdate = "20150101", edate = "20150101", climateParameters = list("mint"), distance = 0, filePath="D:\\temp\\trash")
getMonthlyWxObservations(climateStations = list(61193, 26215), sdate="201401", edate = "201501", maxMissing = NULL, filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationDataRequestor\\getMonthlyWxSummaryByYear\\Test01_R.csv")
getMonthlyWxObservations(climateStations = list(26215), climateParameters = list('pcpn'), reduceCodes = list('min'), edate= "2016-09", maxMissing = 2, filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationDataRequestor\\getMonthlyWxSummaryByYear\\Test02_R.csv")


