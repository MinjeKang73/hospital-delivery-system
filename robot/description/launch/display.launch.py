from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import PackageNotFoundError, get_package_share_directory


def joint_state_publisher_node(use_sim_time):
    try:
        get_package_share_directory("joint_state_publisher_gui")
        return Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            name="joint_state_publisher_gui",
            output="screen",
            parameters=[{"use_sim_time": use_sim_time}],
        )
    except PackageNotFoundError:
        try:
            get_package_share_directory("joint_state_publisher")
            return Node(
                package="joint_state_publisher",
                executable="joint_state_publisher",
                name="joint_state_publisher",
                output="screen",
                parameters=[{"use_sim_time": use_sim_time}],
            )
        except PackageNotFoundError:
            return LogInfo(
                msg=(
                    "joint_state_publisher_gui and joint_state_publisher are not installed; "
                    "launching robot_state_publisher and RViz only."
                )
            )


def generate_launch_description():
    pkg_share = FindPackageShare("description")
    xacro_file = PathJoinSubstitution([pkg_share, "urdf", "robot.urdf.xacro"])
    rviz_config = PathJoinSubstitution([pkg_share, "rviz", "display.rviz"])
    use_sim_time = LaunchConfiguration("use_sim_time")

    robot_description = ParameterValue(
        Command(["xacro ", xacro_file]),
        value_type=str,
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="false",
        ),
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            output="screen",
            parameters=[
                {
                    "robot_description": robot_description,
                    "use_sim_time": use_sim_time,
                }
            ],
        ),
        joint_state_publisher_node(use_sim_time),
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="screen",
            arguments=["-d", rviz_config],
            parameters=[{"use_sim_time": use_sim_time}],
        ),
    ])
