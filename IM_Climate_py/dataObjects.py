import json
import csv
from datetime import date


class dataObjects(object):

    '''
    Base class for all data objects
    '''

    def __init__(self):
        self.dateRequested = date.today().isoformat()

    def _writeToCSV(self):
        '''
        INFO
        ----
        Writes a 2-dimensional list to a CSV text file
        Comma-delimits values.

        ARGUMENTS
        ---------
        filePathAndName - file name and path
        dataAsList - 2-dimensional list

        RETURNS
        -------
        None

        '''
        with open(self._filePathAndName,'w') as csvFile:
            writer = csv.writer(csvFile, lineterminator='\n' )
            writer.writerows(self._dataAsList)
        csvFile.close()


    def export(self, filePathAndName, format='csv'):
        '''
        INFO
        ----
        Method providing option to export data into various formats

        ARGUMENTS
        ---------
        filePathAndName - Destination where file is to be saved
        format  = Export format. Default = csv


        RETURNS
        --------
        None
        '''
        self._filePathAndName = filePathAndName
        if format == 'csv':
            self._dumpToList()
            self._writeToCSV()






if __name__=='__main__':
    data = {'meta':{},'data':[]}
    queryParams = {'sids':[1,2,3]}
    d = dataObjects(data  = data, queryParams = queryParams)
    ##d._addStandardMetadataElements()
    ##d._addMetadata(elk = 5)
    ##print(d.metadata)
    ##print (d.keys())
    ##print d.metadata
    print d
