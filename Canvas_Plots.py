# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 22:05:56 2015

@author: ev
"""
# The following lines import some necessary python modules. Let me kow if something is not working on your system
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import tkinter as tk
import os
#matplotlib.use('Agg')
from mpl_toolkits.axes_grid1 import make_axes_locatable


"""THis time I am not going to explain very much. Most of the things are technicle plotting issues
    These you could google if you are intersted of. JUst Google matplotlib bar, graph or heat map to become more familliar what is going on here

"""

"""THe first class Pack_App(tk.Tk) is the parent class of the classes that follow bellow. Since tk. is inherited to every class below and
         the things are getting rather complicated even for me, I keep some global variables that are used from of all the parent classes bellow.
         It is a little bit unusuall approach but it works perfectly. However you do not have to care about it that much."""


LARGE_FONT= ("Verdana", 12)  # I am decide how the texts will apear on tkinter

class Pack_App(tk.Tk):
    def __init__(self, mean, std, tid, titel = "Wells' Experiments", xlabel = 'Time Units', ylabel = 'Abs', *args, **kwargs):
        # creates some global variables that will be used in the children classes bellow. WE have some default values
        global means, stds, time, path,titels, xlabels, ylabels
        means = mean
        stds = std
        time = tid
        titels = titel
        xlabels = xlabel
        ylabels = ylabel
        
        tk.Tk.__init__(self, *args, **kwargs)
         #"""THe next couple of lines I am commenting out since you are working on Windows and I have not tested the program on Windows yet"""
         
        if "nt" == os.name:
            tk.Tk.wm_iconbitmap(self, bitmap = "96wellsystem.ico")
        else:
            tk.Tk.wm_iconbitmap(self, bitmap = "@96wellsystem.xbm")
        
        tk.Tk.wm_title(self, "Visualizing Data BioWells")
        
        
        container = tk.Frame(self)   # tkinter syntax for frame
        container.pack(side="top", fill="both", expand = True)  # tkinter syntax . Not easy to explain
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # creating a dictionary that will store our children classes

        for F in (Plot, BarPlot, HeatMap, Graph):  # the next lines fill the dictionary up give them some position properties. Not so important. Google it if yo like

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=1, column=1, sticky="nsew")

        self.show_frame(Plot)

    def show_frame(self, cont):   # this function tells for itself

        frame = self.frames[cont]
        frame.tkraise()
        


        
class Plot(tk.Frame):
    """THis class creates the wellcome page of our plots"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent, bg ='antique white')
        label = tk.Label(self, text=' '*43 + "Start Page"+ ' '*43, font=LARGE_FONT,bg='light sea green')   # creates labels 
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Bar Plot", fg="light sea green",font=("Helvetica", 15),  # creates buttons
                            command=lambda: controller.show_frame(BarPlot))
        button1.pack()

        button2 = tk.Button(self, text="Heat Map",fg="light sea green",font=("Helvetica", 15),
                            command=lambda: controller.show_frame(HeatMap))
        button2.pack()

        button3 = tk.Button(self, text=" Graph  ",fg="light sea green",font=("Helvetica", 15),
                            command=lambda: controller.show_frame(Graph))
                            
        button3.pack()
        
        left, width = .25, .5
        bottom, height = .25, .5
        right = left + width
        top = bottom + height
        
        f = Figure(figsize=(7,7), dpi=100)
        f = Figure( dpi=100)
        f.suptitle('', fontsize=12)
        
        ax = f.add_subplot(111)
        ax.set_ylim([0.0,8])
        ax.set_xlim([0,12])
        
        if len(means[0]) == 0:
            
            ax.text(right, top, "Misstake accured! Check Your Imput Data!!!",
                    horizontalalignment='right',
                    verticalalignment='bottom',
                    color='blue',fontsize=15,
                    transform=ax.transAxes)
            
            
            ax.text(0.5*(left+right), bottom, 'Your Start-Well Should Have Lower Row Nr. Than The Start-Well !!! ',
                    horizontalalignment='center',
                    verticalalignment='top',
                    color='green',fontsize=15,
                    transform=ax.transAxes)
    
            
            
            ax.text(0.5*(left+right), 0.5*(bottom+top), 'Be sure that you have given file directory',
                    horizontalalignment='center',
                    verticalalignment='center',
                    fontsize=15, color='red',
                    transform=ax.transAxes)
            
            
        else:
        
            ax.text(right, top, "Wellcome to BioWells' Plots",
                    horizontalalignment='right',
                    verticalalignment='bottom',
                    color='blue',fontsize=20,
                    transform=ax.transAxes)
            
            
            ax.text(right, bottom, ' To see your plots ',
                    horizontalalignment='center',
                    verticalalignment='top',
                    color='green',fontsize=20,
                    transform=ax.transAxes)
    
            
            
            ax.text(0.5*(left+right), 0.5*(bottom+top), 'Choose an option from above',
                    horizontalalignment='center',
                    verticalalignment='center',
                    fontsize=20, color='red',
                    transform=ax.transAxes)
        
        
        ax.invert_yaxis()
        ax.xaxis.tick_top()
        
        ax.set_xticklabels(' GRAPH ', color="pink",minor=False)
        
        ax.set_yticklabels(' MAP BAR', color="pink",minor=False)
        ax.grid(True)
        ax.tick_params(axis='x', labelsize=14)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        

