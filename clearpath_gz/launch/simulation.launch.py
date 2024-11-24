"""
Top-level launch file to start a Clearpath robot simulation in Gazebo Harmonic

Copyright 2023 Clearpath Robotics, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

@author Roni Kreinin (rkreinin@clearpathrobotics.com)
Modified by
@author Azmyin Md. Kamal (azmyin12@gmail.com)
"""

# Imports
import os
from launch.actions import LogInfo
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, LaunchConfiguration, PathJoinSubstitution, TextSubstitution


# Declare launch arguments
ARGUMENTS = [
    DeclareLaunchArgument('rviz', default_value='false',
                          choices=['true', 'false'], description='Start rviz.'),
    DeclareLaunchArgument('world', default_value='warehouse_cpr',
                          description='Gazebo World'),
    DeclareLaunchArgument('setup_path',
                          default_value=[EnvironmentVariable('HOME'), '/clearpath_simulator_harmonic_ws/robot_yamls/'],
                          description='Path to YAML files for the robots'),
    DeclareLaunchArgument('use_sim_time', default_value='true',
                          choices=['true', 'false'],
                          description='use_sim_time'),
    DeclareLaunchArgument('robot_config_yaml',
                          default_value='robot.yaml',
                          description='Default name of a robot`s configuration file name'),
    DeclareLaunchArgument('joy_config', default_value='xbox',
                          description='Joystick configuration to use'),
    DeclareLaunchArgument('joy_dev', default_value='0',
                          description='Joystick device'),
    DeclareLaunchArgument('publish_stamped_twist', default_value='false',
                          description='Publish geometry_msgs/TwistStamped instead of geometry_msgs/Twist'),
    DeclareLaunchArgument('config_filepath', default_value = ''), # The path is resolved during runtime
    DeclareLaunchArgument('config_with_yaml', default_value=[LaunchConfiguration('joy_config'), '.config.yaml'])
]

# Set robot pose
for pose_element in ['x', 'y', 'yaw']:
    ARGUMENTS.append(DeclareLaunchArgument(pose_element, default_value='0.0',
                     description=f'{pose_element} component of the robot pose.'))

ARGUMENTS.append(DeclareLaunchArgument('z', default_value='0.3',
                 description='z component of the robot pose.'))

# Launch description
def generate_launch_description():
    # Directories
    pkg_clearpath_gz = get_package_share_directory(
        'clearpath_gz')

    # Join paths to additional launch files to spawn world, robot, joy controller
    gz_sim_launch = PathJoinSubstitution(
        [pkg_clearpath_gz, 'launch', 'gz_sim.launch.py'])
    
    robot_spawn_launch = PathJoinSubstitution(
        [pkg_clearpath_gz, 'launch', 'robot_spawn.launch.py'])
    
    # Construct full path to the teleop-launch.py file located in teleop_twist_joy
    teleop_twist_joy_launch = PathJoinSubstitution(
        [get_package_share_directory('teleop_twist_joy'), 'launch', 'teleop-launch.py'])

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([gz_sim_launch]),
        launch_arguments=[
            ('world', LaunchConfiguration('world'))
        ]
    )

    robot_spawn = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([robot_spawn_launch]),
        launch_arguments=[
            ('use_sim_time', LaunchConfiguration('use_sim_time')),
            ('setup_path', LaunchConfiguration('setup_path')),
            ('robot_config_yaml', LaunchConfiguration('robot_config_yaml')),
            ('world', LaunchConfiguration('world')),
            ('rviz', LaunchConfiguration('rviz')),
            ('x', LaunchConfiguration('x')),
            ('y', LaunchConfiguration('y')),
            ('z', LaunchConfiguration('z')),
            ('yaw', LaunchConfiguration('yaw'))]
    )

    # ROS 2 resolves dynamic launch during runtime. Hence only in this part, we can resolve the full path to `xbox.config.yml` file
    joy_config_yaml_string = PathJoinSubstitution([get_package_share_directory('teleop_twist_joy'), 'config', LaunchConfiguration('config_with_yaml')])
    
    # Use LogInfo to print the resolved path
    log_action = LogInfo(msg=joy_config_yaml_string)

    teleop_twist_joy_spawn = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([teleop_twist_joy_launch]),
        launch_arguments=[
            ('joy_config', LaunchConfiguration('joy_config')),
            ('joy_dev', LaunchConfiguration('joy_dev')),
            ('publish_stamped_twist', LaunchConfiguration('publish_stamped_twist')),
            ('config_filepath', joy_config_yaml_string)
        ]
    )
    # Create launch description and add actions
    ld = LaunchDescription(ARGUMENTS) 
    # ld.add_action(log_action) # To print debug message
    ld.add_action(teleop_twist_joy_spawn)
    ld.add_action(gz_sim)
    ld.add_action(robot_spawn)
    return ld
