from cx_Freeze import setup, Executable
import sys

build_exe_options = {
    "packages": [
        "pygame",
        "speech_recognition",
        "pyttsx3",
        "aifc",
        "chunk",
        "audioop"
    ],
    "include_files": [
        ("recursos", "recursos"),
        ("assets", "assets"),
        "log.dat"
    ]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # remove o terminal ao abrir o jogo

setup(
    name="Limbo",
    version="1.0",
    description="Jogo com pygame e voz",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)
