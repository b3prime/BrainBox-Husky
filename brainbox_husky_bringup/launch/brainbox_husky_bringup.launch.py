from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir
from launch_ros.actions import Node, PushRosNamespace
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition

def generate_launch_description():

    # Expose launch arguments
    use_sim_launch_arg = DeclareLaunchArgument(
        'use_sim',
        default_value = 'true',
        description = 'true -> runs Gazebo simulation. false -> uses real robot',
    )

    robot_ns_launch_arg = DeclareLaunchArgument(
        'robot_ns',
        default_value = 'a200_0000',
        description = 'the namespace of the robot (only matters in simulation). a200-000: Husky A200. a300-0000: Husky A300. j100-0000: Jackal J100. w200-0000: Warthog W200'
    )

    setup_path_launch_arg = DeclareLaunchArgument(
        "setup_path",
        default_value = "/home/dcist/dcist_ws/src/brainbox_husky",
        description = "Path to Clearpath robot.yaml file"
    )

    # Find location of relevant share directories
    bringup_share_dir = FindPackageShare('brainbox_husky_bringup')
    clearpath_gz_share_dir = FindPackageShare('clearpath_gz')

    # LaunchDescription for Vectornav
    vn100_launch =  PathJoinSubstitution([bringup_share_dir, 'launch', 'vn100.launch.py'])
    vn100_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([vn100_launch]),
        launch_arguments={
            'use_sim': LaunchConfiguration('use_sim'),
        }.items()
    )

    # LaunchDescription for Ouster
    ouster_launch = PathJoinSubstitution([bringup_share_dir, 'launch', 'ouster.launch.py'])
    ouster_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([ouster_launch]),
        launch_arguments={
            'use_sim': LaunchConfiguration('use_sim'),
            'robot_ns': LaunchConfiguration('robot_ns'),
        }.items()
    )

    # LaunchDescription for UBlox
    ublox_launch =  PathJoinSubstitution([bringup_share_dir, 'launch', 'gnss_antenna.launch.py'])
    ublox_include = IncludeLaunchDescription(PythonLaunchDescriptionSource([ublox_launch]))

    #Launch Description for the Clearpath Gazebo simulation
    sim_launch = PathJoinSubstitution([clearpath_gz_share_dir, 'launch', 'simulation.launch.py'])
    sim_include =   IncludeLaunchDescription(
                        PythonLaunchDescriptionSource([sim_launch]),
                        launch_arguments={
                            "setup_path": LaunchConfiguration("setup_path")
                        }.items(),
                        condition=IfCondition(LaunchConfiguration('use_sim'))
                    )

    # Launch description for the remapping file. 
    # This remaps the simulation's topic names to match the hardware's native name (ex. /a200_0000/sensors/lidar3d_0/scan -> /ouster/scan').
    remap_topics_launch = PathJoinSubstitution([bringup_share_dir, 'launch', 'remap_topics.launch.py'])
    remap_topics_include = IncludeLaunchDescription(
                              PythonLaunchDescriptionSource([remap_topics_launch]),
                              launch_arguments = {
                                  'robot_ns': LaunchConfiguration('robot_ns'),
                              }.items(),
                              condition=IfCondition(LaunchConfiguration('use_sim'))
                          )

    return LaunchDescription([
        setup_path_launch_arg,
        use_sim_launch_arg,
        robot_ns_launch_arg,
        
        vn100_include,
        ublox_include,
        ouster_include,
        sim_include,

        remap_topics_include,
    ])
