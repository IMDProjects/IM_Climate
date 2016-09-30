#' Utility functions for IMClimateR
#' 
#' getStationType function uses the station identifier type code to lookup the station type description
#' @param testType station identifier type code
#' @param testSid first three characters of the station identifier
#' @export 
#' 

getStationSubtype <- function(testType, testSid) {
  # ACIS lookup
  acisLookup <- fromJSON("ACISLookups.json") # assumes placement in package R subfolder
  # acisLookup <- fromJSON("..//ACISLookups.json")
  typeDesc <- acisLookup$stationIdType$description[acisLookup$stationIdType$code == testType]
  subtypeDesc <- NULL
  # If subtypes exist for station type, find matching subtype
  if (!is.na(testType)) {
    if (!acisLookup$stationIdType$subtypes[acisLookup$stationIdType$code == testType] == "") {
      subtypes <- unlist(acisLookup$stationIdType$subtypes[acisLookup$stationIdType$code == testType])
      if(!length(subtypes) == 0 && !subtypes == "") {
        if (!is.na(names(strsplit(unlist(acisLookup$stationIdType$subtypes[acisLookup$stationIdType$code == testType])[testSid], '\n')[testSid]))) {
        tempdf <- as.data.frame(strsplit(unlist(acisLookup$stationIdType$subtypes[acisLookup$stationIdType$code == testType])[testSid], '\n')[testSid])
        typeDesc <- as.character(as.vector(tempdf[1,]))
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

#' stripEscapesGird strips escape characters from input string (used to format getDailyGrids response)
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

#' outputAscii formats grid(s) as ASCII (*.asc) with headers and projection (*.prj)
#' @param gridResponse grid (dataframe format) returned from ACIS request
#' @param filePath full file path for ASCII output
#' @param bbox bounding box for grid request
#' @param luSource ACIS lookup source (as dataframe)
#' @export 
#'
outputAscii <- function(gridResponse, fullFilePath, bbox, luSource) {
  write(paste("ncols ", length(gridResponse[1,])), fullFilePath)
  write(paste("nrows ", length(gridResponse[,1])), fullFilePath, append=TRUE)
  write(paste("xllcorner ", unlist(strsplit(bbox, ","))[1]), fullFilePath, append=TRUE)
  write(paste("yllcorner ", unlist(strsplit(bbox, ","))[2]), fullFilePath, append=TRUE)
  write(paste("cellsize ", luSource$cellSize), fullFilePath, append=TRUE)
  write(paste("NODATA_value ", luSource$missingValue), fullFilePath, append=TRUE)
  write.table(gridResponse, fullFilePath, row.names = FALSE, col.names = FALSE, append = TRUE)
  write(luSource$projection, gsub(".asc", ".prj", fullFilePath))
  return("Success")
}
