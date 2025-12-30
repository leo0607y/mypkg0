# CPU使用率監視パッケージ
[![test](https://github.com/leo0607y/mypkg0/actions/workflows/test.yml/badge.svg)](https://github.com/leo0607y/mypkg0/actions/workflows/test.yml)

本パッケージは、システムのCPU負荷をROS2ネットワーク上に配信する `monitor` ノードと、それを受信してターミナル上にゲージを表示する `listener` ノードで構成。

## テスト環境
- 実行環境: GitHub-hosted runner (ubuntu-22.04)
- コンテナイメージ: `ryuichiueda/ubuntu22.04-ros2:latest`
    - ROS 2 Version: Humble

## 各ノードの機能
### monitor
- システムのCPU使用率を取得し、ROS 2トピックとして配信
- プログラム名: `monitor_node.py`
- `psutil` ライブラリを使用してCPU使用率を取得
- パブリッシュ (Output): `/cpu_usage` ([std_msgs/msg/Float32]): 現在のCPU使用率 [%]

### listener
- 配信されたCPU使用率を受信し、視覚化し表示
- プログラム名: `listener_node.py`
- 受信した数値をもとに、50段階で（`#`）を用いたゲージ表示
- サブスクライブ (Input): `/cpu_usage` ([std_msgs/msg/Float32]): 受信したCPU使用率 [%]

## トピックの仕様説明
### `/cpu_usage`
- 型: `std_msgs/Float32`
- 単位: `%`
- 内容: システム全体のCPU使用率（0.0〜100.0）

## 使用方法
### monitor
- 以下コマンドでCPUの使用率配信を独立して実行
```bash
$ ros2 run my_cpu_monitor monitor

[INFO] [cpu_monitor_node]: CPU Monitor Node has started.
[INFO] [cpu_monitor_node]: Publishing CPU Usage: 11.2%
[INFO] [cpu_monitor_node]: Publishing CPU Usage: 0.2%
[INFO] [cpu_monitor_node]: Publishing CPU Usage: 0.6%
```
### listener
- 以下コマンドでCPUの使用率の受信と表示を独立して実行
```bash
$ ros2 run my_cpu_monitor listener

[INFO] [cpu_listener_node]: --- SYSTEM RESOURCE MONITOR SUBSCRIPTION STARTED ---
[INFO] [cpu_listener_node]: [LOW   ] [#####.............................................]  11.2%
[INFO] [cpu_listener_node]: [LOW   ] [..................................................]   0.2%
[INFO] [cpu_listener_node]: [LOW   ] [..................................................]   0.6%
```
- CPU使用状況に応じステータスラベルが以下のように変化

| ステータス | 閾値 (CPU使用率) | ログレベル | 備考 |
| :--- | :--- | :--- | :--- |
| `[LOW   ]` | 30% 未満 | `INFO` | 安定状態 |
| `[MID   ]` | 70% 未満 | `INFO` | 中負荷 |
| `[HIGH  ]` | 90% 未満 | `WARN` | 注意 |
| `[ALERT ]` | 90% 以上 | `ERROR` | 警告 |

### launchfile
- 以下のコマンドを実行すると、CPU監視（monitor）と表示（listener）が連動して動作
- [monitor-1]: 1秒毎に現在のCPU使用率を計測し、トピック /cpu_usage に送信
- [listener-2]: 受信したデータを用い、50段階のゲージで視覚化
```bash
$ ros2 launch my_cpu_monitor monitor.launch.py

[INFO] [monitor-1]: process started with pid [76402]
[INFO] [listener-2]: process started with pid [76403]
[monitor-1] [INFO] [monitor]: CPU Monitor Node has started.
[listener-2] [INFO] [listener]: --- SYSTEM RESOURCE MONITOR SUBSCRIPTION STARTED ---
[listener-2] [INFO] [listener]: [LOW   ] [########..........................................]  17.8%
[monitor-1] [INFO] [monitor]: Publishing CPU Usage: 10.7%
```
## 著作及びライセンス
- このソフトウェアパッケージは、３条項BSDライセンスの下、再頒布及び仕様が許可されます。
- © 2025 Reo Yamaguchi