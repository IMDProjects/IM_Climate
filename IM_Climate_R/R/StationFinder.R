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
  # TODO: add expand parameter (buffer distance)
  # URLs and request parameters
  # NPS Park bounding boxes
  bboxURLBase <- "http://irmaservices.nps.gov/v2/rest/unit/CODE/geography?detail=envelope&dataformat=wkt&format=json"
  # ACIS data services
  baseURL <- "http://data.rcc-acis.org/"
  webServiceSource <- "StnMeta"
  
  stationMetadata <-c('uid', 'name', 'state', 'll', 'elev', 'valid_daterange', 'sids')
  parameters <- c('pcpn', 'snwd', 'avgt', 'obst', 'mint', 'snow', 'maxt')
  encode <- c("json")
  confg <- add_headers(Accept = "'Accept':'application/json'")
  
  stationURL <- paste(baseURL,webServiceSource)
  
  # Get bounding box for park(s)
  bboxURL <- gsub("CODE", parkCodes, bboxURLBase)
  # Counter-clockwise vertices (as WKT): LL, LR, UR, UL
  bboxWKT <- content(GET(bboxURL, confg))
  #bboxWKT <- strsplit((content(GET(bboxURL, confg))),".")
  # Extract vertices and 'buffer' by 0.3 degrees (~33 km)
  #LL <- bboxWKT
  #RL <- bboxWKT
  
  return (bboxWKT)
  
  # Use bounding box to request station list
  
  
  #return ("stationList")
}