#' Get station data for specified parameter(s) and station(s)
#'
#' Takes a list of one or more parameters and one or more unique station IDs, requests station data, and returns it as a data frame
# @param dataURL URL for ACIS data service vending station data
#' @param climateParameters A list of one or more climate parameters (e.g. pcpn, mint, maxt, avgt, obst, snow, snwd).  If not specified, defaults to all parameters except degree days. See Table 3 on ACIS Web Services page: http://www.rcc-acis.org/docs_webservices.html
#' @param climateStations A list of one or more unique identifiers (uid) for climate stations. Can be a single item, a list of items, or a data frame of the findStation response.
#' @param sdate (optional) Default is period of record ("por"). If specific start date is desired, format as a string (yyyy-mm-dd or yyyymmdd). The beginning of the desired date range.
#' @param edate (optional) Default is period of record ("por"). IF specific end date is desired, format as a string (yyyy-mm-dd or yyyymmdd). The end of the desired date range.
#' @param filePathAndName (optional) File path and name including extension for output CSV file
#' @return A data frame containing the requested data. See User Guide for more details: https://docs.google.com/document/d/1B0rf0VTEXQNWGW9fqg2LRr6cHR20VQhFRy7PU_BfOeA/
#' @examples \dontrun{
#' Precipitation, temperature weather observations for one station for a specifc date range:
#'
#' getDailyWxObservations(climateParameters=list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), climateStations=25056, sdate="20150801", edate="20150831")
#'
#' All weather observations for a station for its period of record
#'
#' getDailyWxObservations(climateStations=60903)
#'
#' All weather observations for all stations (using a findStation response data frame: stationDF) for a specific date range:
#'
#' getDailyWxObservations(climateParameters=list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), climateStations=stationDF, sdate="20150801", edate="20150803")
#' }
#' @export
#'
# TODO: encapsulate in error block
# See https://github.com/hadley/httr/blob/master/vignettes/api-packages.Rmd

getDailyWxObservations <-
  function(climateParameters = NULL,
           climateStations,
           sdate = "por",
           edate = "por",
           filePathAndName = NULL) {
    # URLs and request parameters:
    # ACIS data services
    baseURL <- "http://data.rcc-acis.org/"
    webServiceSource <- "StnData"
    duration <- c("dly")
    # Parameter flags: f = ACIS flag, s = source flag
    paramFlags <- c("f,s")
    lookups <- 
      fromJSON(system.file("ACISLookups.json", package = "IMClimateR"), flatten = TRUE) # assumes placement in package inst subfolder
    #lookups <- fromJSON("ACISLookups.json", flatten = TRUE)
    luElements  <- lookups$element
    
    # If climateParameters is NULL, default to all parameters except degree days.
    if (is.null(climateParameters)) {
      climateParameters0 <- lookups$element$code
      # Remove degree days (v1.5); super cheesy... fix at some point
      climateParameters <- climateParameters0[1:7]
      #climateParameters <- list('pcpn', 'mint', 'maxt', 'avgt', 'obst', 'snow', 'snwd')
    }
    
    # Initialize response object
    dfResponse <- NULL
    
    # Format incoming arguments
    dataURL <-  gsub(" ", "", paste(baseURL, webServiceSource))
    
    # climateElems <- paste(climateParameters, collapse = ",")
    # paramCount <- length(climateParameters)
    # 
    # # Format POST request for use in httr
    # # Iterate parameter list to create elems element:
    # eList <- vector('list', paramCount)
    # for (i in 1:paramCount) {
    #   e <- list(name = unlist(c(climateParameters[i])), add = paramFlags)
    #   #print(e)
    #   eList[[i]] <- e
    # }
    # 
    # # Climate parameters as JSON with flags
    # elems <- toJSON(eList, auto_unbox = TRUE)
    
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
      body <- formatRequest(requestType = "getWxObservations", climateParameters = climateParameters, sdate, edate, cUid, duration = duration, paramFlags = c("f,s"), )
      
      # bList <-
      #   list(
      #     uid = cUid,
      #     sdate = sdate,
      #     edate = edate,
      #     elems = elems
      #   )
      #bList <- list(uid = climateStations, sdate = sdate, edate = edate, elems = elems)
      #bList <- list(sid = climateStations, sdate = sdate, edate = edate, elems = elems)
      
     # body  <- stripEscapes(bList)
      
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
      
      if (grepl("data",content(dataResponseInit, "text")) == FALSE) {
        dfResponse <- content(dataResponseInit, "text")
      }
      else {
        # Format climate data object
        rList <- content(dataResponseInit)
        dataResponseError <- rList$error
        
        # Start building the data frame by populating the date vector
        if (is.null(dataResponseError)) {
          df <-
            formatWxObservations(
              rList,
              duration = duration,
              climateParameters = climateParameters,
              reduceCodes = NULL,
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
