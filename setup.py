
from cx_Freeze import setup, Executable
import os.path
build_exe_options = {"packages":["os"], "excludes":["tkinter"]}
#build_exe_options={"packages":modules,"excludes":emodules}
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = "Win32GUI"

options = {
	'build_exe': {
	 	'include_files':[
	 		os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
	 		os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
	 		],
	},
}
setup(name = "Attendance System",
		   options = options,
    	   version = "0.0.0.1",
    	   author = "olela henri",
           description ="This project consist of an advance school attendance system with database",
           executables =[Executable("connect.py", base=base,)]
           )
   
    