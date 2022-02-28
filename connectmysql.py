"""
ATTENDANCE SYSTEM : DATABASE & GUI MANAGMENT SYSTEM
Author : JOHN SANTOS
"""
#import serial
import sqlite3 as SQL
import time
from datetime import date
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tools
import mysql.connector

maFonte2 = ('Century Gothic',12)
def sendtoDatabase(string):
	"""This class send data collected from arduino to the database"""
	UID = string
	dbmy = time.strftime("%B-%Y")
	dbfile = f"database/PRESENCE {dbmy}.db"
	date_ = time.strftime("%B")
	datetime_ = datetime.now()
	#127.0.0.0 or localhost
	try :
		connexion = mysql.connector.connect(host='127.0.0.1',
	                                         database=dbfile,
	                                         user='santos',
	                                         password='santos1234')
		mySqlCTable = """CREATE TABLE IF NOT EXISTS {date_} (ID INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,studentName TEXT NOT NULL, studentID TEXT NOT NULL, Arriving TEXT, Leaving TEXT"""
		cursor = connexion.cursor()
		result = cursor.execute(mySqlCTable)
		try :
			sql_squery = f"""select Leaving from {date_} where studentID = %s"""
			cursor.execute(sql_squery, (UID,))
			record = cursor.fetchall()
			if record :
				#Leaving Time updated...
				sql_uquery = f"""UPDATE {date_} set Leaving = %s where studentID = %s"""
				inputs = (datetime_,UID)
				cursor.execute(sql_uquery, inputs)
				connexion.commit()
			else :
				#insert Name,UID,Arriving...
				mySql_iquery = f"""INSERT INTO {date_} (studentName, studentID,Arriving,Leaving)VALUES (%s, %s, %s, %s)"""
				recordall = (name,UID,datetime_," ")
				cursor.execute(mySql_iquery, recordall)
				connexion.commit()	
		except mysql.connector.Error as error:
			messagebox.showwarning("Warning db", 
				"Failed to update data in MySQL: {}".format(error))
		finally:
			cursor.close()



	except mysql.connector.Error as error :
		messagebox.showwarning("Warning db", 
		"Failed to create table in MySQL : {}".format(error))
	finally:
	    if (connexion.is_connected()):
	        cursor.close()
	        connexion.close()


def show_studentDetails(data, scrf):
	cframe=tk.LabelFrame(scrf,font=maFonte2,bg="white")
	cframe.place(x=5, y=5)
	dbfile = f"database/STUDENTLIST.db"
	iD = data
	connexion = mysql.connector.connect(host='127.0.0.1',user='johnsantos',
                                       database=f'{dbfile}',password='johnsantos123456789')
	cursor = connexion.cursor()
	try :
		squery = """SELECT * FROM {dbfile} WHERE studentID = %s"""
		cursor.execute(squery, (iD,))
		lst = cursor.fetchall()
		if len(lst)>0:
			total_rows = len(lst)
			total_columns = len(lst[0]) 
			for i in range(total_rows):
				for j in range(total_columns):
					self.e =tk.Entry(cframe, bg="#f4f7fa", width=20, fg='green',
						font=('Arial',14))
					self.e.grid(row=i, column=j)
					self.e.insert(tk.END, lst[i][j]) 		
		else:
			messagebox.showinfo("DB ERROR", 
				"student not found")
	except :
		messagebox.showerror("DB ERROR", 
			"unable to show student data")
	finally :
		cursor.close()

def chech_newStudent(data, iDEnt):
	lab1.config(state=tk.NORMAL)
	lab1.delete(0,tk.END)
	lab1.insert(0,data)
	lab1.config(state=tk.DISABLED)
def ReadfromArduino(scrf, arduino, iDEnt):
	def count():
		try :
			data = arduino.readline()
			print("readfinished...")
			data = str(data)
			sendtoDatabase(data)
			check_newStudent(data, idEnt)
			show_studentDetails(data, scrf)
			tools.progress(progb, root,20)
			tools.progress(progb, root,100)
			try :
				sendtoDatabase(data)
				check_newStudent(data,iDEnt)
				show_studentDetails(data, scrf)
				tools.progress(progb, root,20)
				tools.progress(progb, root,100)
			except:
				messagebox.showerror("DB ERROR", "Error Updating on database")
		except:
			#print("processing...")
			tools.progress(progb, root,0)
		scrf.after(1000, count)
	count()

