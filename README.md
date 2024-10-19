# clearpath_simulator_harmonic

This is a modified version of [clearpath_simulator](https://github.com/clearpathrobotics/clearpath_simulator) that launches and manages all pertinent nodes, services and acition servers to run Gazebo Harmonic simulation worlds, enabling effective testing and validation of robot behavior in virtual settings.

NOTE! This repo requires the use of [Clearpath YAML](https://docs.clearpathrobotics.com/docs/ros/config/yaml/overview/) files to configure various clearpath robot platform. 

## Setup

* Check setup instructions in the root of the [clearpath_simulator_harmonic_ws](https://github.com/clearpathrobotics/clearpath_simulator) repository.

* Root level directory must contain a ```robot_yamls``` folder. A sample yaml file is provided for quick testing

## Vanilla world

* Launch a A200 Husky platform on the default world: ```ros2 launch clearpath_gz simulation.launch.py```