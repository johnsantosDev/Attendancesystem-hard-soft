import manage

"""
ATTENDANCE SYSTEM : DATABASE & GUI MANAGMENT SYSTEM
Author :
"""
#import serial
import sqlite3 as SQL
import time
from datetime import datetime,date
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tools
import mysql.connector
import serial #for arduino series communication(usb)

import link #local module
maFonte2 = ('Century Gothic',12)


out = "OFF"
iN = "ONN"
state = "incounting"
callresetArduino=False
presences = []

def show_studentDetails(serialdata,iD, scrf, x, title, now):
	"""This function show all details related to the student ID"""
	main=tk.LabelFrame(scrf,height=x,width=x,font=maFonte2,bg="white")
	main.place(x=5, y=5)
	cframe=tk.LabelFrame(main,height=1000000,width=x,font=maFonte2,bg="white")
	cframe.place(x=2, y=2)
	dbfile = f"database/STUDENTLIST.db"
	connexion = SQL.connect(dbfile)
	cursor = connexion.cursor()
	if serialdata==True :
		#if len(presences)>0:
		title.config(text="\tSTUDENT NAMES\t\t  STUDENT ID\t\t  GENDER\t\t  CLASS\t\t  TIME\t\t\t")
		squery = 'SELECT * FROM LIST WHERE studentID =?'
		cursor.execute(squery, [iD])
		student = cursor.fetchall()
		if student :
			k_list = (student[0][1],student[0][2],student[0][3],student[0][4],str(now))
			presences.append(k_list)
		if len(presences)>0:
			main=tk.LabelFrame(scrf,height=x,width=x,font=maFonte2,bg="white")
			main.place(x=5, y=5)
			cframe=tk.LabelFrame(main,height=1000000,width=x,font=maFonte2,bg="white")
			cframe.place(x=2, y=2)
			total_rows = len(presences)
			total_columns = len(presences[0])
			for i in range(total_rows):
				for j in range(total_columns):
					e =tk.Entry(cframe, bg="#f4f7fa", width=22, fg='green',
						font=('Arial',14))
					e.grid(row=i, column=j)
					e.insert(tk.END, presences[i][j])
	else :
		title.config(text="\tN°\t\tSTUDENT NAMES\t\t  STUDENT ID\t\t  GENDER\t\t  CLASS\t\t\t\t-")
		try :
			squery = 'SELECT * FROM LIST WHERE studentID =?'
			cursor.execute(squery, [iD])
			lst = cursor.fetchall()
			if len(lst)>0:
				total_rows = len(lst)
				total_columns = len(lst[0]) 
				for i in range(total_rows):
					for j in range(total_columns):
						e =tk.Entry(cframe, bg="#f4f7fa", width=22, fg='green',
							font=('Arial',14))
						e.grid(row=i, column=j)
						e.insert(tk.END, lst[i][j]) 		
			else: 
				print("Unable to show student details... : ", iD)
		except :
			print("unable to open students database for operation : ", iD)
