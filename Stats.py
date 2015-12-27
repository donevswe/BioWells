# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 01:03:35 2015

@author: ev
"""

from pandas import ExcelWriter
import pandas as pd
import numpy as np
from Sqlite_Converter import Sql3
import os
import glob



class ExtractData_Sqlite:
    """This class uses the class Sql3 which is imported from the file Sqlite_Converter!
        here we import tables from Sqlite3 database i the __init_ method , then we add every column
        of the imported table to a dictionary with a key correspnding to the each column
    """
    
    def __init__(self, tabel):# here the firt three lines are assigning var
        self.sqdbase = {}    # create a dictionary to store the imported data
        self.tabel_namn = tabel  # assigning the table name which the user s giving from the beggining
        Sq = Sql3()      # here we assign an object belonging to Sql3 class (see OOP)
        
        try:
            self.sqlData = Sq.sql_read(self.tabel_namn)   # we read the data from the database with the given table name
        except:
            print('failed')   # giving an exceptinon in case it failed
    
    
    def getDbase(self):
        """this method prepare the data for use of the Stats class"""
        for item in self.sqlData:    # for every colummn name in the data
            self.sqdbase[item]=np.array(self.sqlData[item])  # add to the dictionary the clomunm name and the corresponding data
        
        self.sqlData['index'] =  list(range(len(self.sqlData['time']))) # since we sometimes have even a column for index(pandas put it automatically) and sometimes not which will not be used for Stats we dropp it out
        self.sqdbase.pop('index') #  we make sure that all dataFRames we are working with has inde column and the drop it
        return self.sqdbase



class ExtractData_raw_files:
    """This class recieves the path where the original files are stored and the filetype (default value is xlsx). It imports the files one by one with help of the module pandas,
        which is used for statistics and dataFRame handeling of data.
        Then it creates a dictionary, where each cell has its own key, with help of it we can append new data/time point to each key in the dictonary.
        So at the end we have one dictioanra conating all data att one place
    """
    def __init__(self, path, filetype = '.xlsx'):
        self.path = path          # assigning variable for the path
        self.filetype = filetype   # assigning varable for the filetype
        self.dataFRAME=pd.DataFrame()   # create a variable for dataFRame (this is a special way to pandas-pd.DataFrame() is special class of pandas that help statisticians to work easy with data)
        self.dbase={}       # WE create a dictionary that will collect our data. Dictionary is as table we have a key and a data conected to that key
        print(self.path)
        self.list_files = []
        
    def Files_to_import(self):
        self.nr_files = len(glob.glob(self.path + "/*_"+ '*' + self.filetype))
        list_files = [0] * self.nr_files
        for i in range(self.nr_files):        
            Files = glob.glob(self.path + "/*_"+ str(i) + self.filetype)
            for File in Files:
                File= File.split('/')    
                File = "/".join(File[-1:])      
                list_files[i] = File
        return list_files
    
    def createDictBase(self):
        """This method import all data files and collect them in one big dictionary, every key is a cell, and contains the data for this cell for all time_points"""
        #allFiles = glob.glob(self.path + "/*"+ self.filetype)
        #data  = pd.read_excel(allFiles[0])
#==================================================================================================================   
#        self.list_files = self.Files_to_import()
#        data=pd.read_excel(self.path +'/'+self.list_files[0]) # importing the first excel sheet from the first/zero time point
        self.list_files = self.Files_to_import()
        try:
            tim = pd.read_excel(self.path +'/timePoints' + self.filetype)  # importin the time points from a shhet called time_points
            time = np.array(tim['time'])  # assigning variable time conataing an array with the timepoints
            self.nr_files = len(time)
        except:
            time = np.array(list(range(self.nr_files))) 
          
        data=pd.read_excel(self.path +'/'+self.list_files[0])
            
        data=np.array(data)       # converts it to array, so we can manipualte the data easier
        #python wants for some reason first to create the dictionary with at least on value before we can run it in a loop. THat is why we have litle redundancy, since the next part is allmost the same.
        for i in range(len(data)):       # the numbers of rows. Goes through the rows
            for ii in range(len(data[i])):    # the numbers of columns. For every row goes through the columns
                cell_id=str(i)+str(ii)  # we create a variable that has a value cell_id= rowNUm colNUm, for example x= '34' means row 3 column 4
                dat=[]  # a list that will contain the first value of the cell. It will be cleaned every time the loop runs the newxt value
                dat.append(data[i][ii])  # we put the value of the well to the list
                self.dbase[cell_id]=dat  # the list is put to the table. For example dabse['cell_id']= some OD value   
                
        # then we go through the rest of the excell time points and collect them
        for i in range(1,len(time)): 
            if self.list_files[i] != 0:
            
                #data  = pd.read_excel(allFiles[i])
                data=pd.read_excel(self.path +'/'+ self.list_files[i]) 
                data=np.array(data)
                for i in range(len(data)):                # the numbers of rows. Goes through the rows
                    for ii in range(len(data[i])):     # the numbers of columns. For every row goes through the columns
                        cell_id=str(i)+str(ii)      # we create a variable that has a value cell_id= rowNUm colNUm, for example x= '34' means row 3 column 4
            
                        tempVar=self.dbase[cell_id]      # here we use a method of exchanging variables to be able to uppdate the cloumn corresponding to the cell_id
                        tempVar.append(data[i][ii])      # add the new data to the copy
                        self.dbase[cell_id] = tempVar    #  uppdate the original dictionary
            else:
                pass
        self.dbase['time'] = time                 # at theend we add a column that takes care of the time_points 
        return self.dbase
        
    def Dbase_to_DF(self):
        """This method gets the dictionary from the previous method(createDictBase(self)), and transform it to a dataFRame, which is easy to import and export to/from files and Sqlite3 """
        for item in sorted(self.dbase.keys()):
            self.dataFRAME[item]=self.dbase[item]
        return self.dataFRAME
        

    def D_Base_to_Exel(self):       
        """This method exports the data collected in the big dictionary and exports it to file (remmember default value = '.xlxs')"""
#        for item in sorted(self.dbase.keys()):       # for every key/cell add to a dataFRAME
#            self.dataFRAME[item]=self.dbase[item]
        
        self.dataFRAME = self.Dbase_to_DF()
        writer = ExcelWriter(self.path+'/ALLwells'+ self.filetype)  # assign a path for the file
        self.dataFRAME.to_excel(writer, 'Sheet1')  # create a file in the same path the original files came from
        writer.save()  
           
    def FrameBase_to_Sqlite(self):
        """This method gives a possibility to us to export the data directly to the dataBase Sqlite3"""
        sql3 = Sql3(self.dataFRAME)   # we import the created from us class Sql3 to add the data 
        sql3.sql_write()     # very simple and easy

class Stats :
    """This class calculate some basic statistics of a given data,
        the data should be given as a dictionary where every key contains a data from a given well. 
        THe method demands, also NrExperiments, the Column we want to have a look at, and lists - start, stop containing, the start and the stop row for the expriments
        example: we habe three experiment att column= 1, then we give for example Col = 1,  Start = [1,4,6]  , Stop = [3,5,8], where the first experiment start att row=1 and finish att row=3.
        THe second experiment starts at row=4 and fiishes att row=5 , and so on. You get the point :)
    """
    def __init__(self, dbase, NrExperiments, col, start, stop):
        self.dbase = dbase         # here we assign the necessary variables needed for the class
        self.NrExperiments = NrExperiments
        self.col = col
        self.start = start
        self.stop = stop
        self.time = dbase['time']  # we also extract the time data as a separate variable
        self.ListExperiments=[]    # we create a variable that will take care of our experiments
    
    def exper(self):
        """This method checks how many experiments are given and create a key for this experiment with the data for it
            in a Experimets dictionary
            
        """
        self.dbase.pop('time')  # since we do not want the time data to be included in our calculation we drop it out.
        ind=list(zip(self.start, self.stop))   # here I recomend to Google;  'zip , list python' to understand what is going on  :)
        Experiments={}                             # assigning a local dictionary variable
        for x in range(self.NrExperiments):
                Experiments["Experiment{0}".format(x)]=[]   # this two lines creates keys for each experment. For each experiment we are going to collect mean and Std
        
        # next passage is a little bit harsh to digest att once    
        for i in range(self.NrExperiments):    # we are looping n-times  n=number of experiments
            for key in sorted(self.dbase.keys()):  # every time we are going through each key of the dictionary with the data
                if len(key) == 2:      #  we check how the key looks like . If you remmember the first number of the key correspons to the row at which cells is, and 
                # the second part of the key corresponds to the column the cell is comming from . For example key = '32' tells you row = 3 , column = 2
                    if int(key[0]) in list(range(ind[i][0],ind[i][1])) and key[1]==str(self.col):   # here we check if the first number of the key (key[0])is in the range of stat-stop row and att the same time 
                    # att which column key[1]. If it is in the searched column and rows we append it to the expriment of interest
                            Experiments["Experiment{0}".format(i)].append(self.dbase[key])
                else:
                    if int(key[0]) in list(range(ind[i][0],ind[i][1])) and key[1]+key[2] ==str(self.col): # WE have columns 10, 11, 12 wich have key like for ex. key = '212' , which tells you row= 2, column = '12'
                            Experiments["Experiment{0}".format(i)].append(self.dbase[key]) # this is the same as above
            
            self.ListExperiments.append(np.array(Experiments["Experiment{0}".format(i)]))  # we collect at the end all data for our experiments in a final list 'ListExperiments'
        return self.ListExperiments        
        

    def _ReplicaStats(self, myreplica):
        """This is an inner method that used in the next Method (Means_Stds(self)), it returns the means,
            for each end every timepoint for the wells included in a an experiment
        """
    
        means=[None]*len(myreplica)  # creating an empty list for the means with the length of my timepoints indexes
        std=[None]*len(myreplica)    # creating an empty list  for the std
        for i in range(len(myreplica)):
            means[i]=np.mean(myreplica[i])   # numpy is calculating the means and std for every row and then add it to the list
            std[i]=np.std(myreplica[i])
        #print(means, std)
        return means, std

    def Means_Stds(self): 
        """This method combines the previuos two methods exper and ReplicaStats
            end returns a list with means and std for each and every replicate
        """
        self.means=[]  # list taking care for the means of ll experiments
        self.stds=[]   # list taking care fro the Stds of all experiments
        for replica in self.exper():   # remember self.exper, from above returns ListExperiments
            mean, Std = self._ReplicaStats(replica.T)  # here calculates the means and Stds. WE have to transpose the matrix. .T stands for transpose
            self.means.append(mean)  # the calculted data for each experiment is gethered in one place
            self.stds.append(Std)
        #print(self.means, self.stds)
        return self.means, self.stds
    
    def time_return(self):
        """A method for just returning the time points"""
        return self.time
    
    def DbaseReturn(self):
        """A method for just returning the original data dictionary. Not neccesary to have but good for checking our data"""
        return self.dbase

def MainStats(path, filetype, NrExp, col, start, stop):
    """Here we create a function that will be used in tkinter. 
        It uses the classes 'ExtractData_raw_files' and 'Stats' from above,
        to collect data and to calculate Statistics
    """
#    path= path.split('/')    # here is better to google and see what is going on. Or experiment alone
#    path= "/".join(path[:-1])  
    dato=ExtractData_raw_files(path, filetype)
    dBase=dato.createDictBase()
    stats = Stats(dBase, NrExp, col, start, stop)
    means, stds=stats.Means_Stds()
    times = stats.time_return()
    return means , stds, times

def MainStats_from_Sqlite3(table_name, NrExp, col, start, stop):
    """Here we create a function that will be used in tkinter. 
        It uses the classes 'ExtractData_Sqlite' and 'Stats' from above,
        to collect data and to calculate Statistics
    """
    a = ExtractData_Sqlite(table_name)
    db = a.getDbase()
    stats = Stats(db, NrExp, col, start, stop)
    means, stds=stats.Means_Stds()
    times = stats.time_return()
    return means , stds, times
    

#=============================================================================
if __name__ == "__main__":  # this line means that from now on the code runed can not be exprorted anywhere. IT can be run only from this file. Good for testing
    """Let us have a look how our classes works"""
    pat = 'data'
    b= ExtractData_raw_files(pat)
    dbs = b.createDictBase()
    DBS = b.Dbase_to_DF()
   # b.D_Base_to_Exel()
    print('This is all your data: \n\n', DBS,'\n')
#    
#    column = 2
#    startList_rows = [1,4]
#    stopList_rows = [3,7]
#    Antal_experiemnts = len(startList_rows)   # or you can just write = 2
#    statistics = Stats(dbs,Antal_experiemnts, column, startList_rows, stopList_rows)
#    MEANS, STDS = statistics.Means_Stds()
#    print('Means for the first experiment : \n\n',MEANS[0],'\n')
#    print('Stds for the first experiment : \n\n',STDS[0],'\n')
#    
#    print('Means for the second experiment : \n\n',MEANS[1],'\n')
#    print('Stds for the second experiment : \n\n',STDS[1],'\n')



#    tabelNamn = 'mytable'
#    a = ExtractData_Sqlite(tabelNamn)




#    db = a.getDbase()
#    
##    dbs = b.createDictBase()
##    
#    st = Stats(db, 1, 10, [1], [5])
#    mea, stds = st.Means_Stds()
#    tid = st.time_return()
##    
##    st1 = Stats(dbs, 1, 10, [1], [5])
##    mea1, stds1 = st1.Means_Stds()



