#' Get station data for specified parameter(s) and station(s)
#'
#' Takes a list of one or more parameters and one or more unique station IDs, requests station data, and returns it as a data frame. Note: For monthly data, value vectors returned as character format to accommodate missing records ("M")
# @param dataURL URL for ACIS data service vending station data
#' @param climateStations A list of one or more unique identifiers (uid) for climate stations. Can be a single item, a list of items, or a data frame of the findStation response.
#' @param climateParameters A list of one or more climate parameters (e.g. pcpn, mint, maxt, avgt, obst, snow, snwd).  If not specified, defaults to all parameters except degree days. See Table 3 on ACIS Web Services page: http://www.rcc-acis.org/docs_webservices.html
#' @param sdate (optional) Default is period of record ("por"). If specific start date is desired, format as a string (yyyy-mm-dd or yyyymmdd). The beginning of the desired date range.
#' @param edate (optional) Default is period of record ("por"). If specific end date is desired, format as a string (yyyy-mm-dd or yyyymmdd). The end of the desired date range.
#' @param duration (optional) Default is daily ("dly"). Use "mly" for monthly.
#' @param reduceCodes (optional) For monthly requests, a list of one or more reduce codes. If missing, defaults to min, max, sum, and mean.
#' @param maxMissing (optional) Maximum number of missing days within a month before the aggregate is not calculated (applied to each parameter). If missing, defaults to 1 (~3.3 percent missing days/month).
#' @param filePathAndName (optional) File path and name including extension for output CSV file
#' @return A data frame containing the requested data. Note: date vector is in character format, not date format. See User Guide for more details: https://docs.google.com/document/d/1B0rf0VTEXQNWGW9fqg2LRr6cHR20VQhFRy7PU_BfOeA/
#' @examples \dontrun{
#' Precipitation, temperature (daily) weather observations for one station for a specifc date range:
#'
#' getWxObservations(climateParameters=list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), climateStations=25056, sdate="20150801", edate="20150831")
#'
#' The same request written to a CSV file:
#' 
#' getWxObservations(climateParameters=list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), climateStations=25056, sdate="20150801", edate="20160831", filePathAndName = "D:\\temp\\trash\\dailyObs_station25056.csv")
#'  
#' All daily weather observations for a station for its period of record
#'
#' getWxObservations(climateStations=60903)
#' 
#' All monthly weather observations for two stations for a specified date range:
#' 
#' getWxObservations(climateStations = list(61193, 26215), sdate="201401", edate = "201501", duration="mly", maxMissing = NULL)
#'
#' Monthly weather observations for precipitation for a station from beginning of record through Sept 2016
#' 
#' getWxObservations(climateStations = list(26215), climateParameters = list('pcpn'), reduceCodes = list('min'), edate= "2016-09", duration="mly", maxMissing = 2)
#'
#' All daily weather observations for all stations (using a findStation response data frame: stationDF) for a specific date range:
#'
#' getWxObservations(climateParameters=list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), climateStations=stationDF, sdate="20150801", edate="20150803")
#' }
#' @export
#' 
getWxObservations <-
  function(climateStations,
           climateParameters = NULL,
           sdate = "por",
           edate = "por",
           duration = "dly",
           reduceCodes = NULL,
           maxMissing = NULL,
           filePathAndName = NULL) {
    # URLs and request parameters:
    # ACIS data services
    baseURL <- "http://data.rcc-acis.org/"
    webServiceSource <- "StnData"
    # Parameter flags: f = ACIS flag, s = source flag; only valid when requesting daily data
    #paramFlags <- c("f,s")
    # Reduce flags: mcnt = count of missing values in the reduction period
    reduceFlags <- c("mcnt")
    reduceList <- NULL
    # Interval and duration (TODO: add as function params in v1.4)
    interval <- c("dly")
    #duration <- c("mly")
    metaElements <-
      list('uid', 'll', 'name', 'elev', 'sids', 'state')
    lookups <-
      fromJSON(system.file("ACISLookups.json", package = "IMClimateR"),
               flatten = TRUE) # assumes placement in package inst subfolder
    luElements  <- lookups$element
    
    # If climateParameters is NULL, default to all parameters except degree days.
    if (is.null(climateParameters)) {
      climateParameters0 <- lookups$element$code
      # Remove degree days (v1.5); super cheesy... fix at some point
      climateParameters <- climateParameters0[1:7]
      #climateParameters <- list('pcpn', 'mint', 'maxt', 'avgt', 'obst', 'snow', 'snwd')
    }
    if (duration == "mly") {
      # If reduceCodes is NULL, default to min, max, sum, and mean.
      if (is.null(reduceCodes)) {
        reduceCodes <- list('min', 'max', 'sum', 'mean')
      }
      reduceList <- vector('list', length(reduceCodes))
      for (j in 1:length(reduceCodes)) {
        r <- list(reduce = unlist(reduceCodes[j]), add = reduceFlags)
        reduceList[[j]] <- r #unlist(c(r))
      }
      # If maxMissing is NULL, default to 1 (~3.3% missing days/month).
      if (is.null(maxMissing)) {
        maxMissing <- 1
      }
    }
    
    # Initialize response object
    dfResponse <- NULL
    
    # Format incoming arguments
    dataURL <-  gsub(" ", "", paste(baseURL, webServiceSource))
    climateElems <- paste(climateParameters, collapse = ",")
    paramCount <- length(climateParameters)
    
    # Iterate for each station
    if (is.data.frame(climateStations)) {
      listStations = as.list(climateStations$uid)
    }
    else if (is.list(climateStations)) {
      listStations = climateStations
    }
    else {
      listStations = as.list(climateStations)
    }
    for (s in 1:length(listStations)) {
      df <- NULL
      cUid <- unlist(listStations[s])
      body <- formatRequest(requestType = "getWxObservations", climateParameters = climateParameters, sdate, edate, cUid, duration = duration, reduceList = reduceList, maxMissing = maxMissing)
      
      # This returns the full response - need to use content() and parse
      # content(dataResponseInit) results in a list lacking column names but containing data which needs to be
      # converted to dataFrame with appropriate vectors
      dataResponseInit <-
        POST(
          "http://data.rcc-acis.org/StnData",
          accept_json(),
          add_headers("Content-Type" = "application/json"),
          body = body,
          verbose()
        )
      
      if (grepl("data", content(dataResponseInit, "text")) == FALSE) {
        dfResponse <- content(dataResponseInit, "text")
      }
      else {
        # Format climate data object
        rList <- content(dataResponseInit)
        dataResponseError <- rList$error
        if (is.null(dataResponseError)) {
          df <-
            formatWxObservations(
              rList,
              duration = duration,
              climateParameters = climateParameters,
              reduceCodes = reduceCodes,
              luElements = luElements
            )
          # Create output object
          if (is.data.frame(dfResponse)) {
            dfResponse <- rbind(dfResponse, df)
          }
          else {
            dfResponse <- df
          }
        }
        else {
          dfResponse <- dataResponseError
        }
      }
    }
    
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
