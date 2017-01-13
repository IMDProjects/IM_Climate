#' Get daily climate data grids for specified parameter(s) and NPS or FWS unit(s)
#'
#' Takes one park code and a list of one or more climate parameters and requests daily climate data. Returns a grid or grids (by parameter) in ASCII format or an in-memory raster stack.
#' @param unitCode (optional) One unit code as a string. If not specified, defaults to CONUS geographic extent.
#' @param sDate sdate (required) Format as a string (yyyy-mm-dd, yyyymmdd, yyyy-mm, yyyymm, yyyy). The beginning of the desired date range.
#' @param eDate edate (required) Format as a string (yyyy-mm-dd, yyyymmdd, yyyy-mm, yyyymm, yyyy). The end of the desired date range.
#' @param distance (optional) Distance (in kilometers) to buffer park bounding box
#' @param climateParameters (optional) A list of one or more climate parameters (e.g. pcpn, mint, maxt, avgt).  If not specified, defaults to all parameters. See the ACIS Web Services page: http://www.rcc-acis.org/docs_webservices.html
#' @param filePath filePath (optional) Folder path for output ASCII grid(s). If specified, grid(s) are saved to the folder. Otherwise, grid(s) are saved to an in-memory raster stack (by date).
#' @return ASCII-formatted grid file for each parameter for each date or an in-memory raster stack with a layer for each parameter for each date
#' @examples \dontrun{
#' Two daily grids for PRWI for one date: returns one grid for each parameter for each date - 4 grids total
#' getDailyGrids(unitCode = list("PRWI"), sdate = "20160615", edate = "20160616", climateParameters = list("mint", "maxt"), filePath="d:\\temp\\trash")
#'
#' Two daily grids for GRSM for one date: print output to console
#' getDailyGrids(unitCode = list("GRSM"), sdate = "20160615", edate = "20160616", climateParameters = list("mint", "maxt"))
#' }
#' 
#' The same request for two daily grids for GRSM for one date: output to in-memory raster stack, t
#' t <- getDailyGrids(unitCode = list("GRSM"), sdate = "20160615", edate = "20160616", climateParameters = list("mint", "maxt"))
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
    lookups <- 
      fromJSON(system.file("ACISLookups.json", package = "IMClimateR"), flatten = TRUE) # assumes placement in package inst subfolder
    luElements  <- lookups$gridSources[gridElements$gridSource]
    
    # Configure image output
    fileNameRoot <- unlist(gridElements$gridSource)
    gridElements <- c(gridElements, grid = luElements[[1]]$code)
    if (is.null(filePath) == TRUE) {
      rasterStack <- stack()
    }
    
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
          sepDuration <- paste(paste("_", gridElements$duration, sep=""), "_", sep="")
          fileName <-
            paste(paste(
              paste(fileNameRoot, climateParameters[j], sep = "_"),
              resp$data[[i]][[1]],
              sep = sepDuration#"_dly_"
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
            if (outfile == "Success") {
              #outputRaster <- outputRasterStack()
              r <- raster(griddf)
              crs(r) <- luElements[[1]]$projectionCRS
              rasterStack <- stack(rasterStack, r)
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
        } # param loop end
      } # date loop end
      if (exists("rasterStack") == TRUE) { 
        return (rasterStack)
      }
    }
    else {
      print(paste("ERROR: ", dataResponseError))
    }
  }

