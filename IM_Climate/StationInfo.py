import json
try:
    #python 2.x
    from dataObjects import dataObjects
except:
    #python 3.x
    from .dataObjects import dataObjects

class StationInfo(dataObjects):
    def __init__(self, info, *args, **kwargs):
        info['data'] = info['meta'] #swap keys
        info['meta'] = {} #clear out the existing meta key
        super(StationInfo, self).__init__(info, **kwargs)
        self._addStandardMetadataElements()

    @property
    def stationIDs(self):
        '''
        Returns a list of all station IDs
        '''
        return [str(z['sids'][0]) for z in self['data']]

    @property
    def stationNames(self):
        '''
        Returns a list of all station IDs
        '''
        return [str(z['name']) for z in self['data']]

    def dropStation(self, stationID):
        '''
        Removes specified station from self
        '''
        for e in self['data']:
            sids = e['sids']
            for s in sids:
                if s.find(stationID) >= 0:
                    self['data'].remove(e)

    def match(self, stationNames):
        '''Matches provided station names to full list of stations. Matching is
            done using wildcard around provided stationName.
            Returns list of matched station names'''
        if type(stationNames) == str:
            stationNames = [stationNames]
        matches = []
        for sn in stationNames:
            for es in self.stationNames:
                if es.lower().find(sn.lower()) >= 0:
                    matches.append(es)
                    break
        return matches

if __name__ == '__main__':
    stations =  {u'meta': [{u'elev': 10549.9,
            u'll': [-106.17, 39.49],
            u'name': u'Copper Mountain',
            u'sids': [u'USS0006K24S 6'],
            u'state': u'CO',
            u'uid': 67175},
           {u'elev': 10520.0,
            u'll': [-106.42, 39.86],
            u'name': u'Elliot Ridge',
            u'sids': [u'USS0006K29S 6'],
            u'state': u'CO',
            u'uid': 77459}]}
    queryParams = {'sids':'USS0006K29S 6'}
    s = StationInfo(stations, queryParams = queryParams)
    print(s.stationIDs)
    print(s.stationNames)
    print(s.toJSON())
    print(s.metadata)
    print s.match(stationNames = ['ell','cop'])
    s.dropStation(stationID = 'USS0006K24S 6')
    print s.stationNames


