% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/DataRequest.R
\name{getDailyWxObservations}
\alias{getDailyWxObservations}
\title{Get station data for specified parameter(s) and station(s)}
\usage{
getDailyWxObservations(climateParameters = NULL, climateStations,
  sdate = "por", edate = "por", filePathAndName = NULL)
}
\arguments{
\item{climateParameters}{A list of one or more climate parameters (e.g. pcpn, mint, maxt, avgt, obst, snow, snwd).  If not specified, defaults to all parameters except degree days. See Table 3 on ACIS Web Services page: http://www.rcc-acis.org/docs_webservices.html}

\item{climateStations}{A list of one or more unique identifiers (uid) for climate stations. Can be a single item, a list of items, or a data frame of the findStation response.}

\item{sdate}{(optional) Default is period of record ("por"). If specific start date is desired, format as a string (yyyy-mm-dd or yyyymmdd). The beginning of the desired date range.}

\item{edate}{(optional) Default is period of record ("por"). IF specific end date is desired, format as a string (yyyy-mm-dd or yyyymmdd). The end of the desired date range.}

\item{filePathAndName}{(optional) File path and name including extension for output CSV file}
}
\value{
A data frame containing the requested data. See User Guide for more details: https://docs.google.com/document/d/1B0rf0VTEXQNWGW9fqg2LRr6cHR20VQhFRy7PU_BfOeA/
}
\description{
Takes a list of one or more parameters and one or more unique station IDs, requests station data, and returns it as a data frame
}
\examples{
\dontrun{
Precipitation, temperature weather observations for one station for a specifc date range:

getDailyWxObservations(climateParameters=list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), climateStations=25056, sdate="20150801", edate="20150831")

All weather observations for a station for its period of record

getDailyWxObservations(climateStations=60903)

All weather observations for all stations (using a findStation response data frame: stationDF) for a specific date range:

getDailyWxObservations(climateParameters=list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), climateStations=stationDF, sdate="20150801", edate="20150803")
}
}

