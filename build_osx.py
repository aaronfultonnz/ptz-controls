"""
This is an example of py2app setup.py script for freezing your pyside2 application

Usage:
    python setup.py py2app
"""

import os
from setuptools import setup


def tree(src):
    return [(root, map(lambda f: os.path.join(root, f), files))
        for (root, dirs, files) in os.walk(os.path.normpath(src))]


ENTRY_POINT = ['controls.py']
DATA_FILES = tree('DATA_FILES_DIR') + tree('DATA_FILE_DIR2')
OPTIONS = {'argv_emulation': False,
           'strip': True,
           'iconfile': 'assets/AppIcon.icns',
           'includes': []}

setup(
    name="Camera Controller",
    app=ENTRY_POINT,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
