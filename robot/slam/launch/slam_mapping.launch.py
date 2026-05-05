from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
import os


def generate_launch_description():
    slam_share = get_package_share_directory('slam')
    control_share = get_package_share_directory('control')
    sensor_share = get_package_share_directory('sensor_components')
    description_share = get_package_share_directory('description')

    use_sim_time = LaunchConfiguration('use_sim_time')
    slam_params_file = LaunchConfiguration('slam_params_file')
    encoder_params_file = LaunchConfiguration('encoder_params_file')
    imu_params_file = LaunchConfiguration('imu_params_file')
    ekf_params_file = LaunchConfiguration('ekf_params_file')

    default_slam_params_file = os.path.join(
        slam_share,
        'config',
        'slam_mapper_params.yaml'
    )
    default_encoder_params_file = os.path.join(
        control_share,
        'config',
        'encoder_odom_params.yaml'
    )
    default_imu_params_file = os.path.join(
        sensor_share,
        'config',
        'imu_params.yaml'
    )
    default_ekf_params_file = os.path.join(
        sensor_share,
        'config',
        'ekf.yaml'
    )
    default_urdf_file = os.path.join(
        description_share,
        'urdf',
        'robot.urdf.xacro'
    )

    robot_description = ParameterValue(
        Command(['xacro ', default_urdf_file]),
        value_type=str
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false'
        ),
        DeclareLaunchArgument(
            'slam_params_file',
            default_value=default_slam_params_file
        ),
        DeclareLaunchArgument(
            'encoder_params_file',
            default_value=default_encoder_params_file
        ),
        DeclareLaunchArgument(
            'imu_params_file',
            default_value=default_imu_params_file
        ),
        DeclareLaunchArgument(
            'ekf_params_file',
            default_value=default_ekf_params_file
        ),
        DeclareLaunchArgument(
            'motor_port',
            default_value='/dev/ttyACM0'
        ),
        DeclareLaunchArgument(
            'motor_baudrate',
            default_value='115200'
        ),
        DeclareLaunchArgument(
            'cyglidar_port',
            default_value='/dev/ttyUSB0'
        ),
        DeclareLaunchArgument(
            'cyglidar_baud_rate',
            default_value='0'
        ),
        DeclareLaunchArgument(
            'cyglidar_run_mode',
            default_value='2'
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_description,
                'use_sim_time': use_sim_time
            }]
        ),
        Node(
            package='control',
            executable='motor_bridge_node',
            name='motor_bridge_node',
            output='screen',
            parameters=[{
                'port': LaunchConfiguration('motor_port'),
                'baudrate': ParameterValue(LaunchConfiguration('motor_baudrate'), value_type=int),
                'wheel_separation': 0.38,
                'max_linear_vel': 1.0,
                'watchdog_timeout': 0.5
            }]
        ),
        Node(
            package='control',
            executable='encoder_odom_node',
            name='encoder_odom_node',
            output='screen',
            parameters=[
                encoder_params_file,
                {'use_sim_time': use_sim_time}
            ]
        ),
        Node(
            package='sensor_components',
            executable='imu_node',
            name='imu_node',
            output='screen',
            parameters=[
                imu_params_file,
                {'use_sim_time': use_sim_time}
            ]
        ),
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_node',
            output='screen',
            parameters=[
                ekf_params_file,
                {'use_sim_time': use_sim_time}
            ]
        ),
        Node(
            package='cyglidar_d2_ros2',
            executable='cyglidar_d2_publisher',
            name='cyglidar_d2_publisher',
            output='screen',
            parameters=[{
                'port_number': LaunchConfiguration('cyglidar_port'),
                'baud_rate': ParameterValue(LaunchConfiguration('cyglidar_baud_rate'), value_type=int),
                'frame_id': 'laser_frame',
                'fixed_frame': '/map',
                'run_mode': ParameterValue(LaunchConfiguration('cyglidar_run_mode'), value_type=int),
                'frequency_channel': 0,
                'duration_mode': 0,
                'duration_value': 10000,
                'color_mode': 0,
                'data_type_3d': 0,
                'filter_mode': 0,
                'edge_filter_value': 0,
                'enable_kalmanfilter': True,
                'enable_clahe': False,
                'clahe_cliplimit': 40,
                'clahe_tiles_grid_size': 8
            }]
        ),
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[
                slam_params_file,
                {'use_sim_time': use_sim_time}
            ]
        )
    ])
