#!/usr/bin/env python
# SPDX-FileCopyrightText: 2025 Reo Yamaguchi
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import psutil

class CpuMonitorNode(Node):
    def __init__(self):
        super().__init__('cpu_monitor_node')
        self.publisher_ = self.create_publisher(Float32, 'cpu_usage', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.get_logger().info('CPU Monitor Node has started.')

    def timer_callback(self):
        msg = Float32()
        # CPU使用率取得
        msg.data = psutil.cpu_percent()
        self.publisher_.publish(msg)
        # ログ表示
        self.get_logger().info(f'Publishing CPU Usage: {msg.data}%')

def main(args=None):
    rclpy.init(args=args)
    node = CpuMonitorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()