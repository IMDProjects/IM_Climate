import json

class StationList(list):
    def __init__(self, *args, **kwargs):
        super(StationList, self).__init__(*args, **kwargs)

    @property
    def stationIDs(self):
        '''
        Returns a list of all station IDs
        '''
        data = [z['sids'][0] for z in self]
        return data


if __name__ == '__main__':
    stations =  [{u'elev': 10549.9,
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
            u'uid': 77459}]
    s = StationList(stations)
    print s.stationIDs