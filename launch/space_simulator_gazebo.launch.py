import os

from ament_index_python.packages import get_package_share_directory
from ament_index_python import get_package_prefix

from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import (
    DeclareLaunchArgument,
    OpaqueFunction,
    RegisterEventHandler,
    IncludeLaunchDescription,
)
from launch.event_handlers import OnProcessExit
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def launch_setup(context, *args, **kwargs):

    pkg_share_path = os.pathsep + os.path.join(get_package_prefix('space_simulator'), 'share', 'space_simulator', 'models')
    if 'GAZEBO_MODEL_PATH' in os.environ:
        os.environ['GAZEBO_MODEL_PATH'] += pkg_share_path
    else:
        os.environ['GAZEBO_MODEL_PATH'] =  pkg_share_path

    world_path = PathJoinSubstitution(
                [FindPackageShare('space_simulator'),
                 "world", "celestial_sphere.world"])

    start_gazebo_server_cmd = IncludeLaunchDescription(
      PythonLaunchDescriptionSource([os.path.join(
        get_package_share_directory('gazebo_ros'), 'launch'), '/gzserver.launch.py']),
      launch_arguments={'world': world_path}.items())
 
    start_gazebo_client_cmd = IncludeLaunchDescription(
     PythonLaunchDescriptionSource([os.path.join(
        get_package_share_directory('gazebo_ros'), 'launch'), '/gzclient.launch.py']))
    
    nodes_to_start = [
        start_gazebo_server_cmd,
        start_gazebo_client_cmd
    ]

    return nodes_to_start


def generate_launch_description():
    declared_arguments = []

    return LaunchDescription(declared_arguments + [OpaqueFunction(function=launch_setup)])