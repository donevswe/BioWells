# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 16:07:07 2015

@author: evdo-umu
"""

from pandas import ExcelWriter  # Importing the needed modules
import pandas as pd
import numpy as np
import sqlite3
#from pandas.io import sql
import os
import glob

"""The next two classes(Reader and Converter) cooperate with each other for the conversion av files from and to Exel/Csv"""

class Reader:
    """THe class is used for importing/reading form exel and csv files,
        it can easy be expanded with other formats.
        This class is a parent class to the next Converter class
        THis two classes are still under developmnet since I would like to add more formats
    """
    def __init__(self):
        """THe method detmins variable filename that should be given already when the class is called ,
            It also assign a variable dataFRAME which stores the imported data
        """
        #self.dataFRAME=pd.DataFrame()
    
    def import_fromExel(self, filename):
        """This method rads and returns the data impored from exel"""
        dataFRAME=pd.read_excel(filename + '.xlsx')
        #print(self.dataFRAME)
        return dataFRAME
        
    def import_fromCSV(self, filename):
        """This method rads and returns the data impored from csv_file"""
        dataFRAME = pd.read_csv(filename + '.csv', sep=',')
        return dataFRAME
        
    def import_fromText(self, filename):
        dataFRAME = pd.read_csv(filename + '.txt', sep=' ')
        return dataFRAME


class Converter(Reader):
    """THis class is a child class to Reader class.
        The same way as Reader it demands filename already when it is called
    """
    def __init__(self):
        """Inherit every method from Reader"""
        Reader.__init__(self)
    
    def toExel(self, name_file, data):
        """THe method export data to exel"""
        dataFRAME = data
        writer = ExcelWriter(str(name_file) +'.xlsx')
        dataFRAME.to_excel(writer, 'sheet1')
        writer.save()
        
        
    def toCSV(self,  name_file, data):
        """THe method export data to csv_file"""
        dataFRAME = data
        dataFRAME.to_csv(name_file + '.csv',sep=',', index=False, header = True)
        
    def toText(self,  name_file, data):
        """THe method export data to csv_file"""
        dataFRAME = data
        dataFRAME.to_csv(name_file + '.txt',sep=' ', index=False, header = True)
    
        
    def Convert_from_Exel_to_CSV(self, Import_file, Export_file):
        Data = self.import_fromExel(Import_file)
        self.toCSV(Export_file, Data)
        
    def Convert_from_CSV_to_Exel(self, Import_file, Export_file):
        Data = self.import_fromCSV(Import_file)
        Data = np.array(Data)
        columns = list(range(len(Data[0])))
        index = list(range(len(Data)))
        df = pd.DataFrame(Data, index=index, columns=columns)
        self.toExel(Export_file, df)
        
    def Convert_from_Exel_to_Text(self, Import_file, Export_file):
        Data = self.import_fromExel(Import_file)
        self.toText(Export_file, Data)
        
    def Convert_from_CSV_to_Text(self, Import_file, Export_file):
        Data = self.import_fromCSV(Import_file)
        self.toText(Export_file, Data)
        
    def Convert_from_Text_to_CSV(self, Import_file, Export_file):
        Data = self.import_fromText(Import_file)
        self.toCSV(Export_file, Data)
        
    def Convert_from_Text_to_Exel(self, Import_file, Export_file):
        Data = self.import_fromText(Import_file)
        Data = np.array(Data)
        columns = list(range(len(Data[0])))
        index = list(range(len(Data)))
        df = pd.DataFrame(Data, index=index, columns=columns)
        self.toExel(Export_file, df)
        
    def Check_if_to_Path_exist(self, To_file):
        if not os.path.exists(self.path + '/'+str(To_file)+'_files'):
            os.makedirs(self.path + '/'+str(To_file)+'_files')
    
    def Name_to_file(self,path_from_file):
        path= path_from_file.split('/')    
        path = "/".join(path[-1:]) 
        name_to_file = path.split('.')
        return name_to_file[0]
    
    def  List_file_names(self, To):
        list_names_files=[]
        self.To = To
        self.allFiles = glob.glob(self.path + "/*"+ self.filetype)
        self.Check_if_to_Path_exist(self.To)
        for i in range(len(self.allFiles)):
            name_file =self.Name_to_file(self.allFiles[i])
            list_names_files.append(name_file)
        return list_names_files
        
        
    def LoopConverter(self, From, To, pat):
        self.path = pat
        
        if From == 'excel' and To == 'csv':
            self.filetype = '.xlsx'
            for self.name_file in self.List_file_names( To):
                self.Convert_from_Exel_to_CSV(self.path +'/'+ str(self.name_file), self.path + '/'+ str(self.To)+'_files/'+ str(self.name_file))
            
        elif From == 'csv' and To == 'excel': 
            self.filetype = '.csv'
            for self.name_file in self.List_file_names( To):
                self.Convert_from_CSV_to_Exel(self.path +'/'+ str(self.name_file), self.path + '/'+ str(self.To)+'_files/'+ str(self.name_file))
            
                                
        elif From == 'excel' and To == 'text':
            self.filetype = '.xlsx'
            for self.name_file in self.List_file_names( To):
                self.Convert_from_Exel_to_Text(self.path +'/'+ str(self.name_file), self.path + '/'+ str(self.To)+'_files/' + str(self.name_file))
                
        elif From == 'text' and To == 'excel':
            self.filetype = '.txt'
            for self.name_file in self.List_file_names( To):
                self.Convert_from_Text_to_Exel(self.path +'/' + str(self.name_file), self.path + '/'+ str(self.To)+'_files/' + str(self.name_file))
                
        elif From == 'text' and To == 'csv':
            self.filetype = '.txt'
            for self.name_file in self.List_file_names( To):
                self.Convert_from_Text_to_CSV(self.path +'/' + str(self.name_file), self.path + '/'+ str(self.To)+'_files/' + str(self.name_file))
                
        elif From == 'csv' and To == 'text':
            self.filetype = '.csv'
            for self.name_file in self.List_file_names( To):
                self.Convert_from_CSV_to_Text(self.path +'/' + str(self.name_file), self.path + '/'+ str(self.To)+'_files/' + str(self.name_file))
               
                    
                    
            
    def Supported_Files(self):
        return ['excel','csv','text']
            
        




class Sql3:
    """This class takes care of our database handling. 
        It uses database Sqlite3 and module called pandas to navigate through the database.
        It imports, exports, delete, and read data to the databes
    """
    def __init__(self):
        self.filetype = '.xlsx'
    
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

        
    def sql_write(self, df, table_name):
        """THe method write data to the databes
            It demands dataFRAME data, which usually is deliverd by pandas module.
            It also demands a name for the table which serves as ID to  the dataframe
        """
        self.df = df
        sql_db = sqlite3.connect('Sqlite3/test.sql')
        self.df.to_sql(name=table_name, con=sql_db)
        sql_db.close()
        
    def sql_write_raw_data(self, df, table_name, database_name):
        self.df = df
        sql_db = sqlite3.connect('Sqlite3/Raw_Data/' + str(database_name))
        self.df.to_sql(name=table_name, con=sql_db)
        sql_db.close()
        
        
    def Loop_sql_write_raw_data(self, database_name, pat):
        try:
            self.path = pat
            self.list_files = self.Files_to_import()
            try:
                time = pd.read_excel(self.path +'/timePoints' + self.filetype)
                self.sql_write_raw_data(time, 'time_points', database_name)
                tim = np.array(time['time'])
            except:
                tim = np.array(list(range(self.nr_files)))
                time = pd.DataFrame()
                time['time'] = tim
                self.sql_write_raw_data(time, 'time_points', database_name)
                
                
            for i in range(len(tim)):
                data=pd.read_excel(self.path +'/'+ self.list_files[i])
                self.sql_write_raw_data(data, 'output_'+str(i), database_name)
        except:
            pass
            
    def sql_read_raw_data(self, table_name, database_name):
        """THe method read data table from the the database
            It demans only the name/ID of the table
        """
        sql_db = sqlite3.connect('Sqlite3/Raw_Data/' + str(database_name))
        dat=pd.read_sql_query("select * from " + str(table_name), sql_db) # for example table_name = test_table
        #print(dat)
        sql_db.close()
        return dat
        
    def sql_delete_raw_data(self, database_name):
        try:
            os.remove('Sqlite3/Raw_Data/' + str(database_name))
        except:
            pass
    
    def sql_read(self,table_name):
        """THe method read data table from the the database
            It demans only the name/ID of the table
        """
        sql_db = sqlite3.connect('Sqlite3/test.sql')
        dat=pd.read_sql_query("select * from " + str(table_name), sql_db) # for example table_name = test_table
        #print(dat)
        sql_db.close()
        return dat
        
        
    def view_tables(self):
        """THis method delivers all the data tables stored in our database
            This is importnt for tkinter to print out since the user would like to navigate,
            knowing what data is stored in the database. 
        """
        db = sqlite3.connect('Sqlite3/test.sql')
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
        db = sqlite3.connect('Sqlite3/test.sql')
        cursor = db.cursor()
        cursor.execute('''DROP TABLE ''' + str(table_name))
        db.commit()



def Main_Converter(From, To, path):
    """Here we create a function that will be used in tkinter. 
        It uses the classes 'ExtractData_raw_files' and 'Stats' from above,
        to collect data and to calculate Statistics
    """
    path= path.split('/')    # here is better to google and see what is going on. Or experiment alone
    path= "/".join(path[:-1])  # Gooogle it!
    conv = Converter()
    conv.LoopConverter(From, To, path)
    

def Raw_data_to_Sqlite_base(database_name, path): 
    Sq = Sql3()
    Sq.Loop_sql_write_raw_data(database_name, path)
    

if __name__ == "__main__":   # let us see how our classes work
#    """THis sectin shows you how the Converter class works"""
#    file= 'data/output0'         # this will be  a file_name. For example if we have a file  ALLwells.xlsx
#    conv =Converter() #  here the class Converter USES its parent's class methods
#    DF=conv.import_fromExel(file)  #  here the class Converter USES its parent's class Reader methods to import the exel file
#    conv.toText('data/text_test', DF)  # now when we have imported the file we send the data to a file called csv_test.csv
#    # you can see the file csv_test.csv in the folder data. REmove it if you want from the folder and run the code again. NOw you will find the file again in the data folder
#    
#    """Next section shows you how the Sql3 class works"""
#    tabel_namn = 'test_table5'    #  we give name/ID to the table we want to save
#    Sq = Sql3()                     # we give a variable that has our class propeties
#    Sq. sql_write(DF,tabel_namn)    # we import the dataFRAME  which we extracted with the Converter class to our database
#    
#    
#    try:
#        sq= Sq.sql_read(tabel_namn)  #  here we 
#        print('\nTHis is the dataFRAME  you imported to Sslite3! Cool :) :\n\n',sq)
#    except:
#        print('It did not work')
#        
#    Sq.dropTable(tabel_namn)  # WE drop/delete the table from the database and it is as we started
#    a, b=Sq.view_tables()  # here we check what table we have in our database. I have put some tables just to shaow you.
#    print(a,b)    # You can extract these tables with the method Sq.sql_read(tabel_namn) , replacing table_namn with any table name you printed out (it should be a string)

#    From = 'exel'
#    To = 'csv'
#    path = 'data/CSV_files'
#    conv = Converter()
#    conv.LoopConverter(From, To, path)
#    df =   conv.import_fromText('data/text_test') 


#    conv.Convert_from_CSV_to_Exel( 'data/output200', 'data/output200')
#    conv.LoopConverter(From, To, '/home/ev/Documents/4thBioinformatics/ApplicationsProgrammering/WellsBio/data/CSV_files/Exel_files')
    path = '/home/ev/Documents/4thBioinformatics/ApplicationsProgrammering/WellsBio/data/'
    database_name = 'ex'    
    
    #Raw_data_to_Sqlite_base(database_name, path)
    Sq = Sql3()
    DATA=Sq.sql_read_raw_data( 'time_points', database_name)
    print(DATA)
    Sq.sql_delete_raw_data(database_name)
    
    

    







