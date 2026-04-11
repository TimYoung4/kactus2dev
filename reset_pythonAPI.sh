#!/bin/bash

# IFX: executed in <kactus2_root>/build

set -e

echo "Resetting Python API..."

cd PythonAPI

# Remove old files
rm -f PythonAPI_wrap.cxx
make clean

# Generate new files
swig -c++ -python ../../PythonAPI/PythonAPI.i

cp ../../PythonAPI/PythonAPI_wrap.cxx .

qmake6 ../../PythonAPI/PythonAPI.pro
make -j12

cd ../executable
rm -f pythonAPI.py _pythonAPI.so
cp ../../PythonAPI/pythonAPI.py .
ln -s ./libPythonAPI.so.1.0.0 _pythonAPI.so
