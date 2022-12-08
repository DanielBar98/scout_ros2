# Changes:
# rviz starts automatically
# change path to mesh-files (include scout_v2 folder in meshes folder)
# meshes will load

#TO DO:
# meshes laden teilweise erst, wenn das roboter model neu geladen wird
#try out joint state publisher node/interface
#spawn roboter
#meshes für scout mini mit aufnehmen --> github gazebo agilex repo

import os
import launch
import launch_ros

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import FindExecutable, PathJoinSubstitution
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node


def generate_launch_description():
    ## Define pathes an static parameters    
    model_name = 'scout_v2.xacro'
    # model_path = os.path.join(get_package_share_directory('scout_description'), "urdf", model_name)
    # print(model_path)
    robot_description_content = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]), " ",
        PathJoinSubstitution(
            [FindPackageShare("scout_description"), "urdf", model_name]
        ),
    ])
    
    # Name of the description package
    package_description = "scout_description"
    
    # RVIZ Configuration
    rviz_config_dir = os.path.join(get_package_share_directory(package_description),'rviz','urdf_config.rviz')
    
    # return Launch Description
    return launch.LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true',
            description='Use simulation clock if true'),

        launch.actions.LogInfo(msg='use_sim_time: '),
        launch.actions.LogInfo(msg=launch.substitutions.LaunchConfiguration('use_sim_time')),
        
        # Starts robot_state_publisher node --> publishes robot joint transforms under /robot_description topic
        launch_ros.actions.Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'use_sim_time': launch.substitutions.LaunchConfiguration('use_sim_time'),
                'robot_description':robot_description_content
            }]),

        # Starts rviz node with provided config file from scout_description package
        launch_ros.actions.Node(
            package='rviz2',
            executable='rviz2',
            output='screen',
            name='rviz_node',
            parameters=[{'use_sim_time': True}],
            arguments=['-d', rviz_config_dir]
            ),
            
    ])
