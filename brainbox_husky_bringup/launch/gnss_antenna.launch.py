from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.conditions import UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

def generate_launch_description():

    launch_arg_use_sim = DeclareLaunchArgument(
        'use_sim',
        default_value='false',
        description='True -> Gazebo sensors. False -> use real hardware specified in config/gnss_antenna.yaml',
    )

    yaml_file = (
            Path(get_package_share_directory("brainbox_husky_bringup"))
            / "config" / "gnss_antenna.yaml"
    )

    return LaunchDescription([
        Node(
            package="ublox_gps",
            executable="ublox_gps_node",
            name="ublox_gnss",
            parameters=[str(yaml_file)],
            output="screen",
            condition=UnlessCondition(LaunchConfiguration('use_sim')),
        )
    ])
