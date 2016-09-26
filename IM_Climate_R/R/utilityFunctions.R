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
  
  # if (exists("subtypeDesc")) {
  #   if (length(subtypeDesc) > 0) {return (subtypeDesc)}
  # }
  # else if (exists("typeDesc")) {
  #   if (length(typeDesc) > 0) {return (typeDesc)}
  # }
  # else {return (NA)}
  
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

#' outputAscii formats grid(s) as ASCII (*.asc) with headers and projection (*.prj)
# @param gridResponse grid (PNG-format) returned from ACIS request
#' @export 
#'
outputAscii <- function(gridResponse) {
  
}