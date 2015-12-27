# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 18:19:14 2015

@author: ev
"""
import glob
import os
pat = '/home/ev/Documents/4thBioinformatics/ApplicationsProgrammering/WellsBio/data'
nr_files = len(os.listdir(pat))-2
list_files = [0] * nr_files
for i in range(nr_files):
    Files = glob.glob(pat + "/*_"+ str(i)+".xlsx")
    for File in Files:
        File= File.split('/')    
        File = "/".join(File[-1:])  
    
        list_files[i] = File
print(list_files)


    


def Name_to_file(path_from_file):
    path= path_from_file.split('/')    
    path = "/".join(path[-1:]) 
    name_to_file = path.split('.')
    return name_to_file[0]



Files = glob.glob(pat + "/*_"+ '*'+".xlsx")

print(Files)


from tkinter import filedialog
a = filedialog.askdirectory()
b = filedialog.askopenfilename()