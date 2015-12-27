# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 00:55:28 2015

@author: ev
"""
import pandas as pd
import numpy as np
import sqlite3
#from pandas.io import sql
import os


class Sql3:
    """This class takes care of our database handling. 
        It uses database Sqlite3 and module called pandas to navigate through the database.
        It imports, exports, delete, and read data to the databes
    """

    def sql_write(self, df, table_name):
        """THe method write data to the databes
            It demands dataFRAME data, which usually is deliverd by pandas module.
            It also demands a name for the table which serves as ID to  the dataframe
        """
        self.df = df
        sql_db = sqlite3.connect('test.sql')
        self.df.to_sql(name=table_name, con=sql_db)
        sql_db.close()
    
    def sql_read(self,table_name):
        """THe method read data table from the the database
            It demans only the name/ID of the table
        """
        sql_db = sqlite3.connect('test.sql')
        dat=pd.read_sql_query("select * from " + str(table_name), sql_db) # for example table_name = test_table
        #print(dat)
        sql_db.close()
        return dat
        
        
    def view_tables(self):
        """THis method delivers all the data tables stored in our database
            This is importnt for tkinter to print out since the user would like to navigate,
            knowing what data is stored in the database. You all had lektue on Sqlite3 so leave the rest of the cde uncommented
            for you to investigate it on your own.
        """
        db = sqlite3.connect('test.sql')
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        table_list = []
        table_names= 'These are the tables in your Data Base:' + str('\n\n')
        for table_name in tables:
            table_name = table_name[0]
            #table = pd.read_sql_query("SELECT * from %s" % table_name, db)
            table_names +=  table_name + str('\n') + str('\n')
            table_list.append(table_name)
        #print(table_names)
        cursor.close()  
        return table_names, table_list
        
        
    def dropTable(self, table_name):
        """This method delete/drop a table
            It only demands the name of the table the user want to delete fron Sqlite3
        """
        db = sqlite3.connect('test.sql')
        cursor = db.cursor()
        cursor.execute('''DROP TABLE ''' + str(table_name))
        db.commit()


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
    



if __name__ == "__main__":   # let us see how our classes work
    tabelNamn = 'alena'
    column = 2
    startList_rows = [1,4]
    stopList_rows = [3,7]
    Antal_experiemnts = len(startList_rows)   # or you can just write = 2
    means , stds, times = MainStats_from_Sqlite3(tabelNamn, Antal_experiemnts, column, startList_rows, stopList_rows)
    print('Means for the first experiment : \n\n',means[0],'\n')
    print('Stds for the first experiment : \n\n',stds[0],'\n')
    
    print('Means for the second experiment : \n\n',means[1],'\n')
    print('Stds for the second experiment : \n\n',stds[1],'\n')
    
    
    
    
    
    
    
    
    
    
    
    