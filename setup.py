# Build the Windows executable (run on Windows, or under Wine):
#     python -m pip install cx_Freeze
#     python setup.py build_exe
# Output: build/ReNameR/ReNameR.exe (copy the whole folder to distribute).
# Optional: put a renamer.ico next to this file to give the exe an icon.
import os

from cx_Freeze import Executable, setup

ICON = "renamer.ico" if os.path.exists("renamer.ico") else None

setup(
    name="ReNameR",
    version="2.0",
    description="ReNameR - renommage de fichiers en lot",
    author="TanGuy",
    options={
        "build_exe": {
            "build_exe": os.path.join("build", "ReNameR"),
            "excludes": ["unittest", "pydoc", "email", "http", "xml", "test"],
            "include_msvcr": True,
        }
    },
    executables=[
        Executable(
            "renamer.py",
            base="gui",
            target_name="ReNameR.exe",
            icon=ICON,
            copyright="CC0 1.0 Universal",
        )
    ],
)
