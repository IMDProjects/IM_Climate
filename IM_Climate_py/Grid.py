import numpy as np
import os
import csv

class Grid(np.ndarray):
    def __new__(cls, grid, *args, **kwargs):
        '''
        This is the method used to inherit the ndarrary object
        '''
        obj = np.asarray(grid).view(cls)
        return obj

    def __init__(self, grid, XLLCenter, YLLCenter, cellSize, projection, missingValue):
        self.nrows = len(self)
        self.ncols = len(self[0])
        self.XLLCenter = XLLCenter # X dimension lower left center
        self.YLLCenter = YLLCenter # Y dimension lower left center
        self.cellSize = cellSize
        self.missingValue = missingValue
        self.projection = projection

    def export(self, filePathAndName):
        '''
        Export grid to ASCII grid format along with PRJ file


        NOTE: Currently this method is specific to PRISM data and the ability to represent
        missing values as -999. This should be modified as new data sources are added
        '''
        #Write the header information at the top of the file
        outfile = open(filePathAndName,'wb')
        outfile.write ('ncols  ' + str(self.ncols) + '\n')
        outfile.write ('nrows  ' + str(self.nrows) + '\n')
        outfile.write ('xllcenter  ' + str(self.XLLCenter) + '\n')
        outfile.write ('yllcenter  ' + str(self.YLLCenter) + '\n')
        outfile.write ('cellsize  ' + repr(self.cellSize) + '\n') #repr preserves the precision
        outfile.write ('NODATA_value  ' + str(self.missingValue) + '\n')

        #create csv file and iterate through rows of grid
        #Because ndarray manages -999 as a decimal, also convert that to the
        #the original -999 representation
        #NOTE: REPLACEMENT OF -999 IS SPECIFIC TO PRISM GRIDS!!
        r = csv.writer(outfile, delimiter = ' ', lineterminator='\n')
        for row in reversed(self):
            row = list(row) #convert to a list from a np.array
            row = map(lambda x: '-999' if x == -999.0 else str(x), row)
            r.writerow(row)
        outfile.close()

        #Create PRJ projection file
        prjFile = os.path.splitext(filePathAndName)[0] + '.prj'
        outfile = open(prjFile,'w')
        outfile.write(str(self.projection))
        outfile.close()

if __name__ == '__main__':
    grid = [[1.5, 2.3, 3.7, 4.12], [5.0, 6.3, 7.7,8.1], [-999.0, 10, 11, 12]]
    XLLCenter = -130
    YLLCenter = 40
    cellSize = 4
    missingValue = -999
    projection = 'NAD83'
    g = Grid(grid = grid, XLLCenter = XLLCenter, YLLCenter = YLLCenter
        , cellSize = cellSize, projection = projection, missingValue = missingValue)
    g.export('aaa.asc')
    print (g.ncols)
    print (g.nrows)
    print (g)