class BarPlot(tk.Frame):
    """THis class delivers the BarPLots.I have used some not so buetyful approach since for different number of samples, 
        because I had to addapt the appearance of the plots individually. difficult to automatise in one function
        
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,  bg ='antique white')
        label = tk.Label(self, text= ' '*43 + " Bar PLot!!! " + 43*' ', font=LARGE_FONT,bg='light sea green')
        label.pack(pady=10,padx=10)
        self.means = means
        self.stds = stds

        button1 = tk.Button(self, text="  PLot  ", fg="light sea green", 
                            command=lambda: controller.show_frame(Graph))
                            
        button1.pack()

        button2 = tk.Button(self, text="Heat Map",fg="light sea green", 
                            command=lambda: controller.show_frame(HeatMap))
        button2.pack()

        f = Figure(figsize=(7,7), dpi=100)
        a = f.add_subplot(111)
        ind = np.arange(len(self.means[0]))  # the x locations for the groups
        width = 0.35 # the width of the bars
        if len(self.means) == 1:
            rects1 = a.bar(ind, self.means[0], width, color='r', yerr=self.stds[0])
            a.legend(('1'))
            a.set_xticks(ind)
        
        elif len(self.means) == 2:
            rects1 = a.bar(ind, self.means[0], width, color='r', yerr=self.stds[0])            
            rects2 = a.bar(ind + width, self.means[1], width, color='y', yerr=self.stds[1])
            a.legend((rects1[0], rects2[0]), ('Sample1', 'Sample2'), loc = 'upper left')
            a.set_xticks(ind+0.5)
        
        elif len(self.means) == 3:
            width =0.25
            rects1 = a.bar(ind-width , self.means[0], width=0.25, color='r', yerr=self.stds[0])            
            rects2 = a.bar(ind , self.means[1], width=0.25, color='y', yerr=self.stds[1])
            rects3 = a.bar(ind + width, self.means[2], width=0.25, color='g', yerr=self.stds[2])
            a.legend((rects1[0], rects2[0],rects3[0]), ('Sample1', 'Sample2', 'Sample3'), loc = 'upper left') 
            a.set_xticks(ind)
            a.xaxis_date()
            a.autoscale(tight=False)
            
        elif len(self.means) == 4:
            width =0.20
            rects1 = a.bar(ind+2*width , self.means[0], width=0.20, color='r', yerr=self.stds[0])            
            rects2 = a.bar(ind+3*width , self.means[1], width=0.20, color='y', yerr=self.stds[1])
            rects3 = a.bar(ind + 4*width, self.means[2], width=0.20, color='g', yerr=self.stds[2])
            rects4 = a.bar(ind + 5*width, self.means[3], width=0.20, color='c', yerr=self.stds[3])
            a.legend((rects1[0], rects2[0],rects3[0], rects4[0]), ('Sample1', 'Sample2', 'Sample3', 'Sample4'), loc = 'upper left') 
            a.set_xticks(ind)
            a.xaxis_date()
            a.autoscale(tight=False)
            
        elif len(self.means) == 5:
            width =0.16
            rects1 = a.bar(ind+2*width , self.means[0], width=0.16, color='r', yerr=self.stds[0])            
            rects2 = a.bar(ind+3*width , self.means[1], width=0.16, color='y', yerr=self.stds[1])
            rects3 = a.bar(ind + 4*width, self.means[2], width=0.16, color='g', yerr=self.stds[2])
            rects4 = a.bar(ind + 5*width, self.means[3], width=0.16, color='c', yerr=self.stds[3])
            rects5 = a.bar(ind + 6*width, self.means[4], width=0.16, color='violet', yerr=self.stds[4])
            a.legend((rects1[0], rects2[0],rects3[0], rects4[0], rects5[0]), ('Sample1', 'Sample2', 'Sample3', 'Sample4','Sample5'), loc = 'upper left') 
            a.set_xticks(ind)
            a.xaxis_date()
            a.autoscale(tight=False)
        
        # add some text for labels, title and axes ticks
        a.set_ylabel(ylabels)
        a.set_xlabel(xlabels)
        a.set_title(titels)
        a.set_xticklabels([str(x) for x in time[::1]])
        a.autoscale(tight=True)
        a.grid(True)    
    
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class HeatMap(tk.Frame):
    """DElivers the heat map. Google for details"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg ='antique white')
        label = tk.Label(self, text=' '*43 +"Heat Map!!!" + ' '*43, font=LARGE_FONT, bg='light sea green')
        label.pack(pady=12,padx=8)

        button1 = tk.Button(self, text="  PLot  ", fg="light sea green",
                            command=lambda: controller.show_frame(Graph))
        button1.pack()

        button2 = tk.Button(self, text="Bar Plot",fg="light sea green", 
                            command=lambda: controller.show_frame(BarPlot))
        button2.pack()
        f = Figure(figsize=(8,7), dpi=100)
        f.suptitle(titels, fontsize=12)
        self.means = means
        self.time = time
        a = f.add_subplot(111)
        
        y_labels = leg(len(self.means))
        x_labels = self.time


        df = pd.DataFrame(self.means)
        df = np.array(df)
        heatmap =a.pcolor(df, cmap=plt.cm.Blues, edgecolors='w') # create the heta (put white lines between squares in heatmap)
        
        a.set_yticks(np.arange(0.5, 8,1))
        a.set_yticklabels(y_labels, minor=False)
        a.set_xticks(np.arange(0.5, len(self.means[0]),1))
        a.set_xticklabels( x_labels,minor=False)
        a.grid(True)
        a.set_title('Hi everyone! How Cool is Python :)!!!')
        a.set_ylabel(ylabels)
        a.set_xlabel(xlabels)
        a.autoscale(tight=True)  # get rid of whitespace in margins of heatmap
        a.set_aspect('equal')    # ensure heatmap cells are square
        a.tick_params(bottom='off', top='off', left='off', right='off')  # turn off ticks
        divider = make_axes_locatable(a)
        cax = divider.append_axes("right", "3%", pad="1%")
        f.colorbar(heatmap, cax=cax)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class Graph(tk.Frame):
    """Growing curves in logarithmic scale. Again Google it for details."""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg ='antique white')
        label = tk.Label(self, text=' '*43 + "Graph Page!!!" + ' '*43, font=LARGE_FONT, bg='light sea green')
        label.pack(pady=10,padx=10)
        self.means = means
        self.stds = stds
        self.time = time
        
        
        button2 = tk.Button(self, text="Bar Plot", fg="light sea green", 
                            command=lambda: controller.show_frame(BarPlot))
        button2.pack()
        
        button3 = tk.Button(self, text="Heat Map", fg="light sea green", 
                            command=lambda: controller.show_frame(HeatMap))
        button3.pack()
        

        f = Figure(figsize=(7,7), dpi=100)
        #f = Figure( dpi=100)
        f.suptitle('', fontsize=12)
        
        a = f.add_subplot(111)
        
        for i in range(len(self.means)):
            a.errorbar(self.time, self.means[i],self.stds[i])     
        
        tu=leg(len(self.means))
        a.legend(tu, loc = 'upper left')
            
        a.set_xscale('linear',fontsize=16)
        a.set_yscale('log',fontsize=16)
        #a.set_ylim([0.03,0.05])
        a.set_xlim([-10,self.time[-1]+10])
        a.set_title(titels)
        a.set_xlabel(xlabels)
        a.set_ylabel(ylabels)
        a.autoscale(tight=True)
        a.grid(True)
        a.tick_params(axis='x', labelsize=14)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