#' Get monthly climate data grids for specified parameter(s) and NPS or FWS unit(s)
#'
#' Takes one park code and a list of one or more monthly climate parameters and requests monthly climate data. Returns a grid or grids (by parameter) in ASCII format or an in-memory raster stack.
#' @param unitCode (optional) One unit code as a string. If not specified, defaults to CONUS geographic extent.
#' @param sDate sdate (required) Format as a string (yyyy-mm, yyyymm, yyyy). The beginning of the desired date range.
#' @param eDate edate (required) Format as a string (yyyy-mm, yyyymm, yyyy). The end of the desired date range.
#' @param distance (optional) Distance (in kilometers) to buffer park bounding box
#' @param climateParameters (optional) A list of one or more monthly climate parameters (e.g. mly_pcpn, mly_mint, mly_maxt, mly_avgt).  If not specified, defaults to all parameters. See the ACIS Web Services page: http://www.rcc-acis.org/docs_webservices.html
#' @param filePath filePath (optional) Folder path for output ASCII grid(s). If specified, grid(s) are saved to the folder. Otherwise, grid(s) are saved to an in-memory raster stack (by date).
#' @return ASCII-formatted grid file for each parameter for each date or an in-memory raster stack with a layer for each parameter for each date
#' @examples \dontrun{
#' Two monthly grids for PRWI for one date: returns one grid for each parameter for each date - 4 grids total
#' getMonthlyGrids(unitCode = list("PRWI"), sdate = "201606", edate = "201607", climateParameters = list("mint", "maxt"), filePath="d:\\temp\\trash")
#'
#' Two monthly grids for GRSM for one date: print output to console
#' getMonthlyGrids(unitCode = list("GRSM"), sdate = "201606", edate = "201607", climateParameters = list("mint", "maxt"))
#' 
#' Get all monthly grids for one year for one parameter
#' getMonthlyGrids(unitCode = list("GRKO"), sdate = "190001", edate = "190012", climateParameters = list("mly_mint"))
#' 
#' #' The same request for two monthly grids for GRSM for one date: output to in-memory raster stack, t
#' t <- getMonthlyGrids(unitCode = list("GRSM"), sdate = "201606", edate = "201607", climateParameters = list("mint", "maxt"))
#' }
#' @export
#' 
getMonthlyGrids <-
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
    samplePeriod <- "mly"
    
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
        duration = "mly",
        gridSource = "PRISM",
        dataPrecision = 1,
        output = "json",
        meta = "ll"
      )
    
    # Image parameters from lookup file - used for output formatting and  request documentation
    lookups <- 
      fromJSON(system.file("ACISLookups.json", package = "IMClimateR"), flatten = TRUE) # assumes placement in package inst subfolder
    luElements  <- lookups$gridSources[gridElements$gridSource]
    paramElements <- lookups$elementAggregateGrid$code[lookups$elementAggregateGrid$duration == gridElements$duration]
    
    # Configure image output
    fileNameRoot <- unlist(gridElements$gridSource)
    gridElements <- c(gridElements, grid = luElements[[1]]$code)
    if (is.null(filePath) == TRUE) {
      rasterStack <- stack()
    }
    
    bList <- c(bList, output = unlist(gridElements$output))
    bList <- c(bList, grid = unlist(gridElements$grid))
    bList <- c(bList, meta = unlist(gridElements$meta))
    
    # If climateParameters is NULL, default to these parameters
    if (is.null(climateParameters) == TRUE) {
      climateParameters <- c(paramElements)
      #climateParameters <- list('pcpn', 'mint', 'maxt', 'avgt')
    }
    
    # Format incoming arguments
    dataURL <-  gsub(" ", "", paste(baseURL, webServiceSource))
    #climateElems <- paste(climateParameters, collapse = ",")
    paramCount <- length(climateParameters)
    
    # Iterate parameter list to create elems element:
    eList <- vector('list', paramCount)
    for (i in 1:paramCount) {
      e <-
        list(
          name = unlist(c(climateParameters[i])),
          #duration = gridElements$duration,
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
          sepDuration <- paste(paste("_", gridElements$duration, sep=""), "_", sep="")
          fileName <-
            paste(paste(
              paste(fileNameRoot, climateParameters[j], sep = "_"),
              resp$data[[i]][[1]],
              sep = sepDuration
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
            if (outfile == "Success") {
              #outputRaster <- outputRasterStack()
              r <- raster(griddf)
              crs(r) <- luElements[[1]]$projectionCRS
              rasterStack <- stack(rasterStack, r)
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
        } # param loop end
      } # date loop end
      if (exists("rasterStack") == TRUE) { 
        return (rasterStack)
      }
    }
    else {
      print(paste("ERROR: ", dataResponseError))
    }
  }


#' Get climate data grids for specified parameter(s) and NPS or FWS unit(s)
#'
#' Takes one park code and a list of one or more monthly climate parameters and requests monthly climate data. Returns a grid or grids (by parameter) in ASCII format or an in-memory raster stack.
#' @param unitCode (optional) One unit code as a string. If not specified, defaults to CONUS geographic extent.
#' @param sDate sdate (required) Format as a string (yyyy-mm, yyyymm, yyyy). The beginning of the desired date range.
#' @param eDate edate (required) Format as a string (yyyy-mm, yyyymm, yyyy). The end of the desired date range.
#' @param distance (optional) Distance (in kilometers) to buffer park bounding box
#' @param climateParameters (optional) A list of one or more monthly climate parameters (e.g. mly_pcpn, mly_mint, mly_maxt, mly_avgt).  If not specified, defaults to all parameters. See the ACIS Web Services page: http://www.rcc-acis.org/docs_webservices.html
#' @param duration (optional)  "dly" | "mly" | "yly" (i.e, daily, monthly, or yearly). If not specified, defaults to dly.
#' @param filePath filePath (optional) Folder path for output ASCII grid(s). If specified, grid(s) are saved to the folder. Otherwise, grid(s) are saved to an in-memory raster stack (by date).
#' @return ASCII-formatted grid file for each parameter for each date or an in-memory raster stack with a layer for each parameter for each date
#' @examples \dontrun{
#' Two monthly grids for PRWI for one date: returns one grid for each parameter for each date - 4 grids total
#' getGrids(unitCode = list("PRWI"), sdate = "201606", edate = "201607", climateParameters = list("mint", "maxt"), filePath="d:\\temp\\trash")
#'
#' Two monthly grids for GRSM for one date: print output to console
#' getGrids(unitCode = list("GRSM"), sdate = "201606", edate = "201607", climateParameters = list("mint", "maxt"))
#' 
#' Get all monthly grids for one year for one parameter
#' getGrids(unitCode = list("GRKO"), sdate = "190001", edate = "190012", climateParameters = list("mly_mint"))
#' 
#' #' The same request for two monthly grids for GRSM for one date: output to in-memory raster stack, t
#' t <- getGrids(unitCode = list("GRSM"), sdate = "201606", edate = "201607", climateParameters = list("mint", "maxt"))
#' }
#' @export
#' 
getGrids <-
  function (unitCode = NULL,
            sdate = NULL,
            edate = NULL,
            distance = NULL,
            climateParameters = NULL,
            duration = "dly",
            filePath = NULL) {
    # URLs and request parameters:
    # ACIS data services
    baseURL <- "http://data.rcc-acis.org/"
    webServiceSource <- "GridData"
    config <- add_headers(Accept = "'Accept':'application/json'")
    
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
        duration = duration,
        gridSource = "PRISM",
        dataPrecision = 1,
        output = "json",
        meta = "ll"
      )
    
    # Image parameters from lookup file - used for output formatting and  request documentation
    lookups <- 
      fromJSON(system.file("ACISLookups.json", package = "IMClimateR"), flatten = TRUE) # assumes placement in package inst subfolder
    luElements  <- lookups$gridSources[gridElements$gridSource]
    
    
    # Configure image output
    fileNameRoot <- unlist(gridElements$gridSource)
    gridElements <- c(gridElements, grid = luElements[[1]]$code)
    if (is.null(filePath) == TRUE) {
      rasterStack <- stack()
    }
    
    bList <- c(bList, output = unlist(gridElements$output))
    bList <- c(bList, grid = unlist(gridElements$grid))
    bList <- c(bList, meta = unlist(gridElements$meta))
    
    # If climateParameters is NULL, default to these parameters
    if (is.null(climateParameters == TRUE)) {
      if (duration == "dly") {
        #climateParameters <- list('pcpn', 'mint', 'maxt', 'avgt')
        climateParameters <- lookups$elementGrid$code
      }
      else {
        # Monthly (mly) or Yearly (yly)
        climateParameters <- lookups$elementAggregateGrid$code[lookups$elementAggregateGrid$duration == gridElements$duration]
      }
    }
    
    # Format incoming arguments
    dataURL <-  gsub(" ", "", paste(baseURL, webServiceSource))
    #climateParameters <- c(paramElements)
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
          sepDuration <- paste(paste("_", gridElements$duration, sep=""), "_", sep="")
          fileName <-
            paste(paste(
              paste(fileNameRoot, climateParameters[j], sep = "_"),
              resp$data[[i]][[1]],
              sep = sepDuration#"_dly_"
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
            if (outfile == "Success") {
              #outputRaster <- outputRasterStack()
              r <- raster(griddf)
              crs(r) <- luElements[[1]]$projectionCRS
              rasterStack <- stack(rasterStack, r)
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
        } # param loop end
      } # date loop end
      if (exists("rasterStack") == TRUE) { 
        return (rasterStack)
      }
    }
    else {
      print(paste("ERROR: ", dataResponseError))
    }
  }
