#' Get station data for specified parameter(s) and station(s)
#' 
#' Takes a list of one or more parameters and one or more unique station IDs, requests station data, and returns it as a data frame
# @param dataURL URL for ACIS data service vending station data
#' @param climateParameters A list of one or more climate parameters (e.g. pcpn, mint, maxt, avgt, obst, snow, snwd, cdd, hdd, gdd).  See Table 3 on ACIS Web Services page: http://www.rcc-acis.org/docs_webservices.html
#' @param climateStations A list of one or more unique identifiers for climate stations
#' @param sdate (optional) Default is period of record ("por"). If specific start date is desired, format as a string (yyyy-mm-dd or yyyymmdd). The beginning of the desired date range.   
#' @param edate (optional) Default is period of record ("por"). IF specific end date is desired, format as a string (yyyy-mm-dd or yyyymmdd). The end of the desired date range. 
#' @param filePathAndName (optional) File path and name including extension for output CSV file
#' @return A data frame containing the requested data
#' @examples 
#' Precipitation, temperature weather observations for a station for a specifc date range:
#' 
#' getDailyWxObservations(list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), 25056, "20150801", "20150831")
#' 
#' All weather observations for a station for its period of record
#' 
#' getDailyWxObservations(list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), 60903)
#' @export
#' 
# TODO: extract response metadata and add as output object
# TODO: iterate climateStation list
# TODO: encapsulate in error block
# See https://github.com/hadley/httr/blob/master/vignettes/api-packages.Rmd

