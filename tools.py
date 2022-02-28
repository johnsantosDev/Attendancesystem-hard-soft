"""
ATTENDANCE SYSTEM : LOGIN SYSTEM
Author :
"""
import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime, date
import sqlite3 as SQL
import mysql.connector
maFonte2 = ('Century Gothic',12)


class BindedEntry2:
    def __init__(self, entryW, text):
        self.entryW = entryW
        self.text = text
        self.entryW.bind('<Enter>',self.setfree)
        self.entryW.bind('<Leave>',self.leave)
    def setfree(self,event):
        self.entryW.delete(0,tk.END)
        self.entryW.focus()
    def thenpass(self,event):
        if self.entryW.get()=="":
            self.entryW.insert(0,self.text)
        if self.entryW.get()==self.text :
            self.entryW.delete(0,tk.END)
            self.entryW.focus()
    def leave(self,event):
        self.entryW.bind('<Enter>',self.thenpass)
        if self.entryW.get()=="":
            self.entryW.insert(0,self.text)
        else:pass
class progress:
    def __init__(self, progresser, container, level=0):
        if level==0:
            progresser['value'] = 0    
            container.update_idletasks()     
            time.sleep(0.1)
        if level==20:
            progresser['value'] = 5    
            container.update_idletasks()     
            time.sleep(0.1)
            progresser['value'] = 15    
            container.update_idletasks()     
            time.sleep(0.1)
            progresser['value'] = 20
        elif level==40:
            progresser['value'] = 25    
            container.update_idletasks()         
            time.sleep(0.1)
            progresser['value'] = 40 
        elif level==60:
            progresser['value'] = 45    
            container.update_idletasks()     
            time.sleep(0.1)
            progresser['value'] = 55    
            container.update_idletasks()     
            time.sleep(0.1)
            progresser['value'] = 60 
        elif level==80:
            progresser['value'] = 65    
            container.update_idletasks()     
            time.sleep(0.1)
            progresser['value'] = 70    
            container.update_idletasks()     
            time.sleep(0.1)
            progresser['value'] = 75    
            container.update_idletasks()     
            time.sleep(0.1)
            progresser['value'] = 80
        elif level==100:
            progresser['value'] = 85    
            container.update_idletasks()     
            time.sleep(0.1)
            progresser['value'] = 95    
            container.update_idletasks()     
            time.sleep(0.1)
            progresser['value'] = 100 
            time.sleep(0.1)
            progresser['value'] = 0 
def sendtoDatabase(UID):
	#"""This class send data collected from arduino to the database"""
    dby = time.strftime("%Y")
    dbfile = f"database/PRESENCES_{dby}.db"
    date_ = time.strftime("%B%d")
    date_ = str(date_)
    datetime_ = datetime.now()
    connexion = SQL.connect(dbfile)
    cursor = connexion.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS " + date_ + " (ID INTEGER PRIMARY KEY AUTOINCREMENT,studentName TEXT NOT NULL, studentID INT NOT NULL, Arriving TEXT, Leaving TEXT)")
    connexion.commit()
    squery = 'SELECT * FROM '+date_+' WHERE studentID =?'
    cursor.execute(squery, [UID])
    record = cursor.fetchall()
    if record:
        #Leaving Time updated...
        uquery = 'UPDATE '+date_+' SET Leaving =? where studentID =?'
        cursor.execute(uquery, [datetime_,UID])
        connexion.commit()
        print("Updated Leaving time")
    else :
        #insert Name,UID,Arriving...
        newdb = SQL.connect("database/STUDENTLIST.db")
        cursor = newdb.cursor()
        squery = f'SELECT * FROM LIST where studentID =?'
        cursor.execute(squery, [UID])
        found = cursor.fetchall()
        if found :
            name = found[0][1]
            cursor = connexion.cursor()
            iquery = f'INSERT INTO '+date_+' (studentName, studentID,Arriving,Leaving)VALUES (?,?,?,?)'
            cursor.execute(iquery, [name,UID,datetime_," "])
            connexion.commit()
            print("Updated for Arriving time")
        else :
            print("[ERROR] : Student with ID : [", iD, "] not found")
def showSpecificDate(mainframe, title,dateString, year, x):
	title.config(text="\tN°\t\tSTUDENT NAMES\t\t  STUDENT ID\t\t  IN TIME\t\t  OUT TIME\t\t\t-")
	main=tk.LabelFrame(mainframe,height=x,width=x,font=maFonte2,bg="white")
	main.place(x=5, y=5)
	cframe=tk.LabelFrame(main, height=1000000, width=x,font=maFonte2,bg="white")
	cframe.place(x=5, y=5)
	dbfile = f"database/PRESENCES_{year}.db"
	connexion = SQL.connect(dbfile)
	cursor = connexion.cursor()
	cursor.execute(f'SELECT * FROM '+dateString+'')
	lst = cursor.fetchall()
	if len(lst)>0:
		total_rows = len(lst)
		total_columns = len(lst[0]) 
		for i in range(total_rows):
			for j in range(total_columns):
				e =tk.Entry(cframe, bg="#f4f7fa", width=22, fg='green',
					font=('Arial',15))
				e.grid(row=i, column=j)
				e.insert(tk.END, lst[i][j]) 		
	else:
		print(f"[DB ERROR] : database {dbfile} is empty")


#sendtoDatabase("480918906")      
        
