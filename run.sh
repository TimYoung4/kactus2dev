#!/bin/bash

# IFX: executed in <kactus2_root>/build

cd "$(dirname "$0")/executable"

export LD_LIBRARY_PATH=$PWD:/opt/python/3.12/linux/RHEL70/lib/:$LD_LIBRARY_PATH
export PYTHONPATH=$PWD:$PYTHONPATH

# for test programs
export PYTHONPATH=$PWD/../workspace/test_programs:$PYTHONPATH

./kactus2 "$@"
