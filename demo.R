library(IMClimateR)

# ACIS Data Service Docs: http://www.rcc-acis.org/docs_webservices.html

findStation("MABI", list('pcpn'))
dataRequest(list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), 25056, "20150801", "20150831")
dataRequest(list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), 17611, "20150801", "20150831")