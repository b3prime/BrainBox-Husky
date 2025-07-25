from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch_ros.actions import SetRemap
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, TextSubstitution

# Helper to build "/<robot_ns>/sensors/<name>"                               #
def sensor_path(robot_ns: LaunchConfiguration, tail: str):
    return PathJoinSubstitution([
        TextSubstitution(text='/'),
        robot_ns,
        TextSubstitution(text=f'sensors/{tail}')
    ])

def generate_launch_description() -> LaunchDescription:
    # Namespace of the robot (matches robot.yaml `system → ros2 → namespace`)
    arg_robot_ns = DeclareLaunchArgument(
        'robot_ns',
        default_value='a200_0000',
        description='Robot namespace used by Clearpath generator'
    )
    robot_ns = LaunchConfiguration('robot_ns')

    remap_group = GroupAction([
        # Lidar points
        SetRemap(src = '/a200_0000/sensors/imu_0/data',
                 dst = '/ouster/points'
        ),

        # Lidar scan
        SetRemap(src = sensor_path(robot_ns, 'lidar3d_0/scan'),
                 dst = '/ouster/scan'
        ),

        # IMU data
        SetRemap(src = sensor_path(robot_ns, 'imu_0/data'),
                 dst = '/vectornav/imu'
        ),

        SetRemap(src = sensor_path(robot_ns, 'gps_0/fix'),
                 dst = '/ublox/fix'
        ),
    ])

    return LaunchDescription([
        arg_robot_ns,
        remap_group,
    ])
