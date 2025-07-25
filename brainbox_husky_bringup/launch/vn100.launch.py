from launch import LaunchDescription
from launch_ros.actions import Node
from pathlib import Path                 
from ament_index_python.packages import get_package_share_directory
from launch.conditions import IfCondition, UnlessCondition
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, TextSubstitution, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    launch_arg_use_sim = DeclareLaunchArgument(
        'use_sim',
        default_value='false',
        description='True -> Gazebo sensors. False -> use real hardware specified in config/vn100.yaml',
    )

    use_sim  = LaunchConfiguration('use_sim')

    
    # spin up the real IMU
    vectornav_share = FindPackageShare('vectornav')

    vn_launch_path = PathJoinSubstitution(
        [vectornav_share, 'launch', 'vectornav.launch.py']
    )

    vectornav_hw = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(vn_launch_path),
        condition = UnlessCondition(LaunchConfiguration('use_sim'))
    )

    return LaunchDescription([
        launch_arg_use_sim,
        vectornav_hw,
    ])

