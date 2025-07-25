from launch import LaunchDescription
from launch.launch_description_sources importPythonLaunchDescriptionSource
from launch_ros.actions import IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory
from pathlib import Path

def generate_launch_description():

    zed_launch = Path(
        get_package_share_directory('zed_wrapper'),
        'launch',
        'zed_camera_launch.py'
    )

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(str(zed_launch)),
            launch_arguments={
                'camera_mode': 'zed2i',
                'camera_name': 'zed2i',
                'config_path': str(
                    Path(__file__).with_suffix('.yaml').resolve()
                ),
                'sim_mode': 'true',
                'publish_tf': 'false',
                'base_frame': 'zed2i_link',
            }.items()
        )
    ])
