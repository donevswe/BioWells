# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 00:01:57 2015

@author: ev
"""

from tkinter import *
import os



class BottonWells():
    """In this class is created a tkinter GUI that is representing 96 well plate . Here are used many diferent loops and conditions for the user to be able to navigate
        more easy. Some of them can be harsh at a first glance since I have done it little by ittle during a mounth. And sometimes eve I have difficulties to remmember 
        what I did.
    """
    
    
    def __init__(self, exper =3 ):
        """As usual we determain soe variables need"""
        

        self.r_list=[]
        
        self.exper = exper
        self.ind_colors= False
        
        #self.Col = None
        self.Col = -1
        self.Col1 = -1
        self.yellow_push = False
        self.pushed ={}   # a dictionar that collect which bottons the user have pushed. It will help us keeping track that the uer do not push more than twice certain botton
        for i in range(8):
            for j in range(1,14):
                self.pushed[str(i) + str(j)]= -1  # in tota we got 96 bottons
                
        self.new_color = 'light sea green'   # this will be the original color when the program starts to every botton
        self.pushed_column_list = []
 
 
    def create_bottom_pad(self):
        """This method creates the wells """
        
        Rows = list('ABCDEFGH')   # rows 
        c = 13   # columns 1-13 total of  12
        _frame = Frame(self.roo)    # creating a frame
        _frame.grid(row=10, column=6,sticky=W+E+N+S, padx=15, pady=2)   # some technicalities about size and shape. Usualy does ot make sence
        self.button = [[0 for x in range(c+1)] for x in range(8)]   # creating 96 bottons
        for i in range(8):
            for j in range(1,c+1):     # give them some properties such as text and color 
                
                color = 'white' if j == 1 else self.new_color
                text = Rows[i]+'  '+str(i+1) if j==1 else '' 
                #text = 'col' if j==0 else +1'' 
                self.button[i][j] = Button(_frame,text =  text , bg=color, width=3, command=self.button_clicked(i,j))
                self.button[i][j].grid(row=i, column=j)


    def create_top_bar(self):
        '''creating top buttons representing the columns. THe idea is the same as the previous method'''
        c = 12
        topbar_frame = Frame(self.roo)
        topbar_frame.config(height=25)
        topbar_frame.grid(row=0, columnspan=15, rowspan=10, padx=7, pady=5)
        self.buttons = [0 for x in range(c+1)]
        color = 'white'
        for jj in range(13):
            text = ' ' if jj==0 else 'C'+str(jj)
            self.buttons[jj] = Button(topbar_frame,text= text , bg=color, width=3, command = self.askCol(jj))
            self.buttons[jj].grid(row=0, column=jj)
            
            
    def askCol(self,jj):
        """THis method check if the user click on the top level columns and if it pushed choose all wells from that column as pushed"""
        
        def col():
            #global col
            if jj == 0:  # it is the very first botton when puhed the program does not give anything
                pass

                    
            else:
                btn=self.buttons[jj]
                new_color = 'red'    # otherwise the whole column becmes red
                btn.config(bg=new_color)
                for i in range(0,8):
                    btn1 = self.button[i][jj+1]
                    btn1.config(bg=new_color)
                            
                self.Col = jj
                self.r_list=[0,7]  # assigning wells start stop and column for the stats class later
                print(self.Col)
                return self.Col
        
        return col
        
    def button_clicked(self,i,j):        # here is many things and contidions we leave the exanation fo anaother time
            def callback():
                if j == 1:
                    print('This is not a well')
                else:
                
                    if self.yellow_push == False:
                        for ii in range(0,8):                  
                            btn1 = self.button[ii][j]
                            btn1.config(bg='orange')
                            self.YellowPush()
                    if self.Pushed()  == True:
                        
                        self.Close()
                        
                    else:
                        btn = self.button[i][j]
                        
                        self.r_list.append(i)
                        if self.pushed[str(i) + str(j)] == -1 and self.ind_colors == False:                       
                           self.new_color = 'green'
                           self.chngeColorMOde()    
                           btn.config(bg=self.new_color)
                           self.PushedBotton(i,j)
                           self.Same_Coloum_Pushed_Wells(j)
                                
                                
                        elif self.pushed[str(i) + str(j)] == -1 and self.ind_colors == True:                     
                            self.new_color = 'red'
                            self.chngeColorMOde()    
                            btn.config(bg=self.new_color)
                            self.PushedBotton(i,j)
                            self.Same_Coloum_Pushed_Wells(j)
                            
                        elif self.pushed[str(i) + str(j)] == 1 and self.ind_colors == True:                     
                            self.new_color = 'red'
                            self.chngeColorMOde()    
                            btn.config(bg=self.new_color)
                            self.PushedBotton(i,j)
                            self.Same_Coloum_Pushed_Wells(j)
                            
                        else:
                        
                            self.Close()
    
                return self.r_list           
            return callback  
    # the next five methods are use din the method aove checking many difernet things. Like color of a well if it si pushe or not chnging color, which column it belogs to etc.

    def Same_Coloum_Pushed_Wells(self,j):
        self.pushed_column_list.append(j)
        if all(map(lambda x: x == self.pushed_column_list[0], self.pushed_column_list)) == False:
            self.Close()
        else:
            self.Col1 = j

        
    def YellowPush(self):
        
        if self.yellow_push == False:
            self.yellow_push = True
        
            
    
    def PushedBotton(self,i,j):
      self.pushed[str(i) + str(j)] = 1
      self.push_bottom = int(str(i) + str(j))
    

        
    def chngeColorMOde(self):
        if self.ind_colors== False:
            self.ind_colors = True
        else:
            self.ind_colors = False
     
    def Pushed(self):
        if self.Col != -1:
            
            return True
            
        else:
            return False
            
    
    def returnCol(self):
        # returning a column, either from pushing the top botton or by pushing the wells one by one
        if self.Col != -1:
            return self.Col
        elif self.Col1 != -1:
            return self.Col1 -1
            
      
        
    def return_stop_list(self):   # returning the stop list usd by Stats method
        self.stop_list = self.r_list[1::2]
        print(self.stop_list)
        return self.stop_list
        
    def return_start_list(self):     # returning the stop metho used by Stats method
        self.start_list = self.r_list[0::2]
        print(self.start_list)
        return self.start_list
                        
    def app(self):    # building up the tkinter app
        self.roo = Tk()
        #self.roo.geometry('780x400')
        if "nt" == os.name:
            self.roo.wm_iconbitmap(bitmap = "96wellsystem.ico")
        else:
            self.roo.wm_iconbitmap(bitmap = "@96wellsystem.xbm")
        self.roo.title('Navigation 96 Wells')
        self.create_top_bar()
        self.create_bottom_pad()
        
        #self.create_play_bar()
        self.roo.update()
        self.roo.mainloop()
        
    def Close(self):    # method ued to close the aplication. It is used at many places when the user do not use the wells tkiner in a right way
        try:
            self.roo.destroy()
        except:
            pass

class botons:    # finally a class used by the big tkinter 
    def bot(self):
        self.bw = BottonWells()
        self.bw.app()
        start = self.bw.return_start_list()
        stop = self.bw.return_stop_list()
        col = self.bw.returnCol()
        if len(start) > len(stop):   # checking one final time that the start and the stop ist are of the same size
            start = start[:len(start)-1]
            
        return start, stop , col
        
        
    def close(self):
        self.bw.Close()

        
#======================================================================
if __name__ == '__main__':
    bottons = botons()
    start, stop,col1 = bottons.bot()
    print(start, stop,col1)
    

    