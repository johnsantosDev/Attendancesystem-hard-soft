"""
ATTENDANCE SYSTEM : LOGIN SYSTEM
Author : JOHN SANTOS
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import ImageTk, Image
import manage
import tools

maFonte2 = ('Century Gothic',18)
maFonte1 = ('Arial',12)


def Continue(root, com,iA,iB,oA,oB):
	"""This function calls the backend managnment system after Admin Super user connection """
	manage.Application(root,com, iA,iB,oA,oB)

def getConnected():
	"""Check SuperUser(Admin) username and password, choose the port where arduino is connected"""
	if usn_.get()==defaultuser and pwd_.get()==defaultpswd:
		eframe.destroy()
		ff = tk.LabelFrame(root, text="Admin Connexion", font=maFonte1, 
			bg="#d4dde8",width=600,height=350)
		ff.place(x=50,y=50)
		com = ttk.Entry(ff, font=maFonte2, width=25)
		com.place(x=190,y=100)
		com.insert(0, "PORT COM")
		tools.BindedEntry2(com, "PORT COM")
		l1 = tk.Label(ff, text= "In Time ",
			bg="#d4dde8",font=maFonte2).place(x=10, y=180)
		inA = tk.Entry(ff, width=15, font=maFonte2)
		inA.place(x=150, y=180)
		inA.insert(0,"08:00:00")
		outA = tk.Entry(ff, width=15, font=maFonte2)
		outA.place(x=150, y=210)
		outA.insert(0,"16:00:00")
		l2 = tk.Label(ff, text= "Out Time ", 
			bg="#d4dde8", font=maFonte2).place(x=10, y=210)
		inB = tk.Entry(ff, width=15, font=maFonte2)
		inB.place(x=350, y=180)
		inB.insert(0,"08:59:00")
		outB = tk.Entry(ff, width=15, font=maFonte2)
		outB.place(x=350, y=210)
		outB.insert(0,"16:59:00")
		ttk.Button(ff,text="Continue", 
			command = lambda:Continue(root,com.get(),
				inA.get(), inB.get(), outA.get(),outB.get())).place(x=300,y=270)
	else :
		messagebox.askretrycancel("LOGIN ERROR", 
			"invalid Admin Username of password... please check and try again")

#LOGIN GUI OF THE SYSTEM
root = tk.Tk()
root.title("LOGIN")
root.geometry("700x450+300+100")
root.config(bg="#d4dde8")
title = tk.Label(root, text="RFID BASED SCHOOL ATTENDANCE SYSTEM",bg="#d4dde8",
	 font=('Century Gothic',20, 'bold'), fg="blue").place(x=70,y=5)
eframe = tk.LabelFrame(root, text="Admin Connexion", font=maFonte1, 
	bg="#d4dde8",width=600,height=350)
eframe.place(x=50,y=50)
userico = ImageTk.PhotoImage(Image.open("styles/userico.png"))
tk.Label(eframe, image=userico, bg="#d4dde8").place(x=250,y=1)

defaultuser = "adminuser"  #super admin username 
defaultpswd = "123456789"  #super admin password 
usn = tk.Label(eframe, bg="#d4dde8",text="Username", 
	font=maFonte2).place(x=50,y=145)
usn_ = tk.Entry(eframe, font=maFonte2, width=25)
usn_.place(x=180,y=150)
pwd = tk.Label(eframe, bg="#d4dde8",text="Password", 
	font=maFonte2).place(x=50,y=185)
pwd_ = tk.Entry(eframe, font=maFonte2, width=25, show_="*")
pwd_.place(x=180,y=190)
btncon = tk.Button(eframe, text="Connect", font=maFonte2,command=getConnected)
btncon.place(x=380, y=230)
root.mainloop()


