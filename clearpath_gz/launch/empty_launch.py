"""
Top-level launch file to launch a Clearpath robot in an empty world

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
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node

# Declare launch arguments
ARGUMENTS = [
    DeclareLaunchArgument('rviz', default_value='false',
                          choices=['true', 'false'], description='Start rviz.'),
    DeclareLaunchArgument('world', default_value='empty_world_cpr',
                          description='empty gazebo world'),
    DeclareLaunchArgument('setup_path',
                          default_value=[EnvironmentVariable('HOME'), '/clearpath_simulator_harmonic_ws/robot_yamls/'],
                          description='Path to YAML files for the robots'),
    DeclareLaunchArgument('use_sim_time', default_value='true',
                          choices=['true', 'false'],
                          description='use_sim_time'),
    DeclareLaunchArgument('robot_config_yaml',
                          default_value='robot.yaml',
                          description='Default name of a robot`s configuration file name'),
    
    # Joystick node settings
    DeclareLaunchArgument('joy_config', default_value='teleop_xbox',
                          description='Joystick configuration YAML file name'),
    DeclareLaunchArgument('joy_dev', default_value='2',
                          description='Joystick device name in /dev/input/js<int> format'),
    DeclareLaunchArgument('publish_stamped_twist', default_value='true',
                          description='Publish geometry_msgs/TwistStamped instead of geometry_msgs/Twist'),
    DeclareLaunchArgument('config_filepath', default_value = ''), # The path is resolved during runtime
    DeclareLaunchArgument('config_with_yaml', default_value=[LaunchConfiguration('joy_config'), '.yaml'])
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

    # Join paths to additional launch files to spawn world and robot
    gz_sim_launch = PathJoinSubstitution(
        [pkg_clearpath_gz, 'launch', 'gz_sim.launch.py'])
    
    robot_spawn_launch = PathJoinSubstitution(
        [pkg_clearpath_gz, 'launch', 'robot_spawn.launch.py'])

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

    # Create launch description and add actions
    ld = LaunchDescription(ARGUMENTS)
    #ld.add_action(node_joy_spawner)
    ld.add_action(gz_sim)
    ld.add_action(robot_spawn) # Here in robot_yaml / <robot_name_dir>/ all the pertinent config files and sub launch files are generated
    return ld
