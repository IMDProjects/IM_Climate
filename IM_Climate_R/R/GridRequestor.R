#' Get daily climate data grids for specified parameter(s) and NPS unit(s)
#'
#' Takes one park code and a list of one or more climate parameters and requests daily climate data. Returns a grid or grids (by parameter) in ASCII format.
#' @unitCode unitCode (optional) One NPS unit code as a string. If not specified, defaults to CONUS geographic extent.
#' @param sDate sdate (required) Format as a string (yyyy-mm-dd, yyyymmdd, yyyy-mm, yyyymm, yyyy). The beginning of the desired date range.
#' @param eDate edate (required) Format as a string (yyyy-mm-dd, yyyymmdd, yyyy-mm, yyyymm, yyyy). The end of the desired date range.
#' @param distance (optional) Distance (in kilometers) to buffer park bounding box
#' @climateParameters (optional) A list of one or more climate parameters (e.g. pcpn, mint, maxt, avgt).  If not specified, defaults to all parameters. See the ACIS Web Services page: http://www.rcc-acis.org/docs_webservices.html
#' @filePath filePath (optional) Folder path for output ASCII grid(s). If specified, grid(s) are saved to the folder. Otherwise, grid(s) are saved to the current working directory.
#' @return ASCII-formatted grid file for each parameter
#' @export

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
    }
    else {
      # NPS Park bounding box
      bboxURLBase <- "http://irmaservices.nps.gov/v2/rest/unit/CODE/geography?detail=envelope&dataformat=wkt&format=json"
      if (is.null(distance)) {
        bboxExpand  = 0.0
      }
      else {
        bboxExpand = distance*0.011
      }
      
      # TODO: move into helper function in utilityFunctions.R
      # Get bounding box for park(s)
      bboxURL <- gsub("CODE", unitCode, bboxURLBase)
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
    }
    
    # Initialize body of request
    bList <- list(bbox = bbox, sdate = sdate, edate = edate)
    
    # Hard-coded request elements
    gridElements <- list(interval = "dly", duration = "dly", gridSource = "PRISM", dataPrecision = 1, output = "json", meta = "ll")
    # if (is.null(filePath)==FALSE) {  
    #   # save grid(s) to a folder
    #   gridElements <- c(gridElements, output="json")
    # }
    
    # Elements from lookup file - used for output formatting and  request documentation
    lookups <- fromJSON("ACISLookups.json", flatten = TRUE)
    luElements  <- lookups$gridSources[gridElements$gridSource]
    
    # Configure image output
    fileNameRoot <- unlist(gridElements$gridSource)
    gridElements <- c(gridElements, grid = luElements[[1]]$code)
    # if (is.null(filePath)==FALSE) {
    #   #bList[[length(bList)+1]] <- list(output = unlist(gridElements$output))
    #   bList <- c(bList, output=unlist(gridElements$output))
    # }
    bList <- c(bList, output=unlist(gridElements$output))
    bList <- c(bList, grid = unlist(gridElements$grid))
    #bList <- c(bList, prec = unlist(gridElements$dataPrecision))
    #bList[[length(bList)+1]] <- list(grid = unlist(gridElements$grid))
    
    # If climateParameters is NULL, default to these parameters
    if (is.null(climateParameters)) {
      climateParameters <- list('pcpn', 'mint', 'maxt', 'avgt')
    }
    
    # Format incoming arguments
    dataURL <-  gsub(" ", "", paste(baseURL, webServiceSource))
    climateElems <- paste(climateParameters, collapse = ",")
    paramCount <- length(climateParameters)
    
    # Iterate parameter list to create elems element:
    eList <- vector('list', paramCount)
    for (i in 1:paramCount) {
      e <- list(name = unlist(c(climateParameters[i])), interval = gridElements$interval, duration = gridElements$duration, prec = gridElements$dataPrecision)
      #print(e)
      eList[[i]] <- e
    }
    
    # Climate parameters as JSON
    elems <- toJSON(eList, auto_unbox = TRUE)
    body  <- stripEscapes(c(bList, elems=elems))
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
      #print(dataResponseInit)
      # ideas here: http://zevross.com/blog/2015/02/12/using-r-to-download-and-parse-json-an-example-using-data-from-an-open-data-portal/
      # and ftp://cran.r-project.org/pub/R/web/packages/ascii/ascii.pdf
      resp <- fromJSON(content(dataResponseInit, "text"), simplifyVector = FALSE)
      respList <- content(dataResponseInit)$data
      respJSON  <- toJSON(content(dataResponseInit, "text"), auto_unbox = TRUE)
      # get the second grid content(dataResponseInit)$data[[2]][[2]]
      print(class(resp))
      for (i in 1:length(resp$data)) {
        # Convert each output to ASCII format
        fileName <- paste(paste(paste(fileNameRoot, climateParameters[1], sep = "_"), resp$data[[i]][[1]], sep = "_"), ".asc")
        #fileName <- paste(paste(paste(fileNameRoot, climateParameters[1], sep = "_"), gsub(" ", "", resp$data[[i]][[1]]), sep = "_dly_"), ".asc")
        # grid data is resp$data[[i]][[2]]) as nested list
        print(resp$data[[i]][[1]]) #image date
        print(length(resp$data[[i]][[2]])) #count of image rows
        # get grid data as a matrix
        gridMatrix <- do.call(cbind, resp$data[[i]][[2]])
        griddf <- NULL
        for (j in 1:ncol(gridMatrix)) {
          griddf <- cbind(griddf, as.numeric(gridMatrix[,j]))
          #griddf <- cbind(griddf, as.data.frame(as.numeric(gridMatrix[,j])))
          #griddf <- cbind(griddf, as.data.frame(gridMatrix[,j]))
        }
        outfile <- outputAscii(griddf, paste(filePath, fileName, sep="\\"), bbox, luElements[[1]])
        #ras = raster(griddf)
        #writeRaster(ras, "D:\\temp\\trash\\test.asc", overwrite=TRUE, "ascii")
        #r = raster(as.matrix(griddf), xmn=LLX, ymn=LLY, xmx=URX, ymx=URY)
        #r = raster(vals=as.data.frame(griddf), resolution=c(as.numeric(luElements$PRISM$cellSize)), xmn=LLX, ymn=LLY)
        #writeRaster(ras, "D:\\temp\\trash\\test.asc", overwrite=TRUE, "ascii")
      }
      #print(stripEscapesGrid(resp))
      if (!is.null(filePath)) {
        
      }
      else {
        
      }
    }
    else {
      print(paste("ERROR: ", dataResponseError))
    }
     # output <- tryCatch({
     #    dfResponse = "test"
     # }, warning = function(w) {
     #    print(paste("WARNING: ", w))
     #    
     # }, error = function(e) {
     #    print(paste("ERROR: ", e))
     # }, finally = {
     #   print("Finished try/catch")
     # })
    # output <- try({
    #   
    # })
    # 
    # if (class(output) == "try-error") {
    #   print("ERROR: error retrieving data")
    # }
    # else {
    #   print(output)
    # }
    
    
  }