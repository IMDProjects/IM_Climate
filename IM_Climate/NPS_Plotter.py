import Tkinter as Tk
import ttk
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import GUI.NPS_root as rt


class NPS_Plotter(object):
    '''
    Creates stand-alone graph widget with numerous controls
    '''
    def __init__(self, xAxis, yData, Title = 'Title'
                 ,xLabel = 'X Label', yLabel = 'Y Label', plotType = 'line', **kwargs):
        super(NPS_Plotter, self).__init__(**kwargs)

        self.xAxis = xAxis
        self.yData = yData
        self.plotType = plotType

        self.root=rt.NPS_root()
        #To instantiate StrinVar and IntVar classes, Tk() must already be instantiated
        self.Title = Tk.StringVar()
        self.xMax = Tk.IntVar()
        self.xMin = Tk.IntVar()
        self.yMax = Tk.IntVar()
        self.yMin = Tk.IntVar()
        self.xLabel = Tk.StringVar()
        self.yLabel = Tk.StringVar()
        self.xTicLabel = Tk.StringVar()

        self.yMax.set(max(y for y in self.yData if y is not None))
        self.yMin.set(min(y for y in self.yData if y is not None))

        self.falseX = [x for x in range(0, len(self.xAxis))]
##        self.xMax.set(max(x for x in self.xAxis if x is not None))
##        self.xMin.set(min(x for x in self.xAxis if x is not None))
        self.xMax.set(max(x for x in self.falseX if x is not None))
        self.xMin.set(min(x for x in self.falseX if x is not None))
        self.xLabel.set(xLabel)
        self.yLabel.set(yLabel)
        self.xTicLabel.set( ('aa','ba', 'c', 'd', 'e'))
        #self.xTicLabel.set(map(str, xAxis))
        self.Title.set(Title)
        self.app()


    def app(self):
        self.add_graph_controls_frame()
        self.drawGraph()
        self.root.mainloop()


    def drawGraph(self, *args):
        '''
        Method to draw the matplotlib graph
        '''

        self.graphFrame = Tk.Frame(self.root)
        f = Figure(figsize=(7,5), dpi=100)
        subplot = f.add_subplot(111)
        if self.plotType == 'line':
            #a.plot(self.xAxis, self.yData)
            subplot.plot(self.falseX, self.yData)
        elif self.plotType == 'bar':
            subplot.bar(self.xAxis, self.yData)
        subplot.set_title(self.Title.get())
        subplot.set_xlabel(self.xLabel.get())
        subplot.set_ylabel(self.yLabel.get())
        subplot.set_ylim(self.yMin.get(), self.yMax.get())
        subplot.set_xlim(self.xMin.get(), self.xMax.get())
        #a.set_xticklabels( self.xTicLabel.get(),  rotation = 45)
        #a.set_xticklabels(map(str, self.xAxis), rotation = 45)
        subplot.xticks(self.falseX, map(str, self.xAxis), rotation='vertical')

        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(f, master = self.graphFrame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.graphFrame.grid(row=1, rowspan=10)


    def add_graph_controls_frame(self):
        graphControls = Tk.Frame(self.root)
        graphControls.grid(row=11)

        #Title
        Tk.Label(graphControls, text = 'Title').grid(row = 1, column = 0)
        self.ctlTitle = Tk.Entry(graphControls)
        self.ctlTitle.config(textvariable = self.Title)
        self.ctlTitle.grid(row = 1, column = 1, columnspan = 10, sticky = 'we', pady=10)

        #YMin Selector
        Tk.Label(graphControls, text = 'Min Y' ).grid(row =2, column=1, padx=3)
        self.yMinSelector = Tk.Entry(graphControls)
        self.yMinSelector.config(textvariable = str(self.yMin))
        self.yMinSelector.config(width=5)
        self.yMinSelector.grid(row = 2, column = 2, sticky = 'w')

        #YMax Selector
        Tk.Label(graphControls, text = 'Max Y' ).grid(row = 2, column=3)
        self.yMaxSelector = Tk.Entry(graphControls)
        self.yMaxSelector.config(textvariable = str(self.yMax))
        self.yMaxSelector.config(width=5)
        self.yMaxSelector.grid(row = 2, column = 4, sticky = 'w')

        #XMin Selector
        Tk.Label(graphControls, text = 'Min X' ).grid(row =3, column=1, padx=3)
        self.xMinSelector = Tk.Entry(graphControls)
        self.xMinSelector.config(textvariable = str(self.xMin))
        self.xMinSelector.config(width=5)
        self.xMinSelector.grid(row = 3, column = 2, sticky = 'w')

        #XMax Selector
        Tk.Label(graphControls, text = 'Max X' ).grid(row = 3, column=3)
        self.xMaxSelector = Tk.Entry(graphControls)
        self.xMaxSelector.config(textvariable = str(self.xMax))
        self.xMaxSelector.config(width=5)
        self.xMaxSelector.grid(row = 3, column = 4, sticky = 'w')

        #Graph Type combobox control
        Tk.Label(graphControls, text = 'Graph Type' ).grid(row = 4, column=1)
        self.ctlPlotType = ttk.Combobox(graphControls, values = ('line','bar'))
        self.ctlPlotType.set(self.plotType)
        self.ctlPlotType.grid(row = 4, column = 2)

        #X Label
        Tk.Label(graphControls, text = 'X-Axis Label' ).grid(row = 5, column=1)
        self.ctlXLabel = Tk.Entry(graphControls)
        self.ctlXLabel.config(textvariable = str(self.xLabel))
        self.ctlXLabel.grid(row = 5, column = 2, columnspan=3, sticky = 'we')

        #Y Label
        Tk.Label(graphControls, text = 'Y-Axis Label' ).grid(row = 6, column=1)
        self.ctlYLabel = Tk.Entry(graphControls)
        self.ctlYLabel.config(textvariable = str(self.yLabel))
        self.ctlYLabel.grid(row = 6, column = 2, columnspan=3, sticky = 'we')


        #Draw Graph Button
        self.btnDrawGraph = Tk.Button(graphControls, text = 'Re-Draw Graph')
        self.btnDrawGraph.grid(row = 10, column = 4, sticky = 'e', pady=10)
        self.btnDrawGraph.bind("<Button 1>", self.redrawGraph)


    def redrawGraph(self, *args):
        try:
            self.yMax.set(int(self.yMaxSelector.get()))
        except:
            pass
        try:
            self.yMin.set(int(self.yMinSelector.get()))
        except:
            pass
        try:
            self.xMax.set(int(self.xMaxSelector.get()))
        except:
            pass
        try:
            self.xMin.set(int(self.xMinSelector.get()))
        except:
            pass

        self.Title.set(self.ctlTitle.get())
        self.plotType = self.ctlPlotType.get()
        self.xLabel.set(self.ctlXLabel.get())
        self.yLabel.set(self.ctlYLabel.get())
        self.graphFrame.destroy()
        self.drawGraph()


if  __name__ == '__main__':
    xAxis = ['aa','ba','c','d','e']
    #xAxis = [1,2,3,4,5]
    cg = NPS_Plotter(xAxis = xAxis
                        ,yData = [1,2,7,0,5]
                     ,Title = 'Demo Title'
                     ,xLabel = 'X Label Demo'
                     ,yLabel = 'Y Label Demo')
    cg.app()


