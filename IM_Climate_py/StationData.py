from ParameterSeries import ParameterSeries

class StationData(dict):
    '''
    Dictionary(-like) object containing all climate parameter data (i.e., one or more
    parameter series) for a specific station.
    Station Data is indexable by weather parameter and has been extended to iterate
    over all parameters like a list
    '''
    def __init__(self, stationData, climateParameters):
        self.observationDates = tuple([d[0] for d in stationData])
        for index, p in enumerate(climateParameters):
            self[p] = ParameterSeries(([d[index+1] for d in stationData]), dates = self.observationDates, parameter = p)
    @property
    def climateParameters(self):
        return self.keys()

    def __iter__(self):
        '''
        Allow iteration over StationData (like a list)
        '''
        for param in self.keys():
            yield self[param]

if __name__ == '__main__':

    ############################################################################
    ############################################################################
    #StationData
    data = [[u'2012-01-01', [u'21.5', u' ', u'U'], [u'5', u' ', u'U']],
         [u'2012-01-02', [u'29.5', u' ', u'U'], [u'12', u' ', u'U']],
         [u'2012-01-03', [u'32.0', u' ', u'U'], [u'19', u' ', u'U']],
         [u'2012-01-04', [u'27.5', u' ', u'U'], [u'12', u' ', u'U']],
         [u'2012-01-05', [u'35.5', u' ', u'U'], [u'18', u' ', u'U']]]
    parameters = ['maxt', 'mint']
    sd = StationData(data,parameters)
    print sd
