import json
from datetime import date



class dataObjects(dict):

    '''
    Base class for all dictionary typed data objects
    '''
    def __init__(self, data, queryParams, *args,**kwargs):
        super(dataObjects,self).__init__(data)
        kwargs['queryParams'] = queryParams
        self._addMetadata(**kwargs)

    def toJSON(self):
        return json.dumps(self)

    def _addStandardMetadataElements(self):
        self._addMetadata(dateCreated = date.today().isoformat())

    @property
    def metadata(self):
        return self['meta']

    @property
    def dateCreated(self):
        '''returns the date the object was created
        '''
        return self['meta']['dateCreated']

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
    print(d.dateCreated)
    print (d.keys())
