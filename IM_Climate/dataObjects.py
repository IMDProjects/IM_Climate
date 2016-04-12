import json
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


    def toJSON(self):
        return json.dumps(self)

    def _addStandardMetadataElements(self):
        self._addMetadata(dateRequested = date.today().isoformat())

    @property
    def metadata(self):
        return self['meta']

    def toCSV(self, fileNameAndPath):
        self.outFile = open(fileNameAndPath,'w')
        self._sp = ', '

    def toGeoJSON(self):
        pass

    def _addMetadata(self, **kwargs):
        for i in kwargs.items():
            self['meta'][i[0]] = i[1]

    def _parseDate(self, d):
        if d:
            d = d.split('-')
            d = list(map(int,d))
            return date(d[0], d[1], d[2])

if __name__=='__main__':
    data = {'meta':{},'data':[]}
    queryParams = {'sids':[1,2,3]}
    d = dataObjects(data  = data, queryParams = queryParams)
    d._addStandardMetadataElements()
    d._addMetadata(elk = 5)
    print(d.metadata)
    print (d.keys())
