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
    fromJSON("ACISLookups.json") # assumes placement in package R subfolder
  # acisLookup <- fromJSON("..//ACISLookups.json")
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

#' getBBox retrieves bounding box from IRMA Unit service and buffers it by specified distance
#' @param unitCode unitCode One NPS unit code as a string
#' @param bboxExpand buffer distance in decimal degrees (assumes WGS984)
#' @export
#'
getBBox <- function (unitCode, expandBBox) {
  bboxURLBase <-
    "http://irmaservices.nps.gov/v2/rest/unit/CODE/geography?detail=envelope&dataformat=wkt&format=json"
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
  UL  <- strsplit(gsub("))", "", substring(bboxWKT[[1]][4], 2)), " ")
  
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
#' @param gridResponse grid (dataframe format) returned from ACIS request
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