def leg(n):
    """THis function is used in the plots to deliver Legends, or y_axis labels authomaticaly"""
    li=[]
    for i in range(1,n+1):
        li.append("Sample{0}".format(i))
    return tuple(li)

        
def plo(mea, st,tim , tit= "Wells' Experiments", xlbl='Time Units', ylbl='Abs'): 
    
    """Here we put the things together, REady for the big Tkinter interface """ 
    
    app = Pack_App(mea, st, tim, tit, xlbl, ylbl)
    app.mainloop()


#=============================================================================
if __name__ == "__main__":  # this line means that from now on the code runed can not be exprorted anywhere. IT can be run only from this file. Good for testing
    """As ussua let us see how our classes works"""
    meanses = [[0.050500000000000003,0.059000000000000004,0.053999999999999999,0.062, 0.059000000000000004, 0.060499999999999998, 0.063, 0.0625, 0.063500000000000001,0.068000000000000005,0.068500000000000005],
               [0.048666666666666671, 0.059666666666666666,0.058333333333333327,0.069000000000000006, 0.072333333333333347, 0.079000000000000001, 0.08533333333333333, 0.08666666666666667,0.095000000000000015,0.099000000000000019,0.10866666666666665]]
    
    stdses = [[0.0045000000000000005,0.010000000000000002,0.0069999999999999993,0.0070000000000000027,0.0090000000000000011,0.0065000000000000023,0.010999999999999999,0.0084999999999999971,0.0084999999999999971,0.010999999999999999,0.012500000000000001],
             [0.0044969125210773475,0.008178562764256863,0.0083399973354645399, 0.0049665548085837778,0.0030912061651652309,0.0061644140029689758, 0.0079302515022468805, 0.0091772665986241397,0.0061644140029689758,0.0085244745683629494,0.0089566858950295997]] 
    times=np.array([0, 75, 120, 180, 240, 300, 370, 420, 480, 540, 600 ])           

 
    p=plo(meanses, stdses, times)
    
    
    
    







