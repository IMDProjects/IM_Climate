#' Get station data for specified parameter(s) and station(s)
#' 
#' Takes a list of one or more parameters and one or more stations, requests station data, and returns it as a data frame
# @param dataURL URL for ACIS data service vending station data
#' @param climateParams A list of one or more climate parameters (e.g. pcpn, mint, maxt, avgt, obst, snow, snwd, cdd, hdd, gdd).  See Table 3 on ACIS Web Services page: http://www.rcc-acis.org/docs_webservices.html
#' @param climateStations A list of one or more unique identifiers for climate stations
#' @param sdate Start date as a string (yyyy-mm-dd or yyyymmdd). The beginning of the desired date range. If period of record is desired, use "por".  
#' @param edate End date as a string (yyyy-mm-dd or yyyymmdd). The end of the desired date range. If period of record is desired, use "por".
#' @return A data frame containing the requested data
#' @export
#' 
# TODO: iterate climateStation list

dataRequest <- function(climateParams, climateStations, sdate, edate) {
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
  
  #body  <- list(elems = climateParams, uid = climateStations)
  
  # Format GET URL for use in jsonlite request
  stationRequest <- gsub(" ", "%20", (paste(paste(paste(dataURL, paste(climateParams, collapse = ","), sep="?elems="), climateStations, sep="&uid="), dateRange, sep = "")))
  
  dataResponseInit <- fromJSON(stationRequest)
  #dataResponseMeta <- as.data.frame(dataResponseInit$meta)
  dataResponse <- as.data.frame(dataResponseInit$data)
  colnames(dataResponse)[1] <- c("date")
  colnames(dataResponse)[2:(paramCount+1)]  <- climateParams
  
  return (dataResponse)
}