from cx_Freeze import setup, Executable
import sys
import os

# Define a base para GUI (evita abrir o terminal junto no Windows)
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Inclusão dos arquivos de mídia
incluir_arquivos = [
    ("recursos", "recursos"),
    ("assets", "assets")
]

setup(
    name="Limbo",
    version="1.0",
    description="Jogo Limbo",
    options={
        "build_exe": {
            "packages": [
                "pygame",
                "random",
                "json",
                "pyttsx3",
                "speech_recognition"
            ],
            "include_files": incluir_arquivos,
            "include_msvcr": True
        }
    },
    executables=[
        Executable("main.py", base=base, target_name="Limbo.exe")
    ]
)
