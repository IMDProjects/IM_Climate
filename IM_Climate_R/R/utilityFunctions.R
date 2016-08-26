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