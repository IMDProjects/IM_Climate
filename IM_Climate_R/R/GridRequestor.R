#' Get daily climate data grids for specified parameter(s) and NPS unit(s)
#'
#' Takes one park code and a list of one or more climate parameters and requests daily climate data. Returns a grid or grids (by parameter) in ASCII format.
#' @param unitCode (optional) One unit code as a string. If not specified, defaults to CONUS geographic extent.
#' @param sDate sdate (required) Format as a string (yyyy-mm-dd, yyyymmdd, yyyy-mm, yyyymm, yyyy). The beginning of the desired date range.
#' @param eDate edate (required) Format as a string (yyyy-mm-dd, yyyymmdd, yyyy-mm, yyyymm, yyyy). The end of the desired date range.
#' @param distance (optional) Distance (in kilometers) to buffer park bounding box
#' @param climateParameters (optional) A list of one or more climate parameters (e.g. pcpn, mint, maxt, avgt).  If not specified, defaults to all parameters. See the ACIS Web Services page: http://www.rcc-acis.org/docs_webservices.html
#' @param filePath filePath (optional) Folder path for output ASCII grid(s). If specified, grid(s) are saved to the folder. Otherwise, grid(s) are saved to the current working directory.
#' @return ASCII-formatted grid file for each parameter
#' @examples \dontrun{
#' Two daily grids for PRWI for one date: returns one grid for each parameter for each date - 4 grids total
#' getDailyGrids(unitCode = list("PRWI"), sdate = "20160615", edate = "20160616", climateParameters = list("mint", "maxt"), filePath="d:\\temp\\trash")
#'
#' Two daily grids for GRSM for one date: print output to console
#' getDailyGrids(unitCode = list("GRSM"), sdate = "20160615", edate = "20160616", climateParameters = list("mint", "maxt"))
#' }
#' @export
#' 

getDailyGrids <-
  function (unitCode = NULL,
            sdate = NULL,
            edate = NULL,
            distance = NULL,
            climateParameters = NULL,
            filePath = NULL) {
    # URLs and request parameters:
    # ACIS data services
    baseURL <- "http://data.rcc-acis.org/"
    webServiceSource <- "GridData"
    config <- add_headers(Accept = "'Accept':'application/json'")
    samplePeriod <- "dly"
    
    # Default to CONUS extent
    if (is.null(unitCode)) {
      bbox <- "-130, 20,-50, 60"
    } else {
      # NPS Park bounding box
      if (is.null(distance)) {
        bboxExpand  = 0.0
      } else {
        bboxExpand = distance * 0.011 # convert km to decimal degrees
      }
      bbox <- getBBox(unitCode, bboxExpand)
    }
    
    # Initialize body of request
    bList <- list(bbox = bbox,
                  sdate = sdate,
                  edate = edate)
    
    # Hard-coded request elements
    gridElements <-
      list(
        interval = "dly",
        duration = "dly",
        gridSource = "PRISM",
        dataPrecision = 1,
        output = "json",
        meta = "ll"
      )
    
    # Image parameters from lookup file - used for output formatting and  request documentation
    lookups <- fromJSON("ACISLookups.json", flatten = TRUE)
    luElements  <- lookups$gridSources[gridElements$gridSource]
    
    # Configure image output
    fileNameRoot <- unlist(gridElements$gridSource)
    gridElements <- c(gridElements, grid = luElements[[1]]$code)
    
    bList <- c(bList, output = unlist(gridElements$output))
    bList <- c(bList, grid = unlist(gridElements$grid))
    bList <- c(bList, meta = unlist(gridElements$meta))
    
    # If climateParameters is NULL, default to these parameters
    if (is.null(climateParameters == TRUE)) {
      climateParameters <- list('pcpn', 'mint', 'maxt', 'avgt')
    }
    
    # Format incoming arguments
    dataURL <-  gsub(" ", "", paste(baseURL, webServiceSource))
    climateElems <- paste(climateParameters, collapse = ",")
    paramCount <- length(climateParameters)
    
    # Iterate parameter list to create elems element:
    eList <- vector('list', paramCount)
    for (i in 1:paramCount) {
      e <-
        list(
          name = unlist(c(climateParameters[i])),
          interval = gridElements$interval,
          duration = gridElements$duration,
          prec = gridElements$dataPrecision
        )
      #print(e)
      eList[[i]] <- e
    }
    
    # Climate parameters as JSON
    elems <- toJSON(eList, auto_unbox = TRUE)
    body  <- stripEscapes(c(bList, elems = elems))
    print(dataURL)
    print(body)
    
    # Format POST request for use in httr
    # Initialize response object
    dfResponse <- NULL
    # This returns the full response - need to use content() and parse
    dataResponseInit <-
      POST(
        dataURL,
        accept_json(),
        add_headers("Content-Type" = "application/json"),
        body = body,
        verbose()
      )
    
    # Format climate data object
    rList <- content(dataResponseInit)
    dataResponseError <- rList$error
    if (is.null(dataResponseError)) {
      resp <-
        fromJSON(content(dataResponseInit, "text"), simplifyVector = FALSE)
      #respJSON  <- toJSON(content(dataResponseInit, "text"), auto_unbox = TRUE)
      for (i in 1:length(resp$data)) {
        # Convert each output to ASCII format - grid data is resp$data[[i]][[2]]) as nested list
        print(resp$data[[i]][[1]]) #image date
        # Get the minimum grid center value
        minLon <- min(as.numeric(unlist(resp$meta$lon)))
        minLat <- min(as.numeric(unlist(resp$meta$lat)))
        #print(length(resp$data[[i]][[2]])) #count of image rows
        # Get grid data as a matrix; output to file or console
        for (j in 1:length(climateParameters)) {
          fileName <- NULL
          fileName <-
            paste(paste(
              paste(fileNameRoot, climateParameters[j], sep = "_"),
              resp$data[[i]][[1]],
              sep = "_dly_"
            ), ".asc", sep = "")
          #fileName <- cat(paste(paste(fileNameRoot, climateParameters[j], sep = "_"), resp$data[[i]][[1]], sep = "_dly_"), ".asc")
          #print(fileName)
          gridMatrix <- do.call(rbind, resp$data[[i]][[j + 1]])
          griddf <- NULL
          for (k in 1:ncol(gridMatrix)) {
            # for proper image orientation, flip matrix columns with rev()
            griddf <-
              cbind(griddf, as.numeric(rev(gridMatrix[, k])))
          }
          if (is.null(filePath) == FALSE) {
            #print(griddf)
            outfile <-
              outputAscii(griddf,
                          paste(filePath, fileName, sep = "\\"),
                          minLon,
                          minLat,
                          luElements[[1]])
            if (outfile == "Success") {
              print(
                cat(
                  "SUCCESS: Created raster(s) for",
                  unlist(unitCode),
                  "using climateParameter=",
                  unlist(climateParameters)[j],
                  "in " ,
                  filePath
                )
              )
            }
            else {
              print(
                cat(
                  "ERROR: Unable to create raster(s) for ",
                  unlist(unitCode),
                  "using climateParameter=",
                  unlist(climateParameters)[j]
                )
              )
            }
          }
          else {
            print("INFO: No filePath specified. Output written to console:\n")
            outfile <-
              outputAscii(griddf, "", minLon, minLat, luElements[[1]])
          }
        }
      }
    }
    else {
      print(paste("ERROR: ", dataResponseError))
    }
  }