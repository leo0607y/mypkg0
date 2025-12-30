##!/usr/bin/env python
# SPDX-FileCopyrightText: 2025 Reo Yamaguchi
# SPDX-License-Identifier: BSD-3-Clause:

set -e 

#環境構築
source /opt/ros/humble/setup.bash
cd /root/ros2_ws
source install/setup.bash


# Python
python3 --version
python3 -c "import psutil; print('psutil version:', psutil.__version__)"

# トピックの入出力
ros2 launch my_cpu_monitor monitor.launch.py > /tmp/test.log 2>&1 &
PID=$!

# 待機
sleep 15

# トピック生成
ros2 topic list | grep '/cpu_usage' || (echo "Not Found" && kill $PID && exit 1)

# 数値範囲
VALUE=$(ros2 topic echo --once /cpu_usage | grep "data:" | awk '{print $2}')
echo "CPU使用率: $VALUE"

# bcで比較
CHECK=$(echo "$VALUE >= 0 && $VALUE <= 100" | bc -l)
if [ "$CHECK" -eq 1 ]; then
    echo "範囲内: $VALUE"
else
    echo "エラー: $VALUE"
    kill $PID
    exit 1
fi

# ハッシュゲージ表示
grep "\[" /tmp/test.log | grep "#" || (echo "ゲージエラー" && kill $PID && exit 1)

# 正常終了
echo "=== 合格 ==="
kill $PID
exit 0