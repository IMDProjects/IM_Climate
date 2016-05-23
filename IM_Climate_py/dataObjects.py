import json
import csv
from datetime import date



class dataObjects(dict):

    '''
    Base class for all dictionary typed data objects
    '''
    def __init__(self, data = None, *args,**kwargs):
        if data:
            super(dataObjects,self).__init__(data)
        if not self.get('meta'):
            self['meta'] = {}
        if not self.get('data'):
            self['data'] = {}


        #Hidden properties
        self._tags = []  #common tag elements associated with object

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
            self._toText()
            self._writeToCSV()


##    def _addStandardMetadataElements(self):
##        self._addMetadata(dateRequested = date.today().isoformat())
##
##    @property
##    def metadata(self):
##        return self['meta']
##
##
##    def _addMetadata(self, **kwargs):
##        for i in kwargs.items():
##            self['meta'][i[0]] = i[1]
##
##    def _parseDate(self, d):
##        if d:
##            d = d.split('-')
##            d = list(map(int,d))
##            return date(d[0], d[1], d[2])



if __name__=='__main__':
    data = {'meta':{},'data':[]}
    queryParams = {'sids':[1,2,3]}
    d = dataObjects(data  = data, queryParams = queryParams)
    ##d._addStandardMetadataElements()
    ##d._addMetadata(elk = 5)
    ##print(d.metadata)
    print (d.keys())
