#!/usr/bin/env python
# SPDX-FileCopyrightText: 2025 Reo Yamaguchi
# SPDX-License-Identifier: BSD-3-Clause
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class CpuListenerNode(Node):
    def __init__(self):
        super().__init__('cpu_listener_node')
        self.subscription = self.create_subscription(
            Float32, 'cpu_usage', self.listener_callback, 10)
        self.get_logger().info('--- SYSTEM RESOURCE MONITOR SUBSCRIPTION STARTED ---')

    def listener_callback(self, msg):
        u = msg.data
        
        # 2%刻み
        total_steps = 50
        filled = int(total_steps * u // 100)
        bar = "#" * filled + "." * (total_steps - filled)

        # ステータス判定
        if u < 30.0:
            status = "LOW   "
            log = self.get_logger().info
        elif u < 70.0:
            status = "MID   "
            log = self.get_logger().info
        elif u < 90.0:
            status = "HIGH  "
            log = self.get_logger().warn
        else:
            status = "ALERT "
            log = self.get_logger().error

        log(f"[{status}] [{bar}] {u:5.1f}%")

def main(args=None):
    rclpy.init(args=args)
    node = CpuListenerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()