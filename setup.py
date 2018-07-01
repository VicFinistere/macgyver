from cx_Freeze import *
import os

# Please check for tcl86t.dll & tk86t.dll in tcl and tk dir
os.environ['TCL_LIBRARY'] = r'.\venv\Script\tcl86t'
os.environ['TK_LIBRARY'] = r'.\venv\Script\tk86t'

base = None

if sys.platform == "win32":
    base = "Win32GUI"

target = Executable(
    script="main.py",
    base=base,
    icon='item.ico',
    )

setup(
    name="Mac Gyver Maze",
    description="Run a maze with Mac Gyver and collect 3 items",
    author="Zoe Belleton",
    options={'build_exe': {'packages': ['pygame', 'pytmx', 'random']}},
    executables=[target]
)


