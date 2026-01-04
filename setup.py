#!/usr/bin/env python
# SPDX-FileCopyrightText: 2025 Reo Yamaguchi
# SPDX-License-Identifier: BSD-3-Clause

from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'my_cpu_monitor'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['launch/monitor.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='leo0607y',
    maintainer_email='reochimaru@gmail.com',
    description='robosys2025_2',
    license='BSD-3-Clause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'monitor = my_cpu_monitor.monitor_node:main',
            'listener = my_cpu_monitor.listener_node:main',
        ],
    },
)