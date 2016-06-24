#' Get station data for specified parameter(s) and station(s)
#' 
#' Takes a list of one or more parameters and one or more unique station IDs, requests station data, and returns it as a data frame
# @param dataURL URL for ACIS data service vending station data
#' @param climateParams A list of one or more climate parameters (e.g. pcpn, mint, maxt, avgt, obst, snow, snwd, cdd, hdd, gdd).  See Table 3 on ACIS Web Services page: http://www.rcc-acis.org/docs_webservices.html
#' @param climateStations A list of one or more unique identifiers for climate stations
#' @param sdate (optional) Default is period of record ("por"). If specific start date is desired, format as a string (yyyy-mm-dd or yyyymmdd). The beginning of the desired date range.   
#' @param edate (optioanl) Default is period of record ("por"). IF specific end date is desired, format as a string (yyyy-mm-dd or yyyymmdd). The end of the desired date range. 
#' @param filePathAndName (optional) File path and name including extension for output CSV file
#' @return A data frame containing the requested data
#' @export
#' 
# TODO: iterate climateStation list

getDailyWxObservations <- function(climateParams, climateStations, sdate="por", edate="por", filePathAndName=NULL) {
  # URLs and request parameters
  
  # ACIS data services
  baseURL <- "http://data.rcc-acis.org/"
  webServiceSource <- "StnData"
  
  # Request parameters
  parameters <- c('pcpn', 'avgt', 'obst', 'mint', 'maxt')
  
  dataURL <-  gsub(" ","", paste(baseURL,webServiceSource))
  climateElems <- paste(climateParams, collapse = ",")
  paramCount <- length(climateParams)
  dateRange <- paste(paste("&sdate=", sdate, sep=""), edate, sep="&edate=")
  
  # Format GET URL for use in jsonlite request
  stationRequest <- gsub(" ", "%20", (paste(paste(paste(dataURL, paste(climateParams, collapse = ","), sep="?elems="), climateStations, sep="&uid="), dateRange, sep = "")))
  
  # Format climate data object
  dataResponseInit <- fromJSON(stationRequest)
  #dataResponseMeta <- as.data.frame(dataResponseInit$meta)
  dataResponse <- as.data.frame(dataResponseInit$data)
  colnames(dataResponse)[1] <- c("date")
  colnames(dataResponse)[2:(paramCount+1)]  <- climateParams
  
  date<-as.Date(dataResponse$date, "%Y-%m-%d")# convert date to vector of date-time class
  
  # convert climate date to numeric and make data.frame
  temp<-as.data.frame(lapply(dataResponse[,2:ncol(dataResponse)], function(x) as.numeric(as.character(x))))
  
  ## bind date and data vectors
  temp1<-cbind(date,temp)
  
  # format station metadata object
  dataResponseMeta <- dataResponseInit$meta
  
  ## unlist, transpose metadata, and create into df
  metadf<-t(as.data.frame(unlist(dataResponseMeta)))
  row.names(metadf)<-NULL# remove rownames
  
  dataResponse<-cbind(metadf,temp1)
  head(dataResponse)
  #rename some columns
  colnames(dataResponse)[2]<-"longitude"
  colnames(dataResponse)[3]<-"latitude"
  
  # Output file
  if (!is.null(filePathAndName)) {
    write.table(dataResponse, file=filePathAndName, sep=",", row.names=FALSE, qmethod="double")
  }
  else {
    return (dataResponse)
  }
  return (dataResponse)
}