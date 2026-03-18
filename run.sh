#!/bin/bash
# 1. 定位并进入执行目录
cd "$(dirname "$0")/executable"

# 2. 设置系统动态库路径 (解决 libIPXACTmodels.so 报错)
export LD_LIBRARY_PATH=$PWD:$LD_LIBRARY_PATH

export PYTHONPATH=$PWD:~/kactus2dev/workspace/test_programs:$PYTHONPATH

# 5. 启动 Kactus2
./kactus2 "$@"