getDailyWxObservations <- function(climateParameters, climateStations, sdate="por", edate="por", filePathAndName=NULL) {
  # URLs and request parameters
  
  # ACIS data services
  baseURL <- "http://data.rcc-acis.org/"
  webServiceSource <- "StnData"
  # Parameter flags: f = ACIS flag, s = source flag
  paramFlags <- c("f,s")
  lookups <- fromJSON("ACISLookups.json", flatten = TRUE)
  luElements  <- lookups$element

  dataURL <-  gsub(" ","", paste(baseURL,webServiceSource))
  climateElems <- paste(climateParameters, collapse = ",")
  paramCount <- length(climateParameters)
  
  # Format POST request for use in httr
  
  # Iterate parameter list to create elems element:
  eList <- vector('list', paramCount)
  for (i in 1:paramCount) {
    e <- list(name=unlist(c(climateParameters[i])), add=paramFlags)
    #print(e)
    eList[[i]] <- e
  }
  # Climate parameters as JSON with flags
  elems <- toJSON(eList, auto_unbox = TRUE)
  
  # List for SID, sdate, edate
  # TODO: reformat when allow >1 climate station
  bList <- list(uid = climateStations, sdate = sdate, edate = edate, elems = elems)
  #bList <- list(sid = climateStations, sdate = sdate, edate = edate, elems = elems)
  
  # Format and clean up JSON elements
  # Yes, this is crappy code but it works
  # TODO: Clean this up!!!
  bJSON <- gsub("\\\\","T", toJSON(bList, auto_unbox = TRUE))
  f = gsub("\"\\[","\\[", bJSON)
  g = gsub("\\]\"","\\]", f)
  h = gsub("T","", g)
  i = gsub("\"\"\\{","\\{",h)
  body <- gsub("\\}\"\"","\\}",i)
  
  # Initialize vectors for SID type
  sid1_type = c()
  sid2_type = c()
  sid3_type = c()
  
  # This returns the full response - need to use content() and parse
  # content(dataResponseInit) results in a list lacking column names but containing data which needs to be
  # converted to dataFrame with appropriate vectors
  dataResponseInit <- POST("http://data.rcc-acis.org/StnData", accept_json(), add_headers("Content-Type" = "application/json"), body = body, verbose())
  
  # Format climate data object
  rList <- content(dataResponseInit)
  
  # Get the station metadata (list that can be manipulated): lapply(rList[[1]], "[", 1)
  # Get the data readings (by parameter) lapply(rList$data[[1]], "[", 1)
  # or lapply(rList$data, "[", 2) for param 1 (includes flags)
  # Get the data flags (by parameter) lapply(rList$data[[1]], "[", 2)
  # or lapply(rList$data, "[", 3) for param 2 (includes flags)  etc.
  # Get the data source flags (by parameter) lapply(rList$data[[1]], "[", 3)
  
  # Start building the data frame by populating the date vector
  dfDate <- as.data.frame(cbind(unlist(lapply(rList$data, "[", 1)[][])))
  dfMetaInit <-  t(as.data.frame(rList$meta))
  colnames(dfDate) <- c("date")
  dfDate$date <- as.Date(dfDate$date, "%Y-%m-%d")
  
  # Populate metadata
  dfMeta <- as.data.frame(as.character(as.vector(dfMetaInit[1,])))
  colnames(dfMeta)[1]  <- names(rList$meta)[1]
  dfMeta  <- cbind(dfMeta, as.data.frame(as.numeric(as.vector(dfMetaInit[2,]))))
  colnames(dfMeta)[2]  <- "longitude"
  dfMeta  <- cbind(dfMeta, as.data.frame(as.numeric(as.vector(dfMetaInit[3,]))))
  colnames(dfMeta)[3]  <- "latitude"
  # Assumes sids element contains 3 members (even if 2 are empty)
  dfMeta  <- cbind(dfMeta, as.data.frame(as.character(as.vector(dfMetaInit[4,]))))
  colnames(dfMeta)[4]  <- "sid1"
  dfMeta$sid1  <- as.character(dfMeta$sid1)
  sid1_type <-  getStationSubtype(unlist(strsplit(unlist(dfMeta$sid1), " "))[2], substr(unlist(strsplit(unlist(dfMeta$sid1), " "))[1],1,3))
  dfMeta  <- cbind(dfMeta, as.data.frame(as.character(as.vector(sid1_type))))
  colnames(dfMeta)[5]  <- "sid1_type"
    #getStationSubtype(unlist(strsplit(sid1[i], " "))[2], substr(sid1[i],1,3))
  #sid1_type[i] <-  getStationSubtype(unlist(strsplit(unlist(rList$meta$sids[i]), " "))[2], substr(unlist(strsplit(unlist(rList$meta$sids[i]), " "))[1],1,3))
  #for (i in 1:length(rList$meta$sids)) {
  #  sid1_type[i] <-  getStationSubtype(unlist(strsplit(unlist(rList$meta$sids[i]), " "))[2], substr(unlist(strsplit(unlist(rList$meta$sids[i]), " "))[1],1,3))
  #}
  if (identical(dim(dfMetaInit), as.integer(c(9,1)))) {
    dfMeta  <- cbind(dfMeta, as.data.frame(as.character(as.vector(dfMetaInit[6,]))))
    colnames(dfMeta)[6]  <- "sid2"
    dfMeta$sid2  <- as.character(dfMeta$sid2)
    sid2_type <-  getStationSubtype(unlist(strsplit(unlist(dfMeta$sid2), " "))[2], substr(unlist(strsplit(unlist(dfMeta$sid2), " "))[1],1,3))
    dfMeta  <- cbind(dfMeta, as.data.frame(as.character(as.vector(sid2_type))))
    colnames(dfMeta)[7]  <- "sid2_type"
    dfMeta  <- cbind(dfMeta, as.data.frame(as.character(as.vector(dfMetaInit[8,]))))
    colnames(dfMeta)[8]  <- "sid3"
    dfMeta$sid3  <- as.character(dfMeta$sid3)
    sid3_type <-  getStationSubtype(unlist(strsplit(unlist(dfMeta$sid3), " "))[2], substr(unlist(strsplit(unlist(dfMeta$sid3), " "))[1],1,3))
    dfMeta  <- cbind(dfMeta, as.data.frame(as.character(as.vector(sid3_type))))
    colnames(dfMeta)[9]  <- "sid3_type"
  }
  else { # missing one or more sid elements
    if (identical(dim(dfMetaInit), as.integer(c(8,1)))) {
      dfMeta  <- cbind(dfMeta, as.data.frame(as.character(as.vector(dfMetaInit[6,]))))
      colnames(dfMeta)[6]  <- "sid2"
      dfMeta$sid2  <- as.character(dfMeta$sid2)
      sid2_type <-  getStationSubtype(unlist(strsplit(unlist(dfMeta$sid2), " "))[2], substr(unlist(strsplit(unlist(dfMeta$sid2), " "))[1],1,3))
      dfMeta  <- cbind(dfMeta, as.data.frame(as.character(as.vector(sid2_type))))
      colnames(dfMeta)[7]  <- "sid2_type"
    }
    else { # no sid2 value
      dfMeta  <- cbind(dfMeta, as.data.frame(NA))
      colnames(dfMeta)[6]  <- "sid2"
      #dfMeta$sid2  <- as.character(dfMeta$sid2)
      sid2_type <-  as.data.frame(NA)
      #dfMeta  <- cbind(dfMeta, as.character(sid2_type))
      dfMeta  <- cbind(dfMeta, as.data.frame(as.character(as.vector(sid2_type))))
      colnames(dfMeta)[7]  <- "sid2_type"
    } # no sid3 value
    dfMeta  <- cbind(dfMeta, as.data.frame(NA))
    colnames(dfMeta)[8]  <- "sid3"
    #dfMeta$sid3  <- as.character(dfMeta$sid3)
    sid3_type <-  as.data.frame(NA)
    dfMeta  <- cbind(dfMeta, as.data.frame(as.character(as.vector(sid3_type))))
    colnames(dfMeta)[9]  <- "sid3_type"
  }

  # Use SID vectors to find sid_type  # lapply() might work here
  # for (i in 1:length(dfMeta$sid1)) { 
  #   sid1_type[i] <-  getStationSubtype(unlist(strsplit(unlist(dfMeta$sid1), " "))[2], substr(unlist(strsplit(unlist(dfMeta$sid1), " "))[1],1,3))
  # }
  # for (i in 1:length(dfMeta$sid2)) { 
  #   sid2_type[i] <-  getStationSubtype(unlist(strsplit(unlist(dfMeta$sid2), " "))[2], substr(unlist(strsplit(unlist(dfMeta$sid2), " "))[1],1,3))
  # }
  # for (i in 1:length(dfMeta$sid3)) { 
  #   sid3_type[i] <-  getStationSubtype(unlist(strsplit(unlist(dfMeta$sid3), " "))[2], substr(unlist(strsplit(unlist(dfMeta$sid3), " "))[1],1,3))
  # }
  dfMeta  <- cbind(dfMeta, as.data.frame(as.character(as.vector(strsplit(dfMetaInit[,1], " ")$state))))
  colnames(dfMeta)[10]  <- "state"
  dfMeta  <- cbind(dfMeta, as.data.frame(as.numeric(as.vector(strsplit(dfMetaInit[,1], " ")$elev))))
  colnames(dfMeta)[11]  <- "elev"
  #tempName <- paste(strsplit(dfMetaInit[,1], " ")$name, collapse = " ")
  #dfMeta  <- cbind(dfMeta, as.data.frame(as.character(as.vector(tempName))))
  dfMeta  <- cbind(dfMeta, as.data.frame(as.character(as.vector(paste(strsplit(dfMetaInit[,1], " ")$name, collapse = " ")))))
  colnames(dfMeta)[12]  <- "name"
  
  df <- cbind(dfMeta, dfDate)
  
  # Add the paramter vectors - thanks for the matrix suggestion, Tom!!
  # Get parameter units from lookup file
  for (i in 2:(length(rList$data[[1]]))-1)  { #  == count of parameters
    vUnit <- luElements[which(luElements$code==climateParameters[i]),]$unitabbr
    vName <- paste(climateParameters[i], vUnit, sep="_")
    fName <- paste(climateParameters[i], "acis_flag", sep="_")
    sName <- paste(climateParameters[i], "source_flag", sep="_")
    valueArray <-  matrix(unlist(lapply(rList$data, "[", i+1)), ncol=3, byrow=TRUE)[,1]
    flagArray <-  matrix(unlist(lapply(rList$data, "[", i+1)), ncol=3, byrow=TRUE)[,2]
    sourceFlagArray <-  matrix(unlist(lapply(rList$data, "[", i+1)), ncol=3, byrow=TRUE)[,3]
    df[[vName]] <- as.numeric(valueArray)
    df[[fName]] <- as.character(replace(flagArray, flagArray == " ", NA))
    df[[sName]] <- as.character(replace(sourceFlagArray, sourceFlagArray == " ", NA))
  }
  
  dataResponse <- df
  
  # Output file
  if (!is.null(filePathAndName)) {
    write.table(dataResponse, file=filePathAndName, sep=",", row.names=FALSE, qmethod="double")
  }
  else {
    return (dataResponse)
  }
  return (dataResponse)
}
