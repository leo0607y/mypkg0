##!/usr/bin/env python
# SPDX-FileCopyrightText: 2025 Reo Yamaguchi
# SPDX-License-Identifier: BSD-3-Clause:

set -e 

DISTRO=${1:-humble}

# 動的に環境を切り替え
source /opt/ros/$DISTRO/setup.bash
cd /root/ros2_ws
source install/setup.bash

echo "--- Running Test on ROS 2 $DISTRO ---"

# Launch起動
echo "--- Starting Launch File ---"
ros2 launch my_cpu_monitor monitor.launch.py > /tmp/test.log 2>&1 &
PID=$!

# 起動待ち
sleep 15

# トピック存在確認
echo "--- Test 1: Topic Existence ---"
ros2 topic list | grep '/cpu_usage'

# データ受信と型確認
echo "--- Test 2: Data Reception ---"
# 数値だけを抽出
VALUE=$(ros2 topic echo --once /cpu_usage | grep "data:" | awk '{print $2}')

if [ -z "$VALUE" ]; then
    echo "Error: No data received on /cpu_usage"
    kill $PID
    exit 1
fi

# (0.0 <= x <= 100.0)
echo "--- Test 3: Range Check ($VALUE) ---"
# bcコマンドで比較
RESULT=$(echo "$VALUE >= 0 && $VALUE <= 100" | bc -l)

if [ "$RESULT" -eq 1 ]; then
    echo "Check Passed: $VALUE is within valid range."
else
    echo "Check Failed: $VALUE is invalid."
    kill $PID
    exit 1
fi

# 7. 正常終了
echo "--- Integration Test: ALL PASSED ---"
kill $PID
exit 0