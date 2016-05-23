#' Get station data for specified parameter(s) and station(s)
#' 
#' Takes a list of one or more parameters and one or more stations, requests station data, and returns it as a JSON object
#' @param climateParams A list of one or more climate parameters (tmin, tmax, tavg, prcp)
#' @param climateStations A list of one or more climate stations
#' @return A JSON object containing the requested data
#' @export
#' 