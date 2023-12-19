from ament_index_python.packages import get_package_share_path
from launch_ros.actions import Node, PushROSNamespace

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    GroupAction,
)
from launch.substitutions import LaunchConfiguration


def generate_launch_description() -> LaunchDescription:
    launch_description = LaunchDescription()
    arg = DeclareLaunchArgument('vehicle_name')
    launch_description.add_action(arg)

    arg = DeclareLaunchArgument('use_sim_time')
    launch_description.add_action(arg)

    package_path = get_package_share_path('final_project')
    mapping_params_file_path = str(package_path / 'config/mapping_params.yaml')

    scenario_arg = DeclareLaunchArgument(
        name='scenario',
        default_value=str(1),
        description='The number of the scenario')
    launch_description.add_action(scenario_arg)

    group = GroupAction([
        PushROSNamespace(LaunchConfiguration('vehicle_name')),
        Node(
            executable='mapper.py',
            package='final_project',
            parameters=[
                LaunchConfiguration('mapping_params',
                                    default=mapping_params_file_path),
                {
                    'use_sim_time': LaunchConfiguration('use_sim_time'),
                },
            ],
        ),
        Node(
            executable='scenario_node.py',
            package='final_project',
            parameters=[
                {
                    'scenario': LaunchConfiguration('scenario'),
                    'use_sim_time': LaunchConfiguration('use_sim_time'),
                },
            ],
        ),
        Node(
            executable='path_planner.py',
            package='final_project',
            parameters=[
                {
                    'use_sim_time': LaunchConfiguration('use_sim_time'),
                },
            ],
        ),
        Node(
            executable='path_follower.py',
            package='final_project',
            parameters=[
                {
                    'use_sim_time': LaunchConfiguration('use_sim_time'),
                },
            ],
        ),
        Node(executable='position_controller.py',
             package='final_project',
             parameters=[{
                 'use_sim_time': LaunchConfiguration('use_sim_time'),
             }]),
        Node(
            executable='yaw_controller.py',
            package='final_project',
            parameters=[
                {
                    'use_sim_time': LaunchConfiguration('use_sim_time'),
                },
            ],
        ),
        Node(
            executable='robot_marker_publisher.py',
            package='final_project',
            parameters=[
                {
                    'use_sim_time': LaunchConfiguration('use_sim_time'),
                },
            ],
        ),
    ])
    launch_description.add_action(group)
    return launch_description