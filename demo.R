library(IMClimateR)

# ACIS Data Service Docs: http://www.rcc-acis.org/docs_webservices.html

findStation(unitCode = "MABI", climateParameters=list('pcpn'), distance = 5)
# FWS OrgCOde - Alamosa NWR
findStation(unitCode = "FF06RALM00", climateParameters=list('pcpn'), distance = 50)
findStation(unitCode = "MABI", distance=10, climateParameters=list('pcpn'), filePathAndName = "mabi.csv")
getWxObservations(climateParameters = list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), climateStations = 25056, sdate = "20150801", edate = "20150831", duration = "dly")
getWxObservations(climateParameters = list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), climateStations = 17611, sdate = "20150801", edate = "20150831")
getWxObservations(climateParameters = list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), climateStations= 25056, sdate = "20150801", edate = "20150810", filePathAndName = "dailyWx.csv")
getWxObservations(climateParameters = list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), climateStations = 60903)
stations <- findStation(unitCode = "AGFO", distance=10)
getWxObservations(climateParameters=list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), climateStations=stations, sdate="20150801", edate="20150803")
getGrids(unitCode = list("AGFO"), distance=10, sdate = "20150801", edate = "20150803", climateParameters = list("mint", "maxt"))
getGrids(unitCode = list("AGFO"), distance=10, sdate = "20150801", edate = "20150803", climateParameters = list("mint", "maxt"), filePath = "D:\\temp\\trash")
getGrids(unitCode = list("APPA"), sdate = "20150101", edate = "20150101", climateParameters = list("mint"), distance = 0, filePath="D:\\temp\\trash")
t <- getGrids(unitCode = list("GRSM"), sdate = "20160615", edate = "20160616", climateParameters = list("mint", "maxt"))
getGrids(unitCode = list("FF06RALM00"), distance=30, sdate = "20150801", edate = "20150803", climateParameters = list("mint", "maxt"))
getWxObservations(climateStations = list(61193, 26215), sdate="201401", edate = "201501", duration = "mly", maxMissing = NULL)
getWxObservations(climateStations = list(26215), climateParameters = list('pcpn'), reduceCodes = list('min'), duration = "mly", edate= "2016-09", maxMissing = 2, filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationDataRequestor\\getMonthlyWxSummaryByYear\\Test02_R.csv")
getWxObservations(climateStations = list(61193, 26215), sdate="201401", edate = "201501", duration = "mly", maxMissing = NULL, filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationDataRequestor\\getMonthlyWxSummaryByYear\\Test01_R.csv")
getWxObservations(climateStations = list(26215), climateParameters = list('pcpn'), reduceCodes = list('min'), edate= "2016-09", duration = "mly", maxMissing = 2, filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationDataRequestor\\getMonthlyWxSummaryByYear\\Test02_R.csv")
getGrids(unitCode = list("PRWI"), sdate = "201606", edate = "201607", climateParameters = list("mly_mint", "mly_maxt"), duration = "mly", filePath="d:\\temp\\trash")
getGrids(unitCode = list("GRSM"), sdate = "201606", edate = "201607", climateParameters = list("mly_mint", "mly_maxt"), duration = "mly")
getGrids(unitCode = list("GRKO"), sdate = "190001", edate = "190012", climateParameters = list("mly_mint"), duration = "mly")
t <- getGrids(unitCode = list("GRSM"), sdate = "201606", edate = "201607", climateParameters = list("mly_mint", "mly_maxt"), duration = "mly")
tYearly <- getGrids(unitCode = list("GRSM"), sdate = "2010", edate = "2016", climateParameters = list("yly_mint", "yly_maxt"), duration = "yly")
getGrids(unitCode = list("FF06RALM00"), distance=30, sdate = "197001", edate = "197012", climateParameters = list("mly_pcpn"), duration = "mly")
ll <- getGrids(unitCode = list("FF06RALM00"), distance=30, sdate = "197001", edate = "197012", climateParameters = list("mly_pcpn"), duration = "mly")

########### Test case examples #########################
# findStation() 
# Test 1
findStation(unitCode = "ROMO", distance=30, climateParameters=list('maxt','mint'), filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationFinder\\Test01_R.csv")

# Test 2

findStation(unitCode = "AGFO", distance=10, filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationFinder\\Test02_R.csv")

# getWxObservations - Daily
# Test 1

getWxObservations(climateParameters = list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), climateStations = 25056, sdate =  "20150801", edate = "20150804", filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationDataRequestor\\getDailyWxObservations\\Test01_R.csv")

# Test 2

getWxObservations(climateParameters = list('pcpn'), climateStations = 30433, sdate = "20150801", edate = "20150804", filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationDataRequestor\\getDailyWxObservations\\Test02_R.csv")

# Test 3

ff <- findStation(unitCode = "AGFO", climateParameters = list('pcpn'), distance=10)
getWxObservations(climateParameters = list('pcpn'), climateStations = ff, sdate = "20150801", edate = "20150804", filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationDataRequestor\\getDailyWxObservations\\Test03_R.csv")

# Test 4

ff <- findStation(unitCode = "ACAD", distance=20)
getWxObservations(climateParameters = NULL, climateStations = ff, sdate = "2015-08-01", edate = "20150804", filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationDataRequestor\\getDailyWxObservations\\Test04_R.csv")

# Test 5
cahaStations  <- findStation(unitCode = "CAHA", distance = 10, climateParameters = list("pcpn", "mint", "maxt"))
getWxObservations(climateParameters = list("pcpn", "mint", "maxt"), climateStations = cahaStations, filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationDataRequestor\\getDailyWxObservations\\Test05_R.csv")

# getMonthlyWxObservations
# Test 1

getWxObservations(climateStations = list(61193, 26215), sdate="201401", edate = "201501", duration = "mly", maxMissing = NULL, filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationDataRequestor\\getMonthlyWxSummaryByYear\\Test01_R.csv")

# Test 2

getWxObservations(climateStations = list(26215), climateParameters = list('pcpn'), reduceCodes = list('min'), edate= "2016-09", duration = "mly", maxMissing = 2, filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationDataRequestor\\getMonthlyWxSummaryByYear\\Test02_R.csv")

# getDailyGrids
# Test 1
getGrids(unitCode = list("APPA"), distance = 0, sdate = "2015-01-01", edate = "2015-01-01", climateParameters = list("mint"), filePath="D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\GridRequestor\\getDailyGrids\\Test01")

# Test 2  getMonthlyGrids

getGrids(unitCode = list("GRKO"), sdate = "1900-01", edate = "1900-01", climateParameters = list("mly_mint"), duration = "mly", filePath = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\GridRequestor\\getMonthlyGrids\\Test01")

# Test 3 getYearlyGrids

getGrids(unitCode = list("ARPO"), sdate = "1900-01", edate = "1900-01", climateParameters = list("yly_pcpn"), duration = "yly", filePath = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\GridRequestor\\getYearlyGrids\\Test01")