def settings(timeN, inA,inB,outA,outB):
	"""This function define the in  and out time range for starting and closing attendance"""
	readarduino = False
	a=str(date.today())+" "+inA+".000001"
	b=str(date.today())+" "+inB+".000001"
	c=str(date.today())+" "+outA+".000001"
	d=str(date.today())+" "+outB+".000001"
	#inA = datetime.strptime(a,"%Y-%m-%d %H:%M:%S.%f")  #just for time conversion view)

	split1 = inA.split(":")
	split2 = inB.split(":")
	now = str(timeN)
	sp = now.split(" ")
	time_ = sp[1]
	splitnow = time_.split(":")
	split3 = outA.split(":")
	split4 = outB.split(":")

	if int(splitnow[0]) in range(int(split1[0]),int(split2[0])) or int(splitnow[0])==int(split1[0]) or int(splitnow[0])==int(split2[0]):
		if int(split1[0])==int(split2[0]) and int(splitnow[0])==int(split1[0]):
			if int(splitnow[1]) in range(int(split1[1]),int(split2[1])):
				readarduino = True
				print("ARDUINO ONN1")
			else :
				if int(splitnow[1]) in range(int(split3[1]),int(split4[1])):
					#if state =="incounting":
						#callresetArduino==True
					readarduino = True
				else:
					readarduino = False
					print("ARDUINO OFF[1]")
		else :
			if int(splitnow[0]) in range(int(split1[0]),int(split2[0])):
				readarduino = True
				print("ARDUINO ONN[2]")
			else :
				if int(splitnow[1]) in range(int(split3[0]),int(split4[0])):
					#if state =="incounting":
						#callresetArduino=True
					readarduino = True
				else:
					readarduino = False
					print("ARDUINO OFF[2]")
	else :
		if int(splitnow[0]) in range(int(split3[0]),int(split4[0])) or int(splitnow[0])==int(split3[0]) or int(splitnow[0])==int(split4[0]):
			if int(split3[0])==int(split4[0]) and int(splitnow[0])==int(split3[0]):
				if int(splitnow[1]) in range(int(split3[1]),int(split4[1])):
					readarduino = True
					print("ARDUINO ONN[1]")
					#if state =="incounting":
						#callresetArduino==True
				else :
					readarduino = False
					print("ARDUINO OFF[1]")
			else :
				if int(splitnow[0]) in range(int(split3[0]),int(split4[0])):
					readarduino = True
					print("ARDUINO ONN[2]")
					#if state =="incounting":
						#callresetArduino==True
				else :
					readarduino = False
					print("ARDUINO OFF[2]")
		else :
			readarduino = False
			print("ARDUINO [OFF]")
	return readarduino
def outgoing():
	pass
def ReadfromArduino(port, scrf, arduino, iDEnt, progb, root,x, title, inA,inB,outA,outB):
	"""This function reads incoming data from serial COM port every second"""
	def count():
		start = time.time()
		now = datetime.now()
		outime = str(now)
		sp = outime.split(" ")
		time_ = sp[1]
		splitnow = time_.split(":")
		splitout = outA.split(":")
		if splitnow[0]==splitout[0] and splitnow[1]==splitout[1]:
			print("[preparing the system for OUT TIME ATTENDANCE]")
			#arduino.close()
			#link.Continue(root,port,inA,inB,outA,outB)
			#print("-----------------------OUT TIME --------------------------------")
			#root.after(10000)
			#presences.clear()
		ardubool = settings(now,inA,inB,outA,outB)
		if ardubool == True :
			arduino.write('systemstart'.strip().encode())
			try :
				reads = arduino.readline()
				print("OUT TIME : Waiting for newcard...")
				fdata = reads.decode()
				data = fdata.rstrip()
				data = str(data)
				data = int(data)
				data = abs(data)
				data =  str(data)
				if len(data)>3:
					print("-------------------------------------------------------------------------------")
					print("[CARD DETECTED]\t AT [TIME] : ",now, "  [ID] : ",data)
					print("-------------------------------------------------------------------------------")
					tools.progress(progb, root,20)
					iDEnt.config(state=tk.NORMAL)
					iDEnt.delete(0,tk.END)
					iDEnt.insert(0,data)
					show_studentDetails(True,data, scrf,x, title, now)
					tools.sendtoDatabase(data)
					tools.progress(progb, root,100)
					
					#iDEnt.config(state=tk.DISABLED)
			except:
				#print("processing...")
				tools.progress(progb, root,0)
		else :
			try:
				arduino.write('systemsleep'.strip().encode())
			except :
				pass
		scrf.after(5000, count)
	count()


class Application:
	"""This class is the main window for managing the attendance system, 
	it's called when the login procedures has been successfuly done"""
	def __init__(self, rt, com, oA,oB, iA,iB):
		#parameters
		rt.destroy()
		root = tk.Tk()
		self.COM = "COM"+com
		scx=int(root.winfo_screenwidth())
		self.scx = scx
		scy=int(root.winfo_screenheight())
		self.scy = scy
		geo=f"{scx}x{scy}+0+0"
		root.geometry(geo)
		root.title("ATTENDANCE SYSTEM")
		root.config(bg="#d4dde8")
		self.cont = tk.Frame(root, width=scx, height=scy, bg="#d4dde8")
		self.cont.place(x=1,y=1)
		
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
			text= "Show Student")
		searchbtn.place(x=20,y=60)
		viewbtn = ttk.Button(self.btnframe,
			text= "Delete Student", 
			command = lambda:self.deleteStudent(ent1.get()))
		viewbtn.place(x=115,y=60)
		delbtn = ttk.Button(self.btnframe,
			text= "View All Students", 
			command=lambda:self.viewAllStudents(scx-80))
		delbtn.place(x=210,y=60)
		self.inA = tk.Entry(self.btnframe, bg="#d4dde8",width=15)
		self.inA.place(x=340, y=2)
		self.inA.insert(0,iA)
		self.outA = tk.Entry(self.btnframe, bg="#d4dde8",width=15)
		self.outA.place(x=340, y=26)
		self.outA.insert(0,oA)
		self.inB = tk.Entry(self.btnframe, bg="#d4dde8",width=15)
		self.inB.place(x=430, y=2)
		self.inB.insert(0,iB)
		self.outB = tk.Entry(self.btnframe, bg="#d4dde8",width=15)
		self.outB.place(x=430, y=26)
		self.outB.insert(0,oB)
		self.inA.configure(state=tk.DISABLED)
		self.inB.configure(state=tk.DISABLED)
		self.outA.configure(state=tk.DISABLED)
		self.outB.configure(state=tk.DISABLED)
		#first time setting(default)
		
		self.newcard = tk.LabelFrame(frame1, text="New Student Registration", 
			width=650, height=110, bg="#d4dde8", fg="blue")
		self.newcard.pack(side=tk.LEFT, padx=5)#place(x=scx/2, y=5)
		iDentry_ = tk.Label(self.newcard, font=maFonte2,
			text="New Student ID", bg="#d4dde8").place(x=2,y=2)
		self.iDentry = ttk.Entry(self.newcard, 
			font = maFonte2, width=25)
		self.iDentry.insert(0,"2102669076")
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
		self.title = tk.Label(tframe, fg="white", bg="#08246b", font=('Century Gothic',14,'bold'),
			text="  N°\t\tSTUDENT NAMES\t\tSTUDENT ID\t\tGENDER\t\t\tCLASS\t\tTIME\t\t")
		self.title.pack(side=tk.LEFT,fill=tk.BOTH)
	
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

		now = datetime.now()
		searchbtn.config(command = lambda:show_studentDetails(False,ent1.get(), self.scrf, scx-80, self.title,now ))
		progb = ttk.Progressbar(root, orient = tk.HORIZONTAL,length = scx/2, mode = 'determinate')
		progb.place(x=scx/4,y=scy/6-5)	
		tools.progress(progb, root,20)
		tools.progress(progb, root,100)
		
		year = tk.Entry(self.btnframe, width=10, font=maFonte2)
		year.place(x=340,y=60)
		year.insert(0,"Year")
		tools.BindedEntry2(year, "Year")
		daty = tk.Entry(self.btnframe, width=17, font=maFonte2)
		daty.place(x=400,y=60)
		daty.insert(0,"Month(January01)")
		tools.BindedEntry2(daty, "Month(January01)")
		search = ttk.Button(self.btnframe, text="Search", 
				command = lambda:tools.showSpecificDate(self.scrf, self.title,daty.get(), year.get(), scx-80)).place(x=550,y=60)
		#here we prompt the user to transfer data from Arduino to the server(our PC Actually) by serial communication"""
		#try :
		now = datetime.now()
		ardubool = settings(now,iA,iB, oA,oB)
		arduino = serial.Serial(com, 9600, timeout=.1)
		if ardubool == True :
			arduino.write('systemstart'.strip().encode())
			print("[ARDUINO STARTED ON PORT] :", self.COM)
			ReadfromArduino(com,self.scrf, arduino,self.iDentry, progb, 
				root, scx-80, self.title, iA,iB, oA,oB)
		else :
			print("ARDUINO STOPPED...")
			arduino.write('systemsleep'.strip().encode())
		#except :
			#messagebox.showerror("ARDUINO ERROR",
				#f"Error connecting to Arduino port {self.COM} please"
				#"verify the com selected in your Arduino IDE,"
				#" or close connexion and start again")
		root.mainloop()
	def saveStudent(self):
		"""This function register a new student and save his data in the db for next attendance"""
		iD = self.iDentry.get()
		open("files/ALLID.txt",'w+').write(f",{iD}")
		name = self.Namentry.get()
		Class = self.Classentry.get()
		Gender = self.Sexentry.get()
		dbfile = "database/STUDENTLIST.db"
		#cursor.execute(f'create database {dbfile}')
		connexion = SQL.connect(dbfile)
		cursor = connexion.cursor()
		cquery = """CREATE TABLE IF NOT EXISTS LIST (ID INTEGER PRIMARY KEY AUTOINCREMENT,studentName TEXT NOT NULL, studentID INTEGER NOT NULL, Gender TEXT NOT NULL, Class TEXT NOT NULL);"""
		result = cursor.execute(cquery)
		squery = 'SELECT * FROM LIST WHERE studentID=?'
		cursor.execute(squery, [iD])
		present = cursor.fetchall()
		if present :
			messagebox.showwarning("Existing Student", 
				f"The student you are trying to add with ID : {iD} already exists in")
		else :
			try:
				mySql_iquery = 'INSERT INTO LIST (studentName, studentID,Gender,Class)VALUES (?,?,?,?)'
				recordall = (name,iD,Gender,Class)
				cursor.execute(mySql_iquery, recordall)
				connexion.commit()
				messagebox.showinfo("Student Added", 
					f"successfully added Student with ID:{iD}")
				self.Namentry.delete(0,tk.END)
				self.Classentry.delete(0,tk.END)
				self.Sexentry.delete(0,tk.END)
			except Error as error:
				messagebox.showerror("Table Error", 
					f"Unable to insert Student data in table : \nError details:{error}")
	def deleteStudent(self, iD):
		"""This function delete an existing student data"""
		now = datetime.now()
		show_studentDetails(False,iD, self.scrf, self.scx-80, self.title, now)
		qst = messagebox.askyesno("Delete Student", "Are you sure you want to delete this student?")
		if qst>0 :
			dbfile = "database/STUDENTLIST.db"
			connexion = SQL.connect(dbfile)
			cursor = connexion.cursor()
			squery = 'SELECT * FROM LIST WHERE studentID=?'
			cursor.execute(squery, [iD,])
			result1 = cursor.fetchall()
			if result1 :
				try :
					dquery = 'DELETE FROM LIST WHERE studentID=?'
					cursor.execute(dquery, [iD,])
					connexion.commit()
					result2 = cursor.fetchall()
					if cursor.rowcount>0:
						messagebox.showinfo("Delete Student", 
							f"student with ID : {iD} has been successfully deleted ")
				except :
					messagebox.showinfo("Delete Student", 
						f"unabe to delete ID : {iD}")
			else :
				messagebox.showerror("Delete Student", 
						"the student you're trying to delete doesnt exist \n"
						f"ID : {iD} not found...")
			#except :
				#messagebox.showerror("Delete Student",
					#f"unable to make delete operation for ID : {iD}")
		else :
			pass
	def viewAllStudents(self,x):
		"""This function displays in the scrollable frame all available 
			students from the database"""
		self.title.config(text="\tN°\t\tSTUDENT NAMES\t\t  STUDENT ID\t\t  GENDER\t\t  CLASS\t\t\t-")
		main=tk.LabelFrame(self.scrf,height=x,width=x,font=maFonte2,bg="white")
		main.place(x=5, y=5)
		cframe=tk.LabelFrame(main, height=1000000, width=x,font=maFonte2,bg="white")
		cframe.place(x=5, y=5)
		dbfile = f"database/STUDENTLIST.db"
		connexion = SQL.connect(dbfile)
		cursor = connexion.cursor()
		try :
			cursor.execute(f'SELECT * FROM LIST')
			lst = cursor.fetchall()
			if len(lst)>0:
				total_rows = len(lst)
				total_columns = len(lst[0]) 
				for i in range(total_rows):
					for j in range(total_columns):
						self.e =tk.Entry(cframe, bg="#f4f7fa", width=22, fg='green',
							font=('Arial',15))
						self.e.grid(row=i, column=j)
						self.e.insert(tk.END, lst[i][j]) 		
			else:
				messagebox.showerror("DB ERROR", 
					"database is empty")
		except:
			messagebox.showerror("DB ERROR", 
					"error openning database")
	