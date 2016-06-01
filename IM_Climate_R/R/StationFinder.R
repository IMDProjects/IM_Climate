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
  # URLs and request parameters
  
  # NPS Park bounding boxes
  bboxURLBase <- "http://irmaservices.nps.gov/v2/rest/unit/CODE/geography?detail=envelope&dataformat=wkt&format=json"
  bboxExpand  <- 0.33
  
  # ACIS data services
  baseURL <- "http://data.rcc-acis.org/"
  webServiceStation <- "StnMeta"
  
  #stationMetadata <-c('uid', 'name', 'state', 'll', 'elev', 'valid_daterange', 'sids')
  parameters <- c('pcpn', 'snwd', 'avgt', 'obst', 'mint', 'snow', 'maxt')
  encode <- c("json")
  config <- add_headers(Accept = "'Accept':'application/json'")
  
  stationURL <- gsub(" ","",paste(baseURL,webServiceStation))
  
  #Example URLS
  # http://data.rcc-acis.org/StnMeta?bbox=-104.895308730118,%2041.8657116369158,%20-104.197521654032,%2042.5410939149279&meta=uid,%20name,%20state,%20ll,%20elev,%20valid_daterange,sids
  # http://data.rcc-acis.org/StnMeta?bbox=-104.895308730118,%2041.8657116369158,%20-104.197521654032,%2042.5410939149279
  
  # Get bounding box for park(s)
  bboxURL <- gsub("CODE", parkCodes, bboxURLBase)
  # Counter-clockwise vertices (as WKT): LL, LR, UR, UL
  bboxWKT <- strsplit(content(GET(bboxURL, config))[[1]]$Geography, ",")
  # Extract vertices and 'buffer' by 0.3 degrees (~33 km)
  # TODO: add Eastern Hemisphere detection
  LL <- strsplit(substring(bboxWKT[[1]][1], 11), " ")
  LR <- strsplit(substring(bboxWKT[[1]][2], 2), " ")
  UR  <- strsplit(substring(bboxWKT[[1]][3], 2), " ")
  UL  <- strsplit(gsub("))","",substring(bboxWKT[[1]][4], 2)), " ")
  
  LLX  <- as.numeric(LL[[1]][1]) - bboxExpand
  LLY  <- as.numeric(LL[[1]][2]) - bboxExpand
  LRX  <- as.numeric(LR[[1]][1]) + bboxExpand
  LRY  <- as.numeric(LR[[1]][2]) - bboxExpand
  URX  <- as.numeric(UR[[1]][1]) + bboxExpand
  URY  <- as.numeric(UR[[1]][2]) + bboxExpand
  ULX  <-  as.numeric(UL[[1]][1]) - bboxExpand
  ULY  <- as.numeric(UL[[1]][2]) + bboxExpand
  
  bbox  <- paste(c(LLX, LLY, URX, URY), collapse=", ")
  
  body  <- list(bbox = bbox)
  #body  <- list(bbox = bbox, meta = stationMetadata)
  #body  <- list(elems = parameters, bbox = bbox, meta = stationMetadata)
  
  # Format GET URL for use in jsonlite request
  stationRequest <- gsub(" ", "%20", paste(stationURL, body, sep="?bbox="))
  
  # Use bounding box to request station list (jsonlite)
  stationList <- fromJSON(stationRequest) 
  # Use bounding box to request station list (httr GET)
  #stationList  <- content(GET(stationURL, query = body, config = config))
  
  return (stationList$meta)
}