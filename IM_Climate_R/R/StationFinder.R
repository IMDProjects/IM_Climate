#' Find stations near a park or refuge
#' 
#' Takes one park or refuge organizational code and one or more climate parameters, determines the stations near the specified park/refuge using a bounding box from the IRMA Unit Service (\url{http://irmaservices.nps.gov/v2/rest/unit/CODE/geography?detail=envelope&dataformat=wkt&format=json}). 
#' If distance parameter is specified, bounding box will be buffered by that distance. If no distance is provided, park bounding box is used. 
#' Station location must intersect park bounding box (unbuffered or buffered).
#' Returns station information as a data frame with the following items: name, longitude, latitude, station IDs (sids), state code, elevation (feet), and unique station ID
# @param sourceURL sourceURL for ACIS data services
#' @param unitCode One NPS unit code or FWS refuge code as a string
#' @param distance (optional) Distance (in kilometers) to buffer park bounding box
#' @param climateParameters A list of one or more climate parameters (e.g. pcpn, mint, maxt, avgt, obst, snow, snwd). If not specified, defaults to all parameters except degree days. See Table 3 on ACIS Web Services page: \url{http://www.rcc-acis.org/docs_webservices.html}
#' @param filePathAndName (optional) File path and name including extension for output CSV file
#' @return A data frame containing station information for stations near the specified park/refuge. See User Guide for more details:  \url{https://docs.google.com/document/d/1B0rf0VTEXQNWGW9fqg2LRr6cHR20VQhFRy7PU_BfOeA/}
#' @examples \dontrun{
#' Find stations collecting average temperature within 10km of Marsh-Billings NHP:
#' 
#' findStation(unitCode = "MABI", distance=10, climateParameters=list('avgt'))
#' 
#' Find stations collecting all climate parameters except degree days within 15km of Marsh-Billings NHP:
#' 
#' findStation(unitCode = "MABI", distance=10)
#' 
#' Find stations collecting precipitation or average temperature within 10km of Agate Fossil Beds and save to a CSV file:
#' 
#' findStation(unitCode = "AGFO", distance=10, climateParameters=list('pcpn'), filePathAndName = "agfo_stations.csv")
#' 
#' Find stations within 30km of Rocky Mountain NP collecting maxt and mint:
#' 
#' findStation(unitCode = "ROMO", distance=30, climateParameters=list('pcpn'), filePathAndName = "Test01_R.csv")
#' 
#'Find stations within 50km of Alamosa NWR that collect precipitation data 
#'  
#'findStation(unitCode = "FF06RALM00", climateParameters=list('pcpn'), distance = 50)
#' }
#' @export 
#' 

# TODO: iterate unitCode list; add either/or capability for park code/bbox

findStation <- function (unitCode, distance=NULL, climateParameters=NULL, filePathAndName=NULL) {
  # URLs and request parameters
  
  # NPS Park bounding boxes
  if (is.null(distance)) {
    bboxExpand  = 0.0
  }
  else if (distance == 0) {
    bboxExpand = 0.0
  }
  else {
    bboxExpand = distance*0.011  # convert km to decimal degrees
  }
  
  # ACIS data services
  baseURL <- "http://data.rcc-acis.org/"
  webServiceSource <- "StnMeta"
  lookups <- 
    fromJSON(system.file("ACISLookups.json", package = "IMClimateR"), flatten = TRUE) # assumes placement in package inst subfolder
  
  stationMetadata = c('uid', 'name', 'state', 'll', 'elev', 'valid_daterange', 'sids')
  #stationMetadata <-c('uid', 'name', 'state', 'll', 'elev', 'valid_daterange', 'sids')
  # If climateParameters is NULL, default to all parameters except degree days.
  #parameters <- list('pcpn', 'avgt', 'obst', 'mint', 'maxt', 'snwd', 'snow') 
  encode <- c("json")
  config <- add_headers(Accept = "'Accept':'application/json'")
  
  stationURL <- gsub(" ","",paste(baseURL,webServiceSource))
  
  #Example URLS
  # http://data.rcc-acis.org/StnMeta?bbox=-104.895308730118,%2041.8657116369158,%20-104.197521654032,%2042.5410939149279&meta=uid,%20name,%20state,%20ll,%20elev,%20valid_daterange,sids
  # http://data.rcc-acis.org/StnMeta?bbox=-104.895308730118,%2041.8657116369158,%20-104.197521654032,%2042.5410939149279
  
  # Get bounding box for park(s)
  bbox <- getBBox(unitCode, bboxExpand) 
  body  <- list(bbox = bbox)

  # Format GET URL for use in jsonlite request
  if (is.null(climateParameters)) {
    climateParameters0 <- lookups$element$code
    # Remove degree days (v1.5); super cheesy... fix at some point
    climateParameters <- climateParameters0[1:7]
    #climateParameters = parameters
  }
  stationRequest <- gsub(" ", "%20", paste(paste(paste(stationURL, paste(climateParameters, collapse = ","), sep="?elems="), body, sep="&bbox="), paste(stationMetadata, collapse=","), sep="&meta="))
  #stationRequest <- gsub(" ", "%20", paste(paste(stationURL, paste(climateParameters, collapse = ","), sep="?elems="), body, sep="&bbox="))
  #stationRequest <- gsub(" ", "%20", paste(paste(paste(stationURL, paste(climateParameters, collapse = ","), sep="?elems="), body, sep="&bbox=")),paste(stationMetadata, collapse = ","), sep="&meta=")
  
  # Use bounding box to request station list (jsonlite)
  stationListInit <- fromJSON(stationRequest) 
  if (length(stationListInit$meta) > 0) {
    uid <- setNames(as.data.frame(as.numeric(stationListInit$meta$uid)), "uid")
    longitude <- setNames(as.data.frame(as.numeric(as.matrix(lapply(stationListInit$meta$ll, function(x) unlist(as.numeric(x[1])))))),"longitude")
    latitude <- setNames(as.data.frame(as.numeric(as.matrix(lapply(stationListInit$meta$ll, function(x) unlist(as.numeric(x[2])))))),"latitude")
    # Check for presence of all SID values (use max of 3 per record even if station has > 3)
    # Suppress warnings from getStationSubtype(): raised due to conversion necessary because data.frame vector access does not recognize column name
    sid1 = c()
    sid2 = c()
    sid3 = c()
    sid1_type = c(as.character(NA))
    sid2_type = c(as.character(NA))
    sid3_type = c(as.character(NA))
    minDate = c(as.Date(NA))
    maxDate = c(as.Date(NA))
    for (i in 1:length(stationListInit$meta$sids)) {
      if (length(unlist(stationListInit$meta$sids[i])) >= 3) {
        sid1[i] <- as.character(as.vector(lapply(stationListInit$meta$sids[i], function(x) unlist(x[1]))))
        sid1_type[i] <-  suppressWarnings(getStationSubtype(unlist(strsplit(sid1[i], " "))[2], substr(sid1[i],1,3)))
        
        sid2[i] <- as.character(as.vector(lapply(stationListInit$meta$sids[i], function(x) unlist(x[2]))))
        sid2_type[i] <-  suppressWarnings(getStationSubtype(unlist(strsplit(sid2[i], " "))[2], substr(sid2[i],1,3)))
        sid3[i] <- as.character(as.vector(lapply(stationListInit$meta$sids[i], function(x) unlist(x[3]))))
        sid3_type[i] <-  suppressWarnings(getStationSubtype(unlist(strsplit(sid3[i], " "))[2], substr(sid3[i],1,3)))
      }
      else if (identical(length(unlist(stationListInit$meta$sids[i])), as.integer(c(2)))) {
        sid1[i] <- as.character(as.vector(lapply(stationListInit$meta$sids[i], function(x) unlist(x[1]))))
        sid1_type[i] <-  suppressWarnings(getStationSubtype(unlist(strsplit(sid1[i], " "))[2], substr(sid1[i],1,3)))
        sid2[i] <- as.character(as.vector(lapply(stationListInit$meta$sids[i], function(x) unlist(x[2]))))
        sid2_type[i] <-  suppressWarnings(getStationSubtype(unlist(strsplit(sid2[i], " "))[2], substr(sid2[i],1,3)))
        sid3[i] <- as.character(NA)
        sid3_type[i] <-  as.character(NA)
      }
      else {
        sid1[i] <- as.character(as.vector(lapply(stationListInit$meta$sids[i], function(x) unlist(x[1]))))
        sid1_type[i] <-  suppressWarnings(getStationSubtype(unlist(strsplit(sid1[i], " "))[2], substr(sid1[i],1,3)))
        sid2[i] <- as.character(NA)
        sid2_type[i] <-  as.character(NA)
        sid3[i] <- as.character(NA)
        sid3_type[i] <-  as.character(NA)
      }
    }
    #sid1 <- setNames(sid1,"sid1")
    sid1 <- setNames(as.data.frame(sid1),"sid1")
    sid2 <- setNames(as.data.frame(sid2),"sid2")
    sid3 <- setNames(as.data.frame(sid3),"sid3")
    sid1_type <- setNames(as.data.frame(sid1_type),"sid1_type")
    sid2_type <- setNames(as.data.frame(sid2_type),"sid2_type")
    sid3_type <- setNames(as.data.frame(sid3_type),"sid3_type")
    i <- NULL
    for (i in 1:length(stationListInit$meta$sids)) {
      minDate[i] <- as.Date(range(unlist(stationListInit$meta$valid_daterange[i]))[1], "%Y-%m-%d")
      maxDate[i] <- as.Date(range(unlist(stationListInit$meta$valid_daterange[i]))[2], "%Y-%m-%d")
    }
    minDate <-  setNames(as.data.frame(minDate), "minDate")
    maxDate <-  setNames(as.data.frame(maxDate), "maxDate")
    # Force elevation to be numeric with precision of 1
    options(digits = 1)
    elev <- as.numeric(stationListInit$meta[,5])
    options(digits = 7)
    stationList <- cbind( uid, name=stationListInit$meta[,1], longitude, longitude, sid1, sid1_type, sid2, sid2_type, sid3, sid3_type, state=stationListInit$meta[,4], elev=stationListInit$meta[,5], minDate, maxDate)
    stationList$unitCode <- unitCode[1]
    # Convert factors to character vectors
    fc  <- sapply(stationList, is.factor)
    lc <- sapply(stationList, is.logical)
    stationList[, fc]  <- sapply(stationList[, fc], as.character)
    stationList[, lc]  <- sapply(stationList[, lc], as.character)
  }
  else {
    stationList <- NA # per John Paul's request - Issue #49
    #stationList <- cat("No stations for ", unitCode, "using distance ", distance) 
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


