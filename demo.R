library(IMClimateR)

# ACIS Data Service Docs: http://www.rcc-acis.org/docs_webservices.html

findStation(unitCode = "MABI", climateParameters=list('pcpn'), distance = 5)
# FWS OrgCOde - Alamosa NWR
findStation(unitCode = "FF06RALM00", climateParameters=list('pcpn'), distance = 50)
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
t <- getDailyGrids(unitCode = list("GRSM"), sdate = "20160615", edate = "20160616", climateParameters = list("mint", "maxt"))
getDailyGrids(unitCode = list("FF06RALM00"), distance=30, sdate = "20150801", edate = "20150803", climateParameters = list("mint", "maxt"))
getMonthlyWxObservations(climateStations = list(61193, 26215), sdate="201401", edate = "201501", maxMissing = NULL, filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationDataRequestor\\getMonthlyWxSummaryByYear\\Test01_R.csv")
getMonthlyWxObservations(climateStations = list(26215), climateParameters = list('pcpn'), reduceCodes = list('min'), edate= "2016-09", maxMissing = 2, filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationDataRequestor\\getMonthlyWxSummaryByYear\\Test02_R.csv")
getMonthlyWxObservations(climateStations = list(61193, 26215), sdate="201401", edate = "201501", maxMissing = NULL, filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationDataRequestor\\getMonthlyWxSummaryByYear\\Test01_R.csv")
getMonthlyWxObservations(climateStations = list(26215), climateParameters = list('pcpn'), reduceCodes = list('min'), edate= "2016-09", maxMissing = 2, filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationDataRequestor\\getMonthlyWxSummaryByYear\\Test02_R.csv")
getMonthlyGrids(unitCode = list("PRWI"), sdate = "201606", edate = "201607", climateParameters = list("mint", "maxt"), filePath="d:\\temp\\trash")
getMonthlyGrids(unitCode = list("GRSM"), sdate = "201606", edate = "201607", climateParameters = list("mint", "maxt"))
getMonthlyGrids(unitCode = list("GRKO"), sdate = "190001", edate = "190012", climateParameters = list("mly_mint"))
t <- getMonthlyGrids(unitCode = list("GRSM"), sdate = "201606", edate = "201607", climateParameters = list("mint", "maxt"))
getMonthlyGrids(unitCode = list("FF06RALM00"), distance=30, sdate = "197001", edate = "197012", climateParameters = list("mly_pcpn"))
ll <- getMonthlyGrids(unitCode = list("FF06RALM00"), distance=30, sdate = "197001", edate = "197012", climateParameters = list("mly_pcpn"))

########### Test case examples #########################
# findStation() 
# Test 1
findStation(unitCode = "ROMO", distance=30, climateParameters=list('maxt','mint'), filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationFinder\\Test01_R.csv")

# Test 2

findStation(unitCode = "AGFO", distance=10, filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationFinder\\Test02_R.csv")

# getDailyWxObservations
# Test 1

getDailyWxObservations(list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), 25056, "20150801", "20150804", filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationDataRequestor\\Test01_R.csv")

# Test 2

getDailyWxObservations(list('pcpn'), 30433, "20150801", "20150804")

# Test 3

ff <- findStation(unitCode = "AGFO", climateParameters = list('pcpn'), distance=10)
getDailyWxObservations(list('pcpn'), ff, "20150801", "20150804", filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationDataRequestor\\Test03_R.csv")

# Test 4

ff <- findStation(unitCode = "ACAD", distance=20)
getDailyWxObservations(climateParameters = NULL, climateStations = ff, sdate = "2015-08-01", edate = "20150804", filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationDataRequestor\\Test04_R.csv")

# getMonthlyWxObservations
# Test 1

getMonthlyWxObservations(climateStations = list(61193, 26215), sdate="201401", edate = "201501", maxMissing = NULL, filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationDataRequestor\\getMonthlyWxSummaryByYear\\Test01_R.csv")

# Test 2

getMonthlyWxObservations(climateStations = list(26215), climateParameters = list('pcpn'), reduceCodes = list('min'), edate= "2016-09", maxMissing = 2, filePathAndName = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\StationDataRequestor\\getMonthlyWxSummaryByYear\\Test02_R.csv")

# getDailyGrids
# Test 1
getDailyGrids(unitCode = list("APPA"), distance = 0, sdate = "2015-01-01", edate = "2015-01-01", climateParameters = list("mint"), filePath="D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\GridRequestor\\Test01")

# Test 2  getMonthlyGrids

getMonthlyGrids(unitCode = list("GRKO"), sdate = "1900-01", edate = "1900-01", climateParameters = list("mly_mint"), filePath = "D:\\Project_Workspace\\DataMart\\Climate\\IM_Climate_GitHub\\TestExamples\\GridRequestor\\Test02")

