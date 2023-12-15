"""A setup script to demonstrate build using ssl."""
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from __future__ import annotations

from pathlib import Path

from cx_Freeze import Executable, build_exe, setup


setup(
    name="test_ssl",
    version="0.1",
    description="cx_Freeze script to test ssl",
    executables=[Executable("test_ssl.py")],
    options={
        "build_exe": {
            "zip_include_packages": ["*"],
            "zip_exclude_packages": [],
        }
    },
)