class Application:
	def __init__(self, root, com):
		#parameters
		self.COM = "COM"+com
		scx=int(root.winfo_screenwidth())
		scy=int(root.winfo_screenheight())
		geo=f"{scx}x{scy}+0+0"
		root.geometry(geo)
		root.title("ATTENDANCE SYSTEM")
		root.config(bg="#d4dde8")
		self.cont = tk.Frame(root, width=scx, height=scy, bg="#d4dde8")
		self.cont.place(x=1,y=1)
		#parameters 
		thedate = date.today()
		dbmy = time.strftime("%B-%Y")
		dbfile = f"database/PRESENCE {dbmy}.db"
		connexion = SQL.connect(dbfile)
		cursor = connexion.cursor()
		


		frame1 = tk.Frame(self.cont, width=scx-20, height=scy/6,bg="#d4dde8")
		frame1.place(x=10,y=10)

		self.btnframe = tk.LabelFrame(frame1, text="Control Pannel", 
			width=650, height=110, bg="#d4dde8", fg="blue")
		self.btnframe.pack(side=tk.LEFT, padx=5)#place(x=scx/2, y=5)
		ent1 =ttk.Entry(self.btnframe, width=15,font=('',26))
		ent1.place(x=20,y=5)
		ent1.insert(0, "Student ID here")
		tools.BindedEntry2(ent1,"Student ID here")

		searchbtn = ttk.Button(self.btnframe,
			text= "Show Student", 
			command = lambda:show_studentDetails(iDentry.get(), self.scrf))
		searchbtn.place(x=20,y=60)
		viewbtn = ttk.Button(self.btnframe,
			text= "Delete Student", command = self.deleteStudent)
		viewbtn.place(x=115,y=60)
		delbtn = ttk.Button(self.btnframe,
			text= "View All Students", command=self.viewAllStudents)
		delbtn.place(x=210,y=60)
		self.inA = tk.Entry(self.btnframe, width=15, font=maFonte2)
		self.inA.place(x=340, y=5)
		self.inA.insert(0,"In start-time")
		tools.BindedEntry2(self.inA, "In start-time")
		self.inB = tk.Entry(self.btnframe, width=15, font=maFonte2)
		self.inB.place(x=340, y=35)
		self.inB.insert(0,"Out start-time")
		tools.BindedEntry2(self.inB, "Out start-time")
		self.outA = tk.Entry(self.btnframe, width=15, font=maFonte2)
		self.outA.place(x=490, y=5)
		self.outA.insert(0,"In end-time")
		tools.BindedEntry2(self.outA, "In end-time")
		self.outB = tk.Entry(self.btnframe, width=15, font=maFonte2)
		self.outB.place(x=490, y=35)
		self.outB.insert(0,"Out end-time")
		tools.BindedEntry2(self.outB, "Out end-time")
		parambtn = ttk.Button(self.btnframe,
			text= "Save Time", command = self.settings)
		parambtn.place(x=555,y=65)
		self.newcard = tk.LabelFrame(frame1, text="New Student Registration", 
			width=650, height=110, bg="#d4dde8", fg="blue")
		self.newcard.pack(side=tk.LEFT, padx=5)#place(x=scx/2, y=5)
		iDentry_ = tk.Label(self.newcard, font=maFonte2,
			text="New Student ID", bg="#d4dde8").place(x=2,y=2)
		self.iDentry = ttk.Entry(self.newcard, 
			font = maFonte2, width=25)
		self.iDentry.insert(0,"2242424242142")
		self.iDentry.config(state=tk.DISABLED)
		self.iDentry.place(x=140,y=2)
		Namentry_ = tk.Label(self.newcard, font=maFonte2, 
			text="Student Names", bg="#d4dde8").place(x=2,y=35)
		self.Namentry = ttk.Entry(self.newcard,
			font = maFonte2, width=25)
		self.Namentry.place(x=140,y=35)
		Classentry_ = tk.Label(self.newcard, font=maFonte2, 
			text="Student Classe", bg="#d4dde8").place(x=380,y=2)
		self.Classentry = ttk.Entry(self.newcard,
			font = maFonte2,width=12)
		self.Classentry.place(x=510,y=2)
		Sexentry_ = tk.Label(self.newcard, font=maFonte2, 
			text="Student Gender", bg="#d4dde8").place(x=380,y=35)
		self.Sexentry = ttk.Combobox(self.newcard,values=["Male", "Female"],
			font = maFonte2, width=10)
		self.Sexentry.current(0)
		self.Sexentry.place(x=510,y=35)
		save = ttk.Button(self.newcard, text="Save Student", 
			command=self.saveStudent)
		save.place(x=545,y=65)

		frame2 = tk.LabelFrame(self.cont, text="View data", 
			width=scx-20, height=scy-220, bg="#d4dde8")
		frame2.place(x=10,y=scy/6+10)
		tframe = tk.Frame(frame2, width=scx-20, height=40)
		tframe.place(x=1,y=1)
		tk.Label(tframe, fg="white", bg="#08246b", font=('Century Gothic',14,'bold'),
			text="N°\tSTUDENT NAMES\t\t\t\tSTUDENT ID\t\tCLASS\t\tARRIVING\t\tLEAVING").pack(side=tk.LEFT,fill=tk.BOTH)
	
		container = tk.LabelFrame(frame2, width=scx-50, height=scy-330,
			relief = tk.GROOVE)
		canvas = tk.Canvas(container, bg="white", width=scx-50, height=scy-330)
		scrollbar = ttk.Scrollbar(container, orient="vertical", 
			command=canvas.yview)
		self.scrf = tk.Frame(canvas, bg="white", width=scx-50, height=scy-330)
		self.scrf.bind(
		    "<Configure>",
		    lambda e: canvas.configure(
		        scrollregion=canvas.bbox("all")
		    )
		)
		scrollbar.pack(side="right", fill="y")
		canvas.create_window((0, 0), window=self.scrf, anchor="nw")
		canvas.configure(yscrollcommand=scrollbar.set)
		container.place(x=1,y=50)
		canvas.pack(side="left", fill="both", expand=True)
		
		progb = ttk.Progressbar(root, orient = tk.HORIZONTAL,length = scx/2, mode = 'determinate')
		progb.place(x=scx/4,y=scy/6-5)	
		tools.progress(progb, root,20)
		tools.progress(progb, root,100)
		liste = open("files/ALLID.txt").read()
		#here we prompt the user to transfer data from Arduino to the server(our PC Actually) by serial communication"""
		try :
			arduino = serial.Serial(self.COM, 9600, timeout=.1)
			if self.readarduino == True :
				arduino.write(liste)
				ReadfromArduino(self.scrf, arduino,self.iDentry)
			else :
				arduino.write("systemleep")
		except :
			messagebox.showerror("ARDUINO ERROR",
				f"Error connecting to Arduino port {self.COM} please "
				"verify the com selected in your Arduino IDE,"
				" or close connexion and start again")
	def saveStudent(self):
		"""This function register a new student and save his data in the db for next attendance"""
		iD = self.iDentry.get()
		open("files/ALLID.txt",'w+').write(f",{iD}")
		name = self.Namentry.get()
		Class = self.Classentry.get()
		Gender = self.Sexentry.get()
		dbfile = "STUDENTLIST"
		#cursor.execute(f'create database {dbfile}')
		try :
			connexion = mysql.connector.connect(host='127.0.0.1', user='johnsantos',
	                                        database=f'{dbfile}',password='johnsantos123456789')
			mySqlCTable = f"""CREATE TABLE {dbfile}.LIST (ID INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,studentName VARCHAR(50) NOT NULL, studentID INT(15) NOT NULL TEXT, Gender TEXT, Class TEXT"""
			cursor = connexion.cursor()
			result = cursor.execute(mySqlCTable)
			try:
				mySql_iquery = """INSERT INTO LIST (studentName, studentID,Gender,Class)VALUES (%s, %s, %s, %s)"""
				recordall = (name,iD,Gender,Class)
				cursor.execute(mySql_iquery, recordall)
				connexion.commit()
				print("done")
			except Error as error:
				messagebox.showerror("Table Error", 
					f"Unable to insert Student data in table : \nError details:{error}")
		except mysql.connector.Error as error :
			messagebox.showerror("Table Error", 
				f"Unable to create table : \nError details:{error}")
		finally:
		    cursor.close()
		    connexion.close()
	
	def deleteStudent(self):
		iD = self.iDentry.get()
		dbfile = f"database/STUDENTLIST.db"
		connexion = mysql.connector.connect(host='127.0.0.1',user='johnsantos',
	                                    database=f'{dbfile}',password='johnsantos123456789')
		cursor = connexion.cursor()
		try :
			dquery = """DELETE * FROM {dbfile} WHERE studentID = %s"""
			cursor.execute(dquery, (iD,))
			result = cursor.fetchall()
			if result :
				messagebox.showinfo("Delete Student", 
					f"student with ID : {iD} has been successfully deleted ")
			else :
				messagebox.showerror("Delete Student", 
					f"ID : {iD} not found...")
		except :
			messagebox.showerror("Delete Student", 
				f"unable to make delete operation for ID : {iD}")
		finally:
			cursor.close()

	def viewAllStudents(self):
		cframe=tk.LabelFrame(self.scrf, font=maFonte2,bg="white")
		cframe.place(x=5, y=5)
		dbfile = f"STUDENTLIST.db"
		connexion = mysql.connector.connect(host='127.0.0.1',user='johnsantos',
	                                       database=f'{dbfile}',password='johnsantos123456789')
		cursor = connexion.cursor()
		try :
			cursor.execute("""SELECT * FROM {dbfile}""")
			lst = cursor.fetchall()
			if len(lst)>0:
				total_rows = len(lst)
				total_columns = len(lst[0]) 
				for i in range(total_rows):
					for j in range(total_columns):
						self.e =tk.Entry(cframe, bg="#f4f7fa", width=20, fg='green',
							font=('Arial',14))
						self.e.grid(row=i, column=j)
						self.e.insert(tk.END, lst[i][j]) 		
			else:
				messagebox.showerror("DB ERROR", 
					"database is empty")
		except :
			messagebox.showerror("DB ERROR", 
				"unable to show database data")
		finally :
			cursor.close()
	def settings(self):
		inA = self.inA.get()
		inB = self.inB.get()
		outA = self.outA.get()
		outB = self.outB.get()
		if time.time() in range(inA,inB) or time.time() in range(outA,outB):
			self.readarduino = True
		else:
			self.readarduino = False




	