#' Find stations near a park
#' 
#' Takes one or more park codes, determines the stations near the specified park, and returns the list of station identifiers
# @param sourceURL sourceURL for ACIS data services
#' @param parkCodes One or more NPS park codes as a List
#' @return A list of station identfiers for stations near the specified parks
#' @export 
#' 

#install.packages("jsonlite")
#library(jsonlite)

findStation <- function (parkCodes) {
  baseURL <- "http://data.rcc-acis.org/"
  webServiceSource <- "StnMeta"
  
  targetURL <- paste(baseURL,webServiceSource)
  
  return ("stationList")
}