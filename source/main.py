#!/usr/bin/python
# -*- coding: utf-8 -*-

# move.py

import wx
import random
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
import numpy as np
import pylab
import datetime
from DataManager import getCurrentValue
import time
from threading import Thread
import Queue

frequency = 20.0
max_length = 150

def ThreadFunction(mainFrame):
    while 1>0:
        #mainFrame.data.append(getCurrentValue())
        mainFrame.data.append(getCurrentValue())
        if (len(mainFrame.data)>max_length):
            mainFrame.data.pop(0)
        mainFrame.count+= 1
        time.sleep(1/frequency)

class MainFrame(wx.Frame):
  
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, 
            size=(1000, 800))
            
        #self.datagen = DataGen()
        self.queue = Queue.Queue()
        self.data = [getCurrentValue()]
        self.count = 0
        self.create_main_panel()
            
        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)        
        self.redraw_timer.Start(100)
        
        self.SetSize((1000, 800))
        self.Centre()
        self.Show()
        self.thread = Thread(target=ThreadFunction, args=(self,))
        self.thread.start()
        
    def create_main_panel(self):
        self.panel = wx.Panel(self)

        self.init_plot()
        self.canvas = FigCanvas(self.panel, -1, self.fig)
    
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 1, flag=wx.LEFT | wx.TOP | wx.GROW)        
        
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

    def init_plot(self):
        self.dpi = 100
        self.fig = Figure((3.0, 3.0), dpi=self.dpi)

        self.axes = self.fig.add_subplot(111)
        self.axes.set_axis_bgcolor('black')
        self.axes.set_title('Pulse', size=12)
        
        pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes.get_yticklabels(), fontsize=8)

        # plot the data as a line series, and save the reference 
        # to the plotted line series
        #
        self.plot_data = self.axes.plot(
            self.data, 
            linewidth=1,
            color=(1, 1, 0),
            )[0]
    def draw_plot(self):
        """ Redraws the plot
        """
        
        xmax = (self.count if self.count > max_length else max_length)
        xmin = (xmax - max_length)
        xmax = xmax/frequency
        xmin = xmin/frequency
        ymin = round(min(self.data), 0) - 1
        ymax = round(max(self.data), 0) + 1
        

        self.axes.set_xbound(lower=xmin, upper=xmax)
        self.axes.set_ybound(lower=ymin, upper=ymax)
        

        self.axes.grid(True, color='gray')

        pylab.setp(self.axes.get_xticklabels(), 
            visible=True)
        
        self.plot_data.set_xdata(np.arange(len(self.data))/frequency+xmin)
        self.plot_data.set_ydata(np.array(self.data))
        
        self.canvas.draw()
    def on_redraw_timer(self, event):
        #print datetime.datetime.now()
        self.draw_plot()

if __name__ == '__main__':
  
    app = wx.App()
    MainFrame(None, title='Heart rate')
    app.MainLoop()
