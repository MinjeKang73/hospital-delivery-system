import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    control_share = get_package_share_directory('control')
    sensor_share = get_package_share_directory('sensor_components')

    default_encoder_params_file = os.path.join(
        control_share, 'config', 'encoder_odom_params.yaml')
    default_imu_params_file = os.path.join(sensor_share, 'config', 'imu_params.yaml')
    default_ekf_params_file = os.path.join(sensor_share, 'config', 'ekf.yaml')

    use_sim_time = LaunchConfiguration('use_sim_time')
    encoder_params_file = LaunchConfiguration('encoder_params_file')
    imu_params_file = LaunchConfiguration('imu_params_file')
    ekf_params_file = LaunchConfiguration('ekf_params_file')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation clock if true.',
        ),
        DeclareLaunchArgument(
            'encoder_params_file',
            default_value=default_encoder_params_file,
            description='Path to the encoder odometry parameters file.',
        ),
        DeclareLaunchArgument(
            'imu_params_file',
            default_value=default_imu_params_file,
            description='Path to the IMU node parameters file.',
        ),
        DeclareLaunchArgument(
            'ekf_params_file',
            default_value=default_ekf_params_file,
            description='Path to the robot_localization EKF parameters file.',
        ),
        Node(
            package='control',
            executable='encoder_odom_node',
            name='encoder_odom_node',
            output='screen',
            parameters=[encoder_params_file, {'use_sim_time': use_sim_time}],
        ),
        Node(
            package='sensor_components',
            executable='imu_node',
            name='imu_node',
            output='screen',
            parameters=[imu_params_file, {'use_sim_time': use_sim_time}],
        ),
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[ekf_params_file, {'use_sim_time': use_sim_time}],
        ),
    ])
