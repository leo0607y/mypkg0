#!/usr/bin/env python
# SPDX-FileCopyrightText: 2025 Reo Yamaguchi
# SPDX-License-Identifier: BSD-3-Clause


import launch
import launch_ros.actions

def generate_launch_description():
    return launch.LaunchDescription([
        launch_ros.actions.Node(
            package='my_cpu_monitor',
            executable='monitor',
            name='monitor'),
        launch_ros.actions.Node(
            package='my_cpu_monitor',
            executable='listener',
            name='listener'),
    ])