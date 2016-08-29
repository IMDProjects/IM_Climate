
### plot daily data retruned from ACIS


###### Interactive (HTML)plot: plots single  parmeter over time period at station level ######

SeriesByStationInt<-function(data, station, parm) {
  require(dygraphs)
  library(reshape)
  library(zoo)
  library(xts)
  
  ## extract data by site
  
  data<-data[data$uid %in% station,]
  data<-droplevels(data)
  
  # create ts object
  data.raw<-data[c("pcpn","avgt","mint","maxt")]
  time.raw <- as.POSIXct(data$date, format = "%Y-%m-%d")
  series.raw<-xts(data.raw, order.by= time.raw)
  #plot.zoo(series.raw)
  #str(series.raw)
  
  ##### Create dynamic plot
  # raw data points
  
  if(parm == "pcpn"){
    y<- dygraph(series.raw$pcpn, main = data$name[1], xlab= "Date", ylab= "Precipitation (in.)")%>%
      dyRangeSelector()%>%
      dyOptions(drawPoints = TRUE, connectSeparatedPoints = FALSE, pointSize = 2)%>%
      dySeries("pcpn", label = "Precipitation (in.)")%>%
      dyLegend(show = "onmouseover", labelsSeparateLines = T)
    print(y)
  }
  if(parm == "avgt"){
    y<- dygraph(series.raw$avgt, main = data$name[1], xlab= "Date", ylab= "Average Temperature (F)")%>%
      dyRangeSelector()%>%
      dyOptions(drawPoints = TRUE, connectSeparatedPoints = FALSE, pointSize = 2)%>%
      dySeries("avgt", label = "Average Temperature (F)")%>%
      dyLegend(show = "onmouseover", labelsSeparateLines = T)
    print(y)
  }
  if(parm == "mint"){
    y<-dygraph(series.raw$mint, main = data$name[1], xlab= "Date", ylab= "Minimum Temperature (F)")%>%
      dyRangeSelector()%>%
      dyOptions(drawPoints = TRUE, connectSeparatedPoints = FALSE, pointSize = 2)%>%
      dySeries("mint", label = "Minimum Temperature (F)")%>%
      dyLegend(show = "onmouseover", labelsSeparateLines = T)
    print(y)
  }
  
  if(parm == "maxt"){
    y<- dygraph(series.raw$pH, main = data$name[1], xlab= "Date", ylab= "Maximum Temperature (F)")%>%
      dyRangeSelector()%>%
      dyOptions(drawPoints = TRUE, connectSeparatedPoints = FALSE, pointSize = 2)%>%
      dySeries("maxt", label = "Maximum Temperature (F)")%>%
      dyLegend(show = "onmouseover", labelsSeparateLines = T)
    print(y)
    
  }
}