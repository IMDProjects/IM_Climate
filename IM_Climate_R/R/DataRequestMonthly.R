#' Get station data for specified parameter(s) and station(s)
#'
#' Takes a list of one or more parameters and one or more unique station IDs, requests station data, and returns it as a data frame
# @param dataURL URL for ACIS data service vending station data
#' @param climateStations A list of one or more unique identifiers (uid) for climate stations. Can be a single item, a list of items, or a data frame of the findStation response.
#' @param climateParameters A list of one or more climate parameters (e.g. pcpn, mint, maxt, avgt, obst, snow, snwd).  If not specified, defaults to all parameters except degree days. See Table 3 on ACIS Web Services page: http://www.rcc-acis.org/docs_webservices.html
#' @param reduceCodes (optional) A list of one or more reduce codes. If missing, defaults to min, max, sum, and mean.
#' @param sdate (optional) Default is period of record ("por"). If specific start date is desired, format as a string (yyyy-mm-dd or yyyymmdd). The beginning of the desired date range.
#' @param edate (optional) Default is period of record ("por"). IF specific end date is desired, format as a string (yyyy-mm-dd or yyyymmdd). The end of the desired date range.
#' @param maxMissing (optional) Maximum number of missing days within a month before the aggregate is not calculated. If missing, defaults to 1 (~3.3% missing days/month).
#' @param filePathAndName (optional) File path and name including extension for output CSV file
#' @return A data frame containing the requested data. See User Guide for more details: https://docs.google.com/document/d/1B0rf0VTEXQNWGW9fqg2LRr6cHR20VQhFRy7PU_BfOeA/
#' @examples \dontrun{
#' Precipitation, temperature weather observations for one station for a specifc date range:
#'
#' getMonthlyWxObservations(climateParameters=list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), climateStations=25056, sdate="20150801", edate="20150831")
#'
#' All weather observations for a station for its period of record
#'
#' getMonthlyWxObservations(climateStations=60903)
#'
#' All weather observations for all stations (using a findStation response data frame: stationDF) for a specific date range:
#'
#' getMonthlyWxObservations(climateParameters=list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), climateStations=stationDF, sdate="20150801", edate="20150803")
#' }
#' @export
getMonthlyWxObservations <-
  function(climateStations,
           climateParameters = NULL,
           reduceCodes = NULL,
           sdate = "por",
           edate = "por",
           maxMissing = NULL,
           filePathAndName = NULL) {
    # URLs and request parameters:
    # ACIS data services
    baseURL <- "http://data.rcc-acis.org/"
    webServiceSource <- "StnData"
    # Parameter flags: f = ACIS flag, s = source flag
    paramFlags <- c("f,s")
    metaElements <- list('uid', 'll', 'name', 'elev', 'sids', 'state')
    lookups <-
      fromJSON(system.file("ACISLookups.json", package = "IMClimateR"),
               flatten = TRUE) # assumes placement in package inst subfolder
    luElements  <- lookups$element
    
    #TODO: By climateParam: add duration,interval,reduce, add(''mcnt'), and maxMissing
    
    # If climateParameters is NULL, default to all parameters except degree days.
    if (is.null(climateParameters)) {
      climateParameters <-
        list('pcpn', 'mint', 'maxt', 'avgt', 'obst', 'snow', 'snwd')
    }
    # If reduceCodes is NULL, default to min, max, sum, and mean.
    if (is.null(reduceCodes)) {
      reduceCodes <- list('min', 'max', 'sum', 'mean')
    }
    # If maxMissing is NULL, default to 1 (~3.3% missing days/month).
    if (is.null(maxMissing)) {
      maxMissing <- 1
    }
    
    # Initialize response object
    dfResponse <- NULL
    
    # Format incoming arguments
    dataURL <-  gsub(" ", "", paste(baseURL, webServiceSource))
    climateElems <- paste(climateParameters, collapse = ",")
    paramCount <- length(climateParameters)
    # Change to an iteration by param:
    rCodes <- paste(reduceCodes, collapse = ",")
    
    mmElem <- list(maxmissing = maxMissing)
    
    # Format POST request for use in httr
    # Iterate parameter list to create elems element:
    eList <- vector('list', paramCount)
    for (i in 1:paramCount) {
      e <- list(name = unlist(c(climateParameters[i])), add = paramFlags)
      #print(e)
      eList[[i]] <- e
    }
    
    # Climate parameters as JSON with flags
    elems <- toJSON(eList, auto_unbox = TRUE)
    
    
    # Output file
    if (!is.null(filePathAndName)) {
      write.table(
        dfResponse,
        file = filePathAndName,
        sep = ",",
        row.names = FALSE,
        qmethod = "double"
      )
    }
    else {
      return (dfResponse)
    }
    return (dfResponse)
  }