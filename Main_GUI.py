# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 15:20:19 2015

@author: evgeniydonev
"""

import webbrowser
import numpy as np
#import tkinter
from tkinter import *
from tkinter import filedialog
import os
import tkinter.simpledialog as simpledialog
import tkinter.messagebox

#===============================================================================================

from WellBottons import botons
from Stats import MainStats, MainStats_from_Sqlite3, ExtractData_raw_files
from Canvas_Plots import plo
from Sqlite_Converter import Sql3, Raw_data_to_Sqlite_base, Main_Converter, Converter


class GUI:
    def __init__(self):
        self.Sq = Sql3()
        self.bottons = botons()
        self.table_chosen = False
        self.plotnr_file =  -1
        self.plotnr_db = -1
        self.MenuFile = False
        self.MenyDataBase = False
        self.GivenDirectory = False
        self.GivenDataBase = False
        self.added_Samples = True
        
        
        
        
        
        
    #######################################################################
    def new_file(self):
        self.root.title("Untitled")
        self.filename = None			
        self.textPad.delete(1.0,END)	
        
    def open_file(self):
        self.filename = filedialog.askopenfilename(defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
        if self.filename == "": # If no file chosen.
            self.filename = None # Absence of file.
        else:
            self.root.title(os.path.basename(self.filename) + " - pyPad") # Returning the basename of 'file'
            self.textPad.delete(1.0,END)         
            fh = open(self.filename,"r")        
            self.textPad.insert(1.0,fh.read()) 
            fh.close()
    
    def openExcel(self):
        self.filename = filedialog.askopenfilename(defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
        if self.filename == "": # If no file chosen.
            self.filename = None # Absence of file.
        else:
            webbrowser.open(self.filename)
    
         
    def GivePath(self): 
        tkinter.messagebox.showinfo(title = 'Status',message = "Your data files shoud be in '.xlsx' format!" )
        try:
            self.directory = filedialog.askdirectory( title = 'Select A Folder', parent = self.root)
            if self.directory == "": # If no file chosen.
                
                tkinter.messagebox.showwarning("Directory Status", "Directory Not Found!")
                pass
                
                
            elif self.directory != "":
                tkinter.messagebox.showinfo(title = 'Directory Status', message = 'Directory Found! Next Step; Add Samples' ) 	
                self.GivenDirectory = True
                
        except:
            pass
        
    def AditionalPLots_from_file(self):
        self.add_Samples_well_bot()        
        self.Plotting_from_file_bottons()
        
    def Add_to_Text_pad(self, text):
        self.textPad.delete(1.0,END)
        self.textPad.insert(1.0, text)
        self.textPad.tag_add("start", "1.0", "25.13")
        self.textPad.tag_config("start", background="khaki", foreground="black")
        
        
    def PlotDabseTables_bottons(self):
        self.datTables, self.tableList = self.Sq.view_tables()
        self.Add_to_Text_pad(self.datTables)
        
        while True:
                try:
                    self.Table_name = simpledialog.askstring("Name prompt", "Enter Table Name or type 'quit to exit' \n (You see the available tables in the text editor)" )
                    if len(self.Table_name) == 0:
                        tkinter.messagebox.showwarning("showwarning", "PLease add Table Name! Or Type 'quit' to exit")
                    elif self.Table_name == 'quit':
                        break
                    else:
                        if self.Table_name in self.tableList:
                            self.GivenDataBase = True
                            tkinter.messagebox.showinfo(title = "Experiment Status", message = "Experiment Found! Next Step; Add Samples and Press 'PLot Your Data'!" )
                            break
                            
                        else:
                            tkinter.messagebox.showwarning("Add Expriment", "Table Not Found! Try again")
            
                except:
                    break
    
            
    def AditionalPLots_from_dbase(self):
        try:
            if self.GivenDataBase == True: 
                self.add_Samples_well_bot()
                self.PLotting_from_dbase_bottons()
            else:
                tkinter.messagebox.showwarning("Additional Plots", "Table is Not Defined! Choose Table First")
        except:
            pass
            

                
    def ViewDabseTables(self):
        self.datTables, self.tableList = self.Sq.view_tables()
        self.Add_to_Text_pad(self.datTables)
        
        return self.datTables, self.tableList
        
    def View_raw_data_from_Dbase(self):
        self.datTables, self.tableList = self.ViewDabseTables() # print out in the text editor which tables we have in Sqlite3
        
        self.experiment_name = simpledialog.askstring("View Raw Data", "Enter A Experiment Name:" +  "(See text editor for Experiments!)" )
        if self.experiment_name in self.tableList:
            time_points=self.Sq.sql_read_raw_data( 'time_points', self.experiment_name)
            time_points.pop('index')
            self.Add_to_Text_pad(time_points)
            
            self.output_nr  = simpledialog.askstring("View Raw Data", "Enter Nr. of Output:" + "  "+"(See your time_points in the text editor!)" )
            output = self.Sq.sql_read_raw_data('output_' + str(self.output_nr), self.experiment_name)
            output.pop('index')
            self.Add_to_Text_pad(output)
        else:
            tkinter.messagebox.showwarning("View Raw Data", "Experiment Not Found!")
       
        
    def  Import_to_dbase(self):
        tkinter.messagebox.showinfo(title = 'Status',message = "Your data files shoud be in '.xlsx' format!" )
        try:
            #self.directory = filedialog.askopenfilename(defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
            self.directory = filedialog.askdirectory( title = 'Select A Folder', parent = self.root)
            if self.directory == "": # If no file chosen.
                
                tkinter.messagebox.showwarning("Directory Status", "Directory Not Found!")
                pass
                
                
            elif self.directory != "":
                #tkinter.messagebox.showinfo(title = 'Directory Status', message = 'Directory Found! Next Step; Add Samples' ) 	
                try:
                    dato=ExtractData_raw_files(self.directory)
                    dato.createDictBase()
                    DF = dato.Dbase_to_DF()
                    tkinter.messagebox.showinfo(title = 'Directory Status', message = 'Directory Found! Next Step; Add Experiment Name!' ) 
                    self.textPad.delete(1.0,END)
                    self.textPad.insert(1.0, DF) 
                    self.textPad.tag_add("start", "1.0", "25.13")
                    self.textPad.tag_config("start", background="green", foreground="black")
                    self.ViewDabseTables() # print out in the text editor which tables we have in Sqlite3
                    
                    experiment_name = simpledialog.askstring("Import Data", "Enter Experiment Name (see your experiments in the text editor)" )  # for ex.  tabel_namn = 'test_table5
                    if len(experiment_name) != 0:
                        Raw_data_to_Sqlite_base(experiment_name, self.directory)
                        self.Sq.sql_write(DF,experiment_name)
                        self.ViewDabseTables()
                    elif len(experiment_name) != 0:
                        tkinter.messagebox.showinfo(title = 'Import Data', message = 'No data has been saved!' ) 
                        pass
                        
                except:
                    tkinter.messagebox.showinfo(title = 'Directory Status', message = 'You chose to quit!' ) 
                
        except:
            pass
        

        
    def Drop_from_dbase(self):
        self.datTables, self.tableList = self.Sq.view_tables()
        self.Add_to_Text_pad(self.datTables)
        try:
            self.experiment_name = simpledialog.askstring("Delete Data", "Enter Experiment Name: " + "(See text editor for Experiments!)" )
            
            if self.experiment_name in self.tableList:
                answer = simpledialog.askstring("Delete Data", "Do you really want to delete Experiment?: y/n" , initialvalue='n')
                if answer == 'y':
                    self.Sq.dropTable(self.experiment_name)
                    self.Sq.sql_delete_raw_data(self.experiment_name)
                    self.datTables, self.tableList = self.Sq.view_tables()
                    tkinter.messagebox.showinfo(title = 'Delete Data',message = 'Experiment Deleted!' )
                    self.Add_to_Text_pad(self.datTables)
                    
                else:
                    tkinter.messagebox.showinfo(title = 'Delete Data',message = 'Experiment Not Deleted!' )
                    
                
                
            else:
                tkinter.messagebox.showwarning("Delete Data", "Table Not Found!")
        except:
            pass          
     
    
    def add_Samples_well_bot(self):
        try:
            self.Start, self.Stop, self.Col = self.bottons.bot()
            self.added_Samples = True
            for i in range(len(self.Start)):
                if self.Start[i] > self.Stop[i]:
                    tkinter.messagebox.showwarning("Imput Wells", "Start-Well row should have lower Nr. than Stop-Well Nr.!")
                    self.NrExp = len(self.Start)
                else:
                    
                    self.NrExp = len(self.Start)
                    print(self.Col, self.Start, self.Stop )
        except:
            self.Start = [1]
            self.Stop = [0]
            self.Col = 2
            
           
    def PlottBotton_Counter_zeroingFile(self):
        self.plotnr_file = -1
        
    def PlottBotton_Counter_zeroingDB(self):
        self.plotnr_db = -1
        
       
    def CloseMasterFile(self):
        if self.MenuFile == True:
            self.mast.destroy()
        else:
            pass
        
    def File_options_Frame(self):
        self.mast = Tk()
        self.center_window(self.mast, 980, 850, 2,1,1,2)
        self.MenuFile = True
        if "nt" == os.name:
            self.mast.wm_iconbitmap(bitmap = "96wellsystem.ico")
        else:
            self.mast.wm_iconbitmap(bitmap = "@96wellsystem.xbm")
        self.mast.geometry('410x320')
        self.mast.title("From File Menu")
        def ActivBotton():
            if self.GivenDirectory == True:
                answer = simpledialog.askstring("Plotting Status", "Are you ready for plotting?: y/n" )
                if answer ==  'y':
                    if self.plotnr_file == -1:
                        Button(self.fr, text='3        PLot Your Data        ', fg="red",font=("Helvetica", 15), command =self.combine_funcs(self.CleanTextPad,self.bottons.close, self.Gui_close)).pack( padx=5, pady=2)
                        Button(self.fr, text='4   Personalize Your Last Plot ', fg="light sea green",font=("Helvetica", 15),command=self.combine_funcs(self.CleanTextPad,self.PLotTetxs_file)).pack(padx=5, pady=2)
                        Button(self.fr, text='5    Plot Additional  Samples  ', fg="light sea green",font=("Helvetica", 15), command =self.combine_funcs(self.CleanTextPad,self.AditionalPLots_from_file)).pack( padx=5, pady=2)
                        self.add_Samples_well_bot()           
                        self.Plotting_from_file_bottons()
                        self.plotnr_file +=1
                    elif self.plotnr_file != -1:
                        self.add_Samples_well_bot()           
                        self.Plotting_from_file_bottons()
                        self.plotnr_file +=1
                else: 
                    tkinter.messagebox.showinfo(title = 'Directory Status', message = 'You chose to quit!' ) 
                    close_master()
            else:
                #tkinter.messagebox.showinfo(title = 'Directory Status', message = 'Directory Not Given!' ) 
                pass
                
                
        def close_master():
            self.mast.destroy()
            
        self.shortcutbar = Frame(self.mast,  height=25, bg='light sea green')
        self.shortcutbar.pack(expand=NO, fill=X)
        self.lnlabel = Label(self.mast, width=2,  bg = 'antique white')
        self.lnlabel.pack(side=LEFT, anchor='nw', fill=Y)
        self.lnlabel1 = Label(self.mast,  width=2,  bg = 'antique white')
        self.lnlabel1.pack(side=RIGHT, anchor='nw', fill=Y)
        self.fr = Frame(self.mast, bd=2, relief=SUNKEN)
        self.fr.pack(side=LEFT)
        Label(self.fr,  text='           Work Flow           ', fg="orange", font=("Helvetica", 20)).pack()  
        Button(self.fr, text='    From DataBase Menu  ', fg="blue",font=("Helvetica", 15), command = self.combine_funcs(self.CleanTextPad ,self.Data_base_options_Frame, self.FromDataBaseWorkFlow, self.CloseMasterFile, self.PlottBotton_Counter_zeroingFile)).pack(padx=30, pady=10)
        Button(self.fr, text='1    Import Tables to DataBase    ', fg="light sea green",font=("Helvetica", 15), command =self.combine_funcs(self.CleanTextPad,self.Import_to_dbase)).pack( padx=5, pady=2)
        Button(self.fr, text='2  Give Files and Plottig Samples ', fg="light sea green",font=("Helvetica", 15), command = self.combine_funcs(self.CleanTextPad, self.GivePath, ActivBotton)).pack(padx=5, pady=2)
        
        
        #self.mast.mainloop()
    
    def CloseMasterDb(self):
        if self.MenyDataBase == True:
            self.master.destroy()
        else:
            self.FromDataBaseWorkFlow()
    
            
    
    def Data_base_options_Frame(self):
        self.master = Tk()
        self.center_window(self.master, 980, 850, 2,1,1,2)
        self.MenyDataBase = True
        self.dataBase = True
        if "nt" == os.name:
            self.master.wm_iconbitmap(bitmap = "96wellsystem.ico")
        else:
            self.master.wm_iconbitmap(bitmap = "@96wellsystem.xbm")
        self.master.geometry('410x400')
        self.master.title("From DataBase Menu")
        def ActivBotton1():
            if self.GivenDataBase == True :
                answer = simpledialog.askstring("Plotting Status", "Are you ready for plotting?: y/n" )
                if answer ==  'y':
                    if self.plotnr_db == -1:
                        
                        Button(self.fr, text='6        PLot Your Data      ', fg="red",font=("Helvetica", 15), command =self.combine_funcs(self.bottons.close, self.Gui_close)).pack( padx=5, pady=2)
            
                        Button(self.fr, text='7  Personalize Your Last Plot', fg="light sea green",font=("Helvetica", 15), command =self.combine_funcs(self.CleanTextPad ,self.Plotexts_dbase)).pack( padx=5, pady=2)
                        Button(self.fr, text='8    Plot Additional Samples ', fg="light sea green",font=("Helvetica", 15), command =self.combine_funcs(self.CleanTextPad,self.AditionalPLots_from_dbase)).pack( padx=5, pady=2)
                        self.add_Samples_well_bot()
                        self.PLotting_from_dbase_bottons()
                        self.plotnr_db += 1
                    elif self.plotnr_db != -1:
                        self.add_Samples_well_bot()           
                        self.PLotting_from_dbase_bottons()
                        self.plotnr_db += 1
                else:
                    tkinter.messagebox.showinfo(title = 'Directory Status', message = 'You chose to quit!' ) 
                    close_master()
            else:
                pass
            
        def close_master1():
            self.master.destroy()
        self.shortcutbar = Frame(self.master,  height=25, bg='light sea green')
        self.shortcutbar.pack(expand=NO, fill=X)
        self.lnlabel = Label(self.master, width=2,  bg = 'antique white')
        self.lnlabel.pack(side=LEFT, anchor='nw', fill=Y)
        self.lnlabel1 = Label(self.master,  width=2,  bg = 'antique white')
        self.lnlabel1.pack(side=RIGHT, anchor='nw', fill=Y)
        self.fr = Frame(self.master, bd=2, relief=SUNKEN)
        self.fr.pack(side=LEFT)
        Label(self.fr,  text='           Work Flow           ', fg="orange", font=("Helvetica", 20)).pack() 
        Button(self.fr, text='      From File Menu    ', fg="blue",font=("Helvetica", 15), command=self.combine_funcs(self.CleanTextPad ,self.File_options_Frame,self.FromFileWorkFlow, self.CloseMasterDb, self.PlottBotton_Counter_zeroingDB)).pack(padx=30, pady=10)
        Button(self.fr, text='1       Show Exp. Records      ', fg="light sea green",font=("Helvetica", 15), command =self.combine_funcs( self.ViewDabseTables)).pack( padx=5, pady=2)
        Button(self.fr, text='2  View Raw Data from DataBase ', fg="light sea green",font=("Helvetica", 15), command = self.View_raw_data_from_Dbase).pack( padx=5, pady=2)        
        Button(self.fr, text='3   Import Data to DataBase    ', fg="light sea green",font=("Helvetica", 15), command =self.combine_funcs(self.CleanTextPad, self.Import_to_dbase)).pack( padx=5, pady=2)
        Button(self.fr, text='4  Delete Data from DataBase   ', fg="light sea green",font=("Helvetica", 15), command = self.combine_funcs(self.CleanTextPad, self.Drop_from_dbase)).pack( padx=5, pady=2)
        Button(self.fr, text='5    Give Plotting Samples     ', fg="light sea green",font=("Helvetica", 15), command = self.combine_funcs(self.CleanTextPad, self.PlotDabseTables_bottons, ActivBotton1,)).pack(padx=5, pady=2)
        
        #self.master.mainloop()
    
    
    def Plotting_from_file_bottons(self):
        try:
            if len(self.Start) == 0:
                pass
            elif len(self.Start) != 0:
                filtyp = '.xlsx'
                self.Means, self.Stds, self.time = MainStats(self.directory , filtyp, self.NrExp, self.Col-1, np.array(self.Start), np.array(self.Stop)+1)
                plo(self.Means, self.Stds, self.time)  
        except:
            pass
        
        
    def PLotting_from_dbase_bottons(self):    
        try:
            if len(self.Start) == 0:
                pass
            elif len(self.Start) != 0:
                self.Meanes, self.Stdes, self.time = MainStats_from_Sqlite3(self.Table_name, self.NrExp, self.Col-1, np.array(self.Start), np.array(self.Stop)+1)
                print(self.Meanes, self.Stdes, self.time)
                plo(self.Meanes, self.Stdes, self.time)
#            elif len(self.Meanes[0]) == 0:
#                self.Data_base_options_Frame()
        except:
            pass
            #tkinter.messagebox.showwarning("Plotting From DataBase", "Your Input is Incorrect! Try option 'Give Plotting Samples'!")
            
    
    def _Give_Titel_Xlabel_Ylabel(self):
       
        Titel = simpledialog.askstring("Name prompt", "Enter A Title" )
        Xlabel = simpledialog.askstring("Name prompt", "Lable Xaxis" )
        Ylabel = simpledialog.askstring("Name prompt", "Lable Yaxis" )
        
        return Titel, Xlabel, Ylabel
   
    
    def PLotTetxs_file(self):
        self.Titel, self.Xlabel, self.Ylabel = self._Give_Titel_Xlabel_Ylabel()
        filtyp = '.xlsx'
        self.Means, self.Stds, self.time = MainStats(self.directory , filtyp, self.NrExp, self.Col-1, np.array(self.Start), np.array(self.Stop)+1)
        plo(self.Means, self.Stds, self.time, self.Titel, self.Xlabel, self.Ylabel)
        
    def Plotexts_dbase(self):
        self.Titel, self.Xlabel, self.Ylabel = self._Give_Titel_Xlabel_Ylabel()
        self.Means, self.Stds, self.time = MainStats_from_Sqlite3(self.Table_name, self.NrExp, self.Col-1, np.array(self.Start), np.array(self.Stop)+1)
        plo(self.Means, self.Stds, self.time, self.Titel, self.Xlabel, self.Ylabel)
        
    def combine_funcs(self, *funcs):
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func
        


    def Convertera_Files(self):
        convert= Converter()
        suported_formats = convert.Supported_Files()
        
        try:
            self.directory = filedialog.askopenfilename(defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
            if self.directory == "": # If no file chosen.
                tkinter.messagebox.showwarning("showwarning", "Directory Not Found!")
                pass
            elif self.directory != "":
                tkinter.messagebox.showinfo(title = 'Converter',message = 'Directory Found! Next Step; Add Samples' ) 
                #while True:
                try:    
                    From = simpledialog.askstring("From File Type", "From What  type of file do you whant to convert: exel, csv  or type 'quit' to exit" , initialvalue='excel')
                    if From == 'quit':
                        pass
                    elif From in suported_formats: 
                        To =   simpledialog.askstring("To File Type", "To What  type of file do you whant to convert: exel, csv" , initialvalue='csv')
                        if To == 'quit':
                            pass
                        elif To in suported_formats:
                            Main_Converter(From, To, self.directory)
                            tkinter.messagebox.showinfo(title = 'Converter',message = 'Files Converted! You find them in the '+ str(To) + '_files folder in the given directory' ) 
                            pass
                        else:
                            tkinter.messagebox.showwarning("showwarning", "To File Type Not Supported!")
                            
                    else:
                        tkinter.messagebox.showwarning("showwarning", "To File Type Not Supported!")        
                    
                except:
                    pass
        except:
            pass
            
                
        
    #Defining save method
    def save(self):
            try:
                f = open(self.filename, 'w')
                letter = self.textPad.get(1.0, 'end')
                f.write(letter)
                f.close()
            except:
                save_as()
                
                
    #Defining save_as method
    def save_as(self):
        try:
            # Getting a filename to save the file.
            self.f = filedialog.asksaveasfilename(initialfile='Untitled.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
            fh = open(self.f, 'w')           
            textoutput = self.textPad.get(0.0, END)
            fh.write(textoutput)              
            fh.close()     			  
            self.root.title(os.path.basename(self.f) + " - pyPad") # Setting the title of the root widget.
        except:
            pass
    
    #########################################################################
    #demo of indexing and tagging features of text widget
    
    def select_all(self):
            self.textPad.tag_add('sel', '1.0', 'end')
            
    
    def CleanTextPad(self):
        self.textPad.delete(1.0,END)
           
    ########################################################################
    #Levaraging built in text widget functionalities
    
    def undo(self):
        self.textPad.event_generate("<<Undo>>")
        
    def redo(self):
        self.textPad.event_generate("<<Redo>>")
        
        
    def cut(self):
        self.textPad.event_generate("<<Cut>>")
        
    def copy(self):
        self.textPad.event_generate("<<Copy>>")
        
    def paste(self):
        self.textPad.event_generate("<<Paste>>")
        
    def WelcomeMessage(self):
        
        self.textPad.delete(1.0,END)         
        fh = open('Navigation_to_the User_texts/WelcomeText.txt',"r")        
        self.Add_to_Text_pad(fh.read())
        fh.close()
        
        
    def FromFileWorkFlow(self):
        self.textPad.delete(1.0,END)         
        fh = open('Navigation_to_the User_texts/FromFileWorkFlow.txt',"r")        
        self.Add_to_Text_pad(fh.read())
        fh.close()
        
        
    def FromDataBaseWorkFlow(self):
        self.textPad.delete(1.0,END)         
        fh = open('Navigation_to_the User_texts/FromDataBaseWorkFlow.txt',"r")        
        self.Add_to_Text_pad(fh.read())
        fh.close()
    ##################################################################
    
    ######################################################################
    def center_window(self, masters, width=300, height=200, a=2, b=2, c=2, d=2):
        # get screen width and height
        screen_width = masters.winfo_screenwidth()
        screen_height = masters.winfo_screenheight()
    
        # calculate position x and y coordinates
        x = (screen_width/a) - (width/b)
        y = (screen_height/c) - (height/d)
        masters.geometry('%dx%d+%d+%d' % (width, height, x, y))
        
    def App(self):
        self.root = Tk()
        #self.root.geometry('980x850')
        self.center_window(self.root, 980, 850, 1.5, 2, 2, 2)
        self.root.title("BioWells")
        
        if "nt" == os.name:
            self.root.wm_iconbitmap(bitmap = "96wellsystem.ico")
        else:
            self.root.wm_iconbitmap(bitmap = "@96wellsystem.xbm")
        
        #defining icons for compund menu demonstration
        self.newicon = PhotoImage(file='icons/new_file.gif')
        self.openicon = PhotoImage(file='icons/open_file.gif')
        self.saveicon = PhotoImage(file='icons/save.gif')
        self.cuticon = PhotoImage(file='icons/cut.gif')
        self.copyicon = PhotoImage(file='icons/copy.gif')
        self.pasteicon = PhotoImage(file='icons/paste.gif')
        self.undoicon = PhotoImage(file='icons/undo.gif')
        self.redoicon = PhotoImage(file='icons/redo.gif')
        self.menubar = Menu(self.root)
        
        # File menu,for open,save,save as and quit       
        self.filemenu = Menu(self.menubar, tearoff=0 ) 
        #filemenu.add_command(label="New", accelerator='Ctrl+N', compound=LEFT, image=newicon, underline=0, command=new_file  )
        self.filemenu.add_command(label="Open", accelerator='Ctrl+O', compound=LEFT, image=self.openicon, underline =0, command=self.open_file)
        self.filemenu.add_command(label="Open Excel", accelerator='Ctrl+E', compound=LEFT, image=self.openicon, underline =0, command=self.openExcel)
        self.filemenu.add_command(label="Save", accelerator='Ctrl+S',compound=LEFT, image=self.saveicon,underline=0, command=self.save_as)
        self.filemenu.add_command(label="New", accelerator='Ctrl+N',compound=LEFT, image=self.newicon,underline=0, command=self.new_file)
        #self.filemenu.add_command(label="Save as",accelerator='Shift+Ctrl+S',  command=self.save_as)
        #filemenu.add_command(label="Excel_to_sqlite",accelerator='Shift+Ctrl+P', command=ExceltoPandas)
        self.filemenu.add_separator()        
        self.filemenu.add_command(label="Exit", accelerator='Alt+F4') 
        self.menubar.add_cascade(label="File", menu=self.filemenu)  
        
        
        #Edit menu - Undo, Redo, Cut, Copy and Paste 
        self.editmenu = Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Undo",compound=LEFT,  image=self.undoicon, accelerator='Ctrl+Z', command=self.undo)
        self.editmenu.add_command(label="Redo",compound=LEFT,  image=self.redoicon, accelerator='Ctrl+Y', command=self.redo)
        self.editmenu.add_separator() 
        self.editmenu.add_command(label="Cut", compound=LEFT, image=self.cuticon, accelerator='Ctrl+X', command=self.cut)
        self.editmenu.add_command(label="Copy", compound=LEFT, image=self.copyicon,  accelerator='Ctrl+C', command=self.copy)
        self.editmenu.add_command(label="Paste",compound=LEFT, image=self.pasteicon, accelerator='Ctrl+V', command = self.paste)
        self.editmenu.add_separator()
        #editmenu.add_command(label="Find",underline= 0, accelerator='Ctrl+F', command=on_find)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Select All", underline=7, accelerator='Ctrl+A', command=self.select_all)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        
        self.root.config(menu=self.menubar)
        
        
        
        # Adding top label to hold and left labels
        # we have colored it for now to differentiate it from the main window
        
        
        self.shortcutbar = Frame(self.root,  height=25, bg='light sea green')
        self.shortcutbar.pack(expand=NO, fill=X)
        self.lnlabel = Label(self.root,  width=2,  bg = 'antique white')
        self.lnlabel.pack(side=LEFT, anchor='nw', fill=Y)
        
        
        #
        # Adding Text Widget & ScrollBar widget
        #
        
        self.textPad = Text(self.root, undo=True)
        self.textPad.pack(expand=YES, fill=BOTH)
        self.scroll=Scrollbar(self.textPad)
        self.textPad.configure(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.textPad.yview)
        self.scroll.pack(side=RIGHT,fill=Y)
        
        self.myframe1 = Frame(self.root, bd=2, relief=SUNKEN)
        self.myframe1.pack(side=LEFT)
        
        # add label to to myframe1
        Label(self.myframe1, text=' Choose Option', fg="orange", font=("Helvetica", 20)).pack()
        
        
        #add button widget to myframe1
        Button(self.myframe1, text='      From File Menu    ', fg="light sea green",font=("Helvetica", 15), command=self.combine_funcs(self.CleanTextPad ,self.File_options_Frame,self.FromFileWorkFlow, self.CloseMasterDb)).pack(padx=30, pady=10)
        Button(self.myframe1, text='    From DataBase Menu  ', fg="light sea green",font=("Helvetica", 15), command = self.combine_funcs(self.CleanTextPad ,self.Data_base_options_Frame, self.FromDataBaseWorkFlow, self.CloseMasterFile)).pack(padx=30, pady=10)
        Button(self.myframe1, text='      File Converter    ', fg="light sea green",font=("Helvetica", 15),command=self.Convertera_Files).pack(padx=30, pady=10)

        
        self.myframe2 = Frame(self.root, bd=2, relief=GROOVE, bg='antique white')
        self.myframe2.pack(side=RIGHT)
        
        #add Photimage Class Widget to myframe2
        Label(self.myframe2,fg="light sea green", text='                     Welcome to BioWells                    ', bg='antique white', font=("Helvetica", 20)).pack()
        self.photo = PhotoImage(file='backgroundwithgrasses.gif',width=550, height=520)
        self.label = Label(self.myframe2,compound = CENTER,  image=self.photo)
        self.label.image = self.photo # keep a reference!
        
        
        self.label.pack()
        
        self.WelcomeMessage()
        
        #self.root.attributes("-topmost", True)
        self.root.lift()
        self.root.mainloop()
        
        
    def Gui_close(self): 
        if self.added_Samples == True :
            self.root.quit()
            self.added_Samples = False
        elif self.added_Samples == False:
            tkinter.messagebox.showwarning("Plot Samples", "No samples are given! Chose option 'Plot Additional Samples' first!") 
            self.added_Samples = True
  
            
        else:
            pass
         

        
      


inter = GUI()
inter.App()