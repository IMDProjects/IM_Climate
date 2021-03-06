% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/DataRequestMonthly.R
\name{getMonthlyWxObservations}
\alias{getMonthlyWxObservations}
\title{Get station data for specified parameter(s) and station(s)}
\usage{
getMonthlyWxObservations(climateStations, climateParameters = NULL,
  reduceCodes = NULL, sdate = "por", edate = "por", maxMissing = NULL,
  filePathAndName = NULL)
}
\arguments{
\item{climateStations}{A list of one or more unique identifiers (uid) for climate stations. Can be a single item, a list of items, or a data frame of the findStation response.}

\item{climateParameters}{A list of one or more climate parameters (e.g. pcpn, mint, maxt, avgt, obst, snow, snwd).  If not specified, defaults to all parameters except degree days. See Table 3 on ACIS Web Services page: http://www.rcc-acis.org/docs_webservices.html}

\item{reduceCodes}{(optional) A list of one or more reduce codes. If missing, defaults to min, max, sum, and mean.}

\item{sdate}{(optional) Default is period of record ("por"). If specific start date is desired, format as a string (yyyy-mm-dd or yyyymmdd). The beginning of the desired date range.}

\item{edate}{(optional) Default is period of record ("por"). IF specific end date is desired, format as a string (yyyy-mm-dd or yyyymmdd). The end of the desired date range.}

\item{maxMissing}{(optional) Maximum number of missing days within a month before the aggregate is not calculated (applied to each parameter). If missing, defaults to 1 (~3.3 percent missing days/month).}

\item{filePathAndName}{(optional) File path and name including extension for output CSV file}
}
\value{
A data frame containing the requested data. Note: date vector is in character format, not date format. See User Guide for more details: https://docs.google.com/document/d/1B0rf0VTEXQNWGW9fqg2LRr6cHR20VQhFRy7PU_BfOeA/
}
\description{
Takes a list of one or more parameters and one or more unique station IDs, requests station data, and returns it as a data frame. Note: For monthly data, value vectors returned as character format to accommodate missing records ("M")
}
\examples{
\dontrun{
Precipitation, temperature weather observations for one station for a specifc date range:

getMonthlyWxObservations(climateParameters=list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), climateStations=25056, sdate="20150801", edate="20150831")

The same request written to a CSV file:

getMonthlyWxObservations(climateParameters=list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), climateStations=25056, sdate="20150801", edate="20160831", filePathAndName = "D:\\\\temp\\\\trash\\\\monthyObs_station25056.csv")
 
All weather observations for a station for its period of record

getMonthlyWxObservations(climateStations=60903)

All weather observations for two stations for a specified date range:

getMonthlyWxObservations(climateStations = list(61193, 26215), sdate="201401", edate = "201501", maxMissing = NULL)

Weather observations for minimum precipitation for a station from beginning of record through Sept 2016

getMonthlyWxObservations(climateStations = list(26215), climateParameters = list('pcpn'), reduceCodes = list('min'), edate= "2016-09", maxMissing = 2)

All weather observations for all stations (using a findStation response data frame: stationDF) for a specific date range:

getMonthlyWxObservations(climateParameters=list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), climateStations=stationDF, sdate="20150801", edate="20150803")
}
}

