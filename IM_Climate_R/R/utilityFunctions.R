#' Utility functions for IMClimateR
#'
#' getStationType function uses the station identifier type code to lookup the station type description
#' @param testType station identifier type code
#' @param testSid first three characters of the station identifier
#' @export
#'

getStationSubtype <- function(testType, testSid) {
  # ACIS lookup
  acisLookup <-
    fromJSON(system.file("ACISLookups.json", package = "IMClimateR")) # assumes placement in package inst subfolder
  typeDesc <-
    acisLookup$stationIdType$description[acisLookup$stationIdType$code == testType]
  subtypeDesc <- NULL
  # If subtypes exist for station type, find matching subtype
  if (!is.na(testType)) {
    if (!acisLookup$stationIdType$subtypes[acisLookup$stationIdType$code == testType] == "") {
      subtypes <-
        unlist(acisLookup$stationIdType$subtypes[acisLookup$stationIdType$code == testType])
      if (!length(subtypes) == 0 && !subtypes == "") {
        if (!is.na(names(strsplit(
          unlist(acisLookup$stationIdType$subtypes[acisLookup$stationIdType$code == testType])[testSid], '\n'
        )[testSid]))) {
          tempdf <-
            as.data.frame(strsplit(unlist(
              acisLookup$stationIdType$subtypes[acisLookup$stationIdType$code == testType]
            )[testSid], '\n')[testSid])
          typeDesc <- as.character(as.vector(tempdf[1, ]))
        }
      }
    }
  }
  
  return(typeDesc)
}

#' formatRequest generates the JSON-formatted request to send to ACIS
#' @param requestType type of request: getDailyWxObservations, getMonthlyWxObservations, getGrids, (findStation)
#' @param climateParameters A list of one or more climate parameters defined in calling source
#' @param sdate sdate (required) Start data defined in calling source
#' @param edate sdate (required) End date defined in calling source
#' @param cUID (optional) station UID defined in calling source, used for getWXObservation requests
#' @param duration (optional) station data duration specified in calling source; used for getWxObservations and getGrids requests
#' @param paramFlags (optional) used for getWxObservations (daily). Parameter flags: f = ACIS flag, s = source flag
#' @param reduceList (optional) used for getWxObservations (monthly). Defaults to min, max, sum, and mean.
#' @param maxMissing (optional) used for getWxObservations (monthly). Defaults to 1 (~3.3% missing days/month).
#' @param gridElements grid request values defined in calling source
#' @export
#' 
formatRequest <- function(requestType, climateParameters, sdate, edate, cUid=NULL, duration=NULL, paramFlags=NULL, reduceList=NULL, maxMissing=NULL, gridElements=NULL) {
  print(requestType)
  
  # Hard-coded request elements
  # Parameter flags: f = ACIS flag, s = source flag
  #paramFlags <- c("f,s")
  # Metadata elements (not used explicitly)
  metaElements <-
    list('uid', 'll', 'name', 'elev', 'sids', 'state')
  # # Used for grid requests
  # gridElements <-
  #   list(
  #     #interval = "dly",
  #     duration = duration,
  #     gridSource = "PRISM",
  #     dataPrecision = 1,
  #     output = "json",
  #     meta = "ll"
  #   )
  # gridElements <- c(gridElements, grid = luElements[[1]]$code)
  # Reduce flags: mcnt = count of missing values in the reduction period
  reduceFlags <- c("mcnt")
  paramCount <- length(climateParameters)
  if (!is.null(reduceList)) {
    reduceCount <- length(reduceList)
  }
  # List of elements
  eList <- NULL
  
  # Build request
  if (requestType == "getWxObservations") {
    # Build elems list
    if (duration == "mly") {
      eList <- vector('list', paramCount*reduceCount)
      counter <- 1
      # Iterate parameter list to create elems element:
      for (i in 1:paramCount) {
        for (j in 1:reduceCount) { #listJ, listI
          e <-
            list(
              name = unlist(c(climateParameters[i])),
              interval = "dly",#interval,
              duration = duration,
              reduce = c(reduceList[j]), 
              maxmissing = maxMissing #unlist(mmElem)
            )
          eList[[counter]] <- e
          counter <- counter + 1
        }
      }
    }
    else {
      eList <- vector('list', paramCount)
      # Iterate parameter list to create elems element:
      for (i in 1:paramCount) {
        e <- list(name = unlist(c(climateParameters[i])), add = paramFlags)
        #print(e)
        eList[[i]] <- e
      }
    }
    # Climate parameters as JSON with flags
    elems <- toJSON(eList, auto_unbox = TRUE)
    # Build body (bList)
    bList <-
      list(
        uid = cUid,
        sdate = sdate,
        edate = edate,
        elems = elems
      )
    reqBody  <- stripEscapes(bList)
  }
  else if ("getGrids") {
    # Build elems list
    # Iterate parameter list to create elems element:
    # Iterate parameter list to create elems element:
    eList <- vector('list', paramCount)
    for (i in 1:paramCount) {
      e <-
        list(
          name = unlist(c(climateParameters[i])),
          #interval = gridElements$interval,
          duration = gridElements$duration,
          prec = gridElements$dataPrecision
        )
      #print(e)
      eList[[i]] <- e
    }
    # Climate parameters as JSON with flags
    elems <- toJSON(eList, auto_unbox = TRUE)
    # Build body (bList)
    bList <- c(bList, output = unlist(gridElements$output))
    bList <- c(bList, grid = unlist(gridElements$grid))
    bList <- c(bList, meta = unlist(gridElements$meta))
    
    reqBody  <- stripEscapes(c(bList, elems = elems))
  }
  # else { # placeholder for findStation
  #   # Build elems list
  #   # Iterate parameter list to create elems element:
  #   eList <- NULL
  #   
  #   # Build body (bList)
  # }
  
  # Return request JSON
  return(reqBody)
}

#' formatWxObservations converts get*WxObservation response to a data frame, iterating by date and value
#' @param responseContent list of response arrays containing name/value pairs: meta (default), data (date, values) 
#' @param duration station data duration specified in calling source 
#' @param climateParameters A list of one or more climate parameters defined in calling source
#' @param reduceCodes A list of one or more reduce codes defined in calling source
#' @param luElements lookup values defined in calling source
#' @export
#'
formatWxObservations  <- function(rList, duration, climateParameters, reduceCodes, luElements) {
  # Initialize return object (table or dataFrame)
  df <- NULL
  dfResponse <- NULL
  # Initialize vectors for SID type
  sid1_type = c()
  sid2_type = c()
  sid3_type = c()
  
  # R does not support the YYYY-MM format for a Date object. Hence, for monthly observations,
  # the date vector is in character format
  dfDate <-
    as.data.frame(cbind(unlist(lapply(
      rList$data, "[", 1
    )[][])))
  colnames(dfDate) <- "date"
  if(duration == "dly") {
    dfDate$date <- as.Date(as.character(as.vector(dfDate$date)), "%Y-%m-%d")
  }
  else {
    dfDate$date <- as.character(as.vector(dfDate$date))
  }
  
  # Populate 'metadata' i.e. station info; accommodate missing and unordered items
  dfMetaInit <-  t(as.data.frame(rList$meta))
  dfMeta <-
    as.data.frame(as.character(as.vector(strsplit(
      dfMetaInit[, 1], " "
    )$uid)))
  #dfMeta <- as.data.frame(as.character(as.vector(dfMetaInit[1, ])))
  colnames(dfMeta)[1]  <- "uid"
  #dfMeta$uid <- as.numeric(dfMeta$uid)
  
  dfMeta  <-
    cbind(dfMeta, as.data.frame(as.character(as.vector(
      paste(strsplit(dfMetaInit[, 1], " ")$name, collapse = " ")
    ))))
  colnames(dfMeta)[2]  <- "name"
  dfMeta  <-
    cbind(dfMeta, as.data.frame(as.numeric(as.vector(
      rList$meta$ll[1]
    ))))
  #dfMeta  <- cbind(dfMeta, as.data.frame(as.numeric(as.vector(dfMetaInit[2, ]))))
  colnames(dfMeta)[3]  <- "longitude"
  dfMeta  <-
    cbind(dfMeta, as.data.frame(as.numeric(as.vector(
      rList$meta$ll[2]
    ))))
  #dfMeta  <- cbind(dfMeta, as.data.frame(as.numeric(as.vector(dfMetaInit[3, ]))))
  colnames(dfMeta)[4]  <- "latitude"
  
  # Assumes sids element contains 3 members (even if 2 are empty)
  # Suppress warnings from getStationSubtype(): raised due to conversion necessary because data.frame vector access technique does not recognize column name
  dfMeta  <-
    cbind(dfMeta, as.data.frame(as.character(as.vector(
      rList$meta$sids[1]
    ))))
  #dfMeta  <- cbind(dfMeta, as.data.frame(as.character(as.vector(dfMetaInit[4, ]))))
  colnames(dfMeta)[5]  <- "sid1"
  dfMeta$sid1  <- as.character(dfMeta$sid1)
  sid1_type <-
    suppressWarnings(getStationSubtype(unlist(strsplit(
      unlist(dfMeta$sid1), " "
    ))[2], substr(unlist(
      strsplit(unlist(dfMeta$sid1), " ")
    )[1], 1, 3)))
  dfMeta  <-
    cbind(dfMeta, as.data.frame(as.character(as.vector(sid1_type))))
  colnames(dfMeta)[6]  <- "sid1_type"
  # Check if SIDS 3 is present (dim 9,1 or dim 10,1 - 4th SID is ignored)
  if (identical(dim(dfMetaInit), as.integer(c(9, 1))) || identical(dim(dfMetaInit), as.integer(c(10, 1)))) {
    dfMeta  <-
      cbind(dfMeta, as.data.frame(as.character(as.vector(
        dfMetaInit[5,]
      ))))
    colnames(dfMeta)[7]  <- "sid2"
    dfMeta$sid2  <- as.character(dfMeta$sid2)
    sid2_type <-
      suppressWarnings(getStationSubtype(unlist(strsplit(
        unlist(dfMeta$sid2), " "
      ))[2], substr(unlist(
        strsplit(unlist(dfMeta$sid2), " ")
      )[1], 1, 3)))
    dfMeta  <-
      cbind(dfMeta, as.data.frame(as.character(as.vector(sid2_type))))
    colnames(dfMeta)[8]  <- "sid2_type"
    dfMeta  <-
      cbind(dfMeta, as.data.frame(as.character(as.vector(
        dfMetaInit[6,]
      ))))
    colnames(dfMeta)[9]  <- "sid3"
    dfMeta$sid3  <- as.character(dfMeta$sid3)
    sid3_type <-
      suppressWarnings(getStationSubtype(unlist(strsplit(
        unlist(dfMeta$sid3), " "
      ))[2], substr(unlist(
        strsplit(unlist(dfMeta$sid3), " ")
      )[1], 1, 3)))
    dfMeta  <-
      cbind(dfMeta, as.data.frame(as.character(as.vector(sid3_type))))
    colnames(dfMeta)[10]  <- "sid3_type"
  }
  else {
    # missing one or more sid elements
    if (identical(dim(dfMetaInit), as.integer(c(8, 1)))) {
      dfMeta  <-
        cbind(dfMeta, as.data.frame(as.character(as.vector(
          dfMetaInit[4,]
          #cbind(dfMeta, as.data.frame(as.character(as.vector(
          #dfMetaInit[5,]
        ))))
      colnames(dfMeta)[7]  <- "sid2"
      dfMeta$sid2  <- as.character(dfMeta$sid2)
      sid2_type <-
        suppressWarnings(getStationSubtype(unlist(strsplit(
          unlist(dfMeta$sid2), " "
        ))[2], substr(unlist(
          strsplit(unlist(dfMeta$sid2), " ")
        )[1], 1, 3)))
      dfMeta  <-
        cbind(dfMeta, as.data.frame(as.character(as.vector(
          sid2_type
        ))))
      colnames(dfMeta)[8]  <- "sid2_type"
    }
    else {
      # no sid2 value
      dfMeta  <- cbind(dfMeta, as.data.frame(NA))
      dfMeta[7] <- setNames(dfMeta[7],"sid2")
      colnames(dfMeta)[7]  <- "sid2"
      sid2_type <-  as.data.frame(NA)
      #dfMeta  <- cbind(dfMeta, as.character(sid2_type))
      dfMeta  <-
        cbind(dfMeta, as.data.frame(as.character(as.vector(
          sid2_type
        ))))
      colnames(dfMeta)[8]  <- "sid2_type"
    } # no sid3 value
    dfMeta  <- cbind(dfMeta, as.data.frame(NA))
    colnames(dfMeta)[9]  <- "sid3"
    #dfMeta$sid3  <- as.character(dfMeta$sid3)
    sid3_type <-  as.data.frame(NA)
    dfMeta  <-
      cbind(dfMeta, as.data.frame(as.character(as.vector(sid3_type))))
    colnames(dfMeta)[10]  <- "sid3_type"
  }
  
  if (!is.null(strsplit(dfMetaInit[, 1], " ")$state)) {
    dfMeta  <-
      cbind(dfMeta, as.data.frame(as.character(as.vector(
        strsplit(dfMetaInit[, 1], " ")$state
      ))))
  }
  else {
    dfMeta  <-
      cbind(dfMeta, as.data.frame(NA))
  }
  colnames(dfMeta)[11]  <- "state"
  
  if (!is.null(strsplit(dfMetaInit[, 1], " ")$elev)) {
    dfMeta  <-
      cbind(dfMeta, as.data.frame(as.numeric(as.vector(
        strsplit(dfMetaInit[, 1], " ")$elev
      ))))
  }
  else {
    dfMeta  <-
      cbind(dfMeta, as.data.frame(NA))
  }
  colnames(dfMeta)[12]  <- "elev"
  df$elev <- as.numeric(df$elev)
  
  # For whatever reason, this conversion has to be re-forced again!
  dfMeta$uid <- as.numeric(as.character(dfMeta$uid))
  options(digits = 1)
  dfMeta$elev <- as.numeric(as.character(dfMeta$elev))
  options(digits = 7)
  df <- cbind(dfMeta, dfDate)
  
  # Add the paramter vectors - thanks for the matrix suggestion, Tom!!
  # For monthly data, value vector returned as character to accommodate missing records ("M")
  # Get parameter units from lookup file
  # rangeBase subtraction forces ignoring of first 'column' which is date
  rangeBase <- length(rList$data[[1]]) - 1
  #if(duration == 'dly') {range <- rangeBase - 1}
  #else {range <- rangeBase}
  print(rangeBase)
  itemCount <- 1
  #for (i in 2:(length(rList$data[[1]])) - 1)  {
  for (i in 1:rangeBase)  {  
    #  == count of parameters
    vUnit <-
      luElements[which(luElements$code == climateParameters[i]),]$unitabbr
    
    if(duration == 'dly') {
      vName <- paste(climateParameters[i], vUnit, sep = "_")
      fName <- paste(climateParameters[i], "acis_flag", sep = "_")
      valueArray <-
        matrix(unlist(lapply(rList$data, "[", i + 1)), ncol = 3, byrow = TRUE)[, 1]
      flagArray <-
        matrix(unlist(lapply(rList$data, "[", i + 1)), ncol = 3, byrow = TRUE)[, 2]
      sName <-
        paste(climateParameters[i], "source_flag", sep = "_")
      sourceFlagArray <-
        matrix(unlist(lapply(rList$data, "[", i + 1)), ncol = 3, byrow = TRUE)[, 3]
      df[[vName]] <- as.numeric(valueArray)
      df[[fName]] <-
        as.character(replace(flagArray, flagArray == " ", NA))
      df[[sName]] <-
        as.character(replace(sourceFlagArray, sourceFlagArray == " ", NA))
    }
    else { 
      for (j in 1:length(reduceCodes)) {
        vReduce <- unlist(reduceCodes[j])
        vName <- paste(paste(climateParameters[i], vUnit, sep = "_"), vReduce, sep = "_")
        fName <- paste(vName, "countMissing", sep = "_")
        #valueArray <-
        #  matrix(unlist(lapply(rList$data, "[", i + 1)), ncol = 2, byrow = TRUE)[, 1]
        #if (itemCount<=(rangeBase-1)) {
        if (itemCount<=rangeBase) {
          valueArray <-
            matrix(unlist(lapply(rList$data, "[", itemCount + 1)), ncol = 2, byrow = TRUE)[, 1]
          flagArray <-
            matrix(unlist(lapply(rList$data, "[", itemCount + 1)), ncol = 2, byrow = TRUE)[, 2]
          print(vName)
          print(valueArray)
          # For monthly data, value vector returned as character to accommodate missing records ("M")
          df[[vName]] <- valueArray#as.numeric(valueArray)
          df[[fName]] <-
            as.character(replace(flagArray, flagArray == " ", NA))
          itemCount <- itemCount + 1
        }
      }
    }
  }
  
  # Convert factors and booleans to character vectors
  fc  <- sapply(df, is.factor)
  lc <- sapply(df, is.logical)
  df[, fc]  <- sapply(df[, fc], as.character)
  df[, lc]  <- sapply(df[, lc], as.character)
  
  # Create output object
  if (is.data.frame(dfResponse)) {
    dfResponse <- rbind(dfResponse, df)
  }
  else {
    dfResponse <- df
  }
  return(dfResponse)
}

#' stripEscapes strips escape characters from input string
#' @param inputStr input from which escape characters are to be stripped
#' @export
#'

stripEscapes <- function(inputStr) {
  # Yes, this is crappy code but it works
  # TODO: Clean this up!!!
  iJSON <- gsub("\\\\", "T", toJSON(inputStr, auto_unbox = TRUE))
  f = gsub("\"\\[", "\\[", iJSON)
  g = gsub("\\]\"", "\\]", f)
  h = gsub("T", "", g)
  i = gsub("\"\"\\{", "\\{", h)
  outputJSON <- gsub("\\}\"\"", "\\}", i)
  
  return(outputJSON)
}

#' stripEscapesGrid strips escape characters from input string (used to format getDailyGrids response)
#' @param inputStr input from which escape characters are to be stripped
#' @export
#'

stripEscapesGrid <- function(inputStr) {
  # Yes, this is crappy code but it works
  # TODO: Clean this up!!!
  dd1  <- gsub("\"\\[", "\\[", inputStr)
  dd2  <- gsub("\\\\", "T", dd1)
  dd3  <- gsub("Tn", "", dd2)
  outputJSON  <- gsub("T", "", dd3)
  
  return(outputJSON)
}

#' getBBox retrieves bounding box from IRMA/ServCat Unit service and buffers it by specified distance
#' @param unitCode unitCode One NPS or FWS unit code as a string
#' @param bboxExpand buffer distance in decimal degrees (assumes WGS984)
#' @export
#'
getBBox <- function (unitCode, expandBBox) {
  # NPS codes are alphabetic; FWS codes are alphanumeric
  if (grepl('^[A-Za-z]+$', unitCode) == TRUE) {
    bboxURLBase <-
      "http://irmaservices.nps.gov/v2/rest/unit/CODE/geography?detail=envelope&dataformat=wkt&format=json"
  }
  else {
    bboxURLBase <-
      "https://ecos.fws.gov/ServCatServices/v2/rest/unit/CODE/geography?detail=envelope&dataformat=wkt&format=json"
  }
  config <- add_headers(Accept = "'Accept':'application/json'")
  # Get bounding box for park(s)
  bboxURL <- gsub("CODE", unitCode, bboxURLBase)
  # Counter-clockwise vertices (as WKT): LL, LR, UR, UL
  bboxWKT <-
    strsplit(content(GET(bboxURL, config))[[1]]$Geography, ",")
  # Extract vertices and 'buffer' by bboxExpand distance or default of 0.011 degrees (~33 km)
  # TODO: add Eastern Hemisphere detection
  LL <- strsplit(substring(bboxWKT[[1]][1], 11), " ")
  LR <- strsplit(substring(bboxWKT[[1]][2], 2), " ")
  UR  <- strsplit(substring(bboxWKT[[1]][3], 2), " ")
  UL  <-
    strsplit(gsub("))", "", substring(bboxWKT[[1]][4], 2)), " ")
  
  LLX  <- as.numeric(LL[[1]][1]) - expandBBox
  LLY  <- as.numeric(LL[[1]][2]) - expandBBox
  LRX  <- as.numeric(LR[[1]][1]) + expandBBox
  LRY  <- as.numeric(LR[[1]][2]) - expandBBox
  URX  <- as.numeric(UR[[1]][1]) + expandBBox
  URY  <- as.numeric(UR[[1]][2]) + expandBBox
  ULX  <-  as.numeric(UL[[1]][1]) - expandBBox
  ULY  <- as.numeric(UL[[1]][2]) + expandBBox
  
  bbox  <- paste(c(LLX, LLY, URX, URY), collapse = ", ")
  return(bbox)
}

#' outputAscii formats grid(s) as ASCII (*.asc) with headers and projection (*.prj)
#' @param gridResponse grid (dataframe format) returned from ACIS request (by date)
#' @param filePath full file path for ASCII output
#' @param lonCen longitude of lower left grid cell
#' @param lonCen latitude of lower left grid cell
#' @param luSource ACIS lookup source (as dataframe)
#' @export
#'
outputAscii <-
  function(gridResponse,
           fullFilePath,
           lonCen,
           latCen,
           luSource) {
    #xcen <- (as.numeric(unlist(strsplit(bbox, ","))[3]) - as.numeric(unlist(strsplit(bbox, ","))[1])) / 2 + as.numeric(unlist(strsplit(bbox, ","))[3])
    #ycen <- (as.numeric(unlist(strsplit(bbox, ","))[4]) - as.numeric(unlist(strsplit(bbox, ","))[2])) / 2 + as.numeric(unlist(strsplit(bbox, ","))[2])
    write(paste("ncols ", length(gridResponse[1, ])), fullFilePath)
    write(paste("nrows ", length(gridResponse[, 1])), fullFilePath, append =
            TRUE)
    write(paste("xllcenter ", lonCen), fullFilePath, append = TRUE)
    write(paste("yllcenter ", latCen), fullFilePath, append = TRUE)
    #write(paste("xllcorner ", unlist(strsplit(bbox, ","))[1]), fullFilePath, append=TRUE)
    #write(paste("yllcorner ", unlist(strsplit(bbox, ","))[2]), fullFilePath, append=TRUE)
    write(paste("cellsize ", luSource$cellSize), fullFilePath, append = TRUE)
    write(paste("NODATA_value ", luSource$missingValue),
          fullFilePath,
          append = TRUE)
    write.table(
      gridResponse,
      fullFilePath,
      row.names = FALSE,
      col.names = FALSE,
      append = TRUE
    )
    write(luSource$projection, gsub(".asc", ".prj", fullFilePath))
    return("Success")
  }

