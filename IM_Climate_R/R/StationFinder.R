#' Find stations near a park
#' 
#' Takes one park code and one or more climate parameters, determines the stations near the specified park using a bounding box from the IRMA Unit Service (\url{http://irmaservices.nps.gov/v2/rest/unit/CODE/geography?detail=envelope&dataformat=wkt&format=json}). 
#' If distance parameter is specified, bounding box will be buffered by that distance. If no distance is provided, park bounding box is used. 
#' Station location must intersect park bounding box (unbuffered or buffered).
#' Returns station information as a data frame with the following items: name, longitude, latitude, station IDs (sids), state code, elevation (feet), and unique station ID
# @param sourceURL sourceURL for ACIS data services
#' @param parkCodes One NPS park code as a string
#' @param distance (optional) Distance (in kilometers) to buffer park bounding box.
#' @param climateParams A list of one or more climate parameters (e.g. pcpn, mint, maxt, avgt, obst, snow, snwd, cdd, hdd, gdd).  See Table 3 on ACIS Web Services page: http://www.rcc-acis.org/docs_webservices.html
#' @param filePathAndName (optional) File path and name including extension for output CSV file
#' @return A data frame containing station information for stations near the specified park
#' @examples 
#' Find stations collecting average temperature within 10km of Marsh-Billings:
#' 
#' findStation(parkCodes = "MABI", distance=10, climateParams=list('avgt'))
#' 
#' Find stations collecting precipitation or average temperature within 10km of Agate Fossil Beds and save to a CSV file
#' 
#' findStation(parkCodes = "AGFO", distance=10, climateParams=list('pcpn'), filePathAndName = "agfo_stations.csv")
#' @export 
#' 

# TODO: iterate parkCodes list; add either/or capability for park code/bbox

findStation <- function (parkCodes, distance=NULL, climateParams, filePathAndName=NULL) {
  # URLs and request parameters
  
  # NPS Park bounding boxes
  bboxURLBase <- "http://irmaservices.nps.gov/v2/rest/unit/CODE/geography?detail=envelope&dataformat=wkt&format=json"
  if (is.null(distance)) {
    bboxExpand  = 0.0
  }
  else {
    bboxExpand = distance*0.011
  }
  
  # ACIS data services
  baseURL <- "http://data.rcc-acis.org/"
  webServiceSource <- "StnMeta"
  
  #stationMetadata <-c('uid', 'name', 'state', 'll', 'elev', 'valid_daterange', 'sids')
  parameters <- c('pcpn', 'snwd', 'avgt', 'obst', 'mint', 'snow', 'maxt')
  encode <- c("json")
  config <- add_headers(Accept = "'Accept':'application/json'")
  
  stationURL <- gsub(" ","",paste(baseURL,webServiceSource))
  
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

  # Format GET URL for use in jsonlite request
  stationRequest <- gsub(" ", "%20", paste(paste(stationURL, paste(climateParams, collapse = ","), sep="?elems="), body, sep="&bbox="))
  
  # Use bounding box to request station list (jsonlite)
  stationListInit <- fromJSON(stationRequest) 
  # Use bounding box to request station list (httr GET)
  if (length(stationListInit$meta) > 0) {
    longitude <- setNames(as.data.frame(as.numeric(as.matrix(lapply(stationListInit$meta[,2], function(x) unlist(as.numeric(x[1])))))),"longitude")
    latitude <- setNames(as.data.frame(as.numeric(as.matrix(lapply(stationListInit$meta[,2], function(x) unlist(as.numeric(x[2])))))),"latitude")
    sid1 <- setNames(as.data.frame(as.character(as.vector(as.matrix(lapply(stationListInit$meta[,3], function(x) unlist(x[1])))))),"sid1")
    sid2 <- setNames(as.data.frame(as.character(as.vector(as.matrix(lapply(stationListInit$meta[,3], function(x) unlist(x[1])))))),"sid2")
    #stationListTemp <- as.data.frame(lapply(unlist(stationListInit$meta[,2][1],function(x) as.numeric(as.character(x)))))
    #stationList <- as.data.frame(stationListInit$meta)
    stationList <- cbind(name=stationListInit$meta[,1], longitude, latitude, sid1, sid2, state=stationListInit$meta[,4], elev=stationListInit$meta[,5], uid=stationListInit$meta[,6])
    stationList$unit_code <- parkCodes[1]
  }
  else {
    stationList <- cat("No stations for ", parkCodes, "using distance ", distance) 
  }
  # Output file
  if (!is.null(filePathAndName)) {
    write.table(stationList, file=filePathAndName, sep=",", row.names=FALSE, qmethod="double")
  }
  else {
    return (stationList)
  }
  return (stationList)
}