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
  
  # This returns the full response - need to use content() and parse
  dataResponseInit <- POST("http://data.rcc-acis.org/StnData", accept_json(), add_headers("Content-Type" = "application/json"), body = body, verbose())
  # content(dataResponseInit) results in a list lacking column names but containing data which needs to be
  # converted to dataFrame with appropriate vectors
  
  # Format climate data object
  rList <- content(dataResponseInit)
  
  # Get the station metadata (list that can be manipulated): lapply(rList[[1]], "[", 1)
  # Get the data readings (by parameter) lapply(rList$data[[1]], "[", 1)
  # or lapply(rList$data, "[", 2) for param 1 (includes flags)
  # Get the data flags (by parameter) lapply(rList$data[[1]], "[", 2)
  # or lapply(rList$data, "[", 3) for param 2 (includes flags)  etc.
  # Get the data source flags (by parameter) lapply(rList$data[[1]], "[", 3)
  
  # Start building the data frame by populating the date vector
  df <- as.data.frame(cbind(unlist(lapply(rList$data, "[", 1)[][])))
  colnames(df) <- c("date")
  df$date <- as.Date(df$date, "%Y-%m-%d")
  
  # Add the paramter vectors - thanks for the matrix suggestion, Tom!!
  for (i in 2:(length(rList$data[[1]]))-1)  { #  == count of parameters
    vName <- paste(climateParameters[i], "value", sep="_")
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
  
  # dataResponse <- as.data.frame(dataResponseInit$data)
  # colnames(dataResponse)[1] <- c("date")
  # colnames(dataResponse)[2:(paramCount+1)]  <- climateParameters
  # 
  # # convert climate date to numeric and make data.frame
  # temp<-as.data.frame(lapply(dataResponse[,2:ncol(dataResponse)], function(x) as.numeric(as.character(x))))
  # 
  # date<-as.Date(dataResponse$date, "%Y-%m-%d")# convert date to vector of date-time class
  # 
  # ## bind date and data vectors
  # temp1<-cbind(date,temp)
  # 
  # # format station metadata object
  # dataResponseMeta <- dataResponseInit$meta
  # 
  # ## unlist, transpose metadata, and create into df
  # metadf<-t(as.data.frame(unlist(dataResponseMeta)))
  # row.names(metadf)<-NULL# remove rownames
  # 
  # dataResponse<-cbind(metadf,temp1)
  # head(dataResponse)
  # #rename some columns
  # colnames(dataResponse)[2]<-"longitude"
  # colnames(dataResponse)[3]<-"latitude"
  # llong <- as.numeric(as.vector(dataResponse$longitude))
  # llat <- as.numeric(as.vector(dataResponse$latitude))
  # 
  # dataResponse <- dataResponse[ , -which(names(dataResponse) %in% c("longitude","latitude"))]
  # dataResponse["longitude"] <- llong
  # dataResponse["latitude"] <- llat
  # dataResponse <- dataResponse[c("uid","longitude","latitude","sids1","sids2","sids3","state","elev","name","date",as.character(climateParameters))]
  # 
  # Output file
  if (!is.null(filePathAndName)) {
    write.table(dataResponse, file=filePathAndName, sep=",", row.names=FALSE, qmethod="double")
  }
  else {
    return (dataResponse)
  }
  return (dataResponse)
}
