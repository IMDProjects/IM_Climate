from IM_Climate_py.StationFinder import StationFinder

localFolder = 'c:\\temp\\'
sf = StationFinder()

#Case #1: All stations around NOCA
data = sf.findStation(unitCode = 'NOCA')
data.export(localFolder + 'NOCA_Stations.txt')

#Case #2: All stations around NOCA recording minimum temperature
data = sf.findStation(unitCode = 'NOCA', parameter = 'mint')
data.export(localFolder + 'minT_Stations.txt')



