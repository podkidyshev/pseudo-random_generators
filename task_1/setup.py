import os
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = 'C:/Programs/Python36/tcl/tcl8.6'
os.environ['TK_LIBRARY'] = 'C:/Programs/Python36/tcl/tk8.6'

base = None    

executables = [Executable("main.py", base=base)]

buildOptions = dict(
    packages = ["os", "sys", "tkinter", "numpy", "matplotlib", "scipy", "random", "argparse"],
    excludes = [],
    include_files=['C:/Programs/Python36/DLLs/tcl86t.dll', 'C:/Programs/Python36/DLLs/tk86t.dll']
)

setup(
    name = "generators",
    options = dict(build_exe = buildOptions),
    version = "0.1",
    description = 'Lalala',
    executables = executables
)
