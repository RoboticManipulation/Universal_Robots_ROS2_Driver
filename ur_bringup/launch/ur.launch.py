from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, ThisLaunchFileDir,PythonExpression

import launch.logging
from launch.conditions import IfCondition

def generate_launch_description():
    # Declare arguments
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "ur_setup",
            description="IP address by which the robot can be reached.",
            choices=[
                "ur3e",
                "ur5",
                "ur5e",
            ],
        )
    )
   

    # Get the value of ur_setup
    ur_setup = LaunchConfiguration("ur_setup")

    # Conditional launch descriptions
    ur5_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([ThisLaunchFileDir(), "/ur5.launch.py"]),
        launch_arguments={
            
            }.items(),
        condition=IfCondition(PythonExpression(["'", ur_setup, "' == 'ur5'"])),
    )

    ur5e_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([ThisLaunchFileDir(), "/ur5e.launch.py"]),
        launch_arguments={
           
            }.items(),
        condition=IfCondition(PythonExpression(["'", ur_setup, "' == 'ur5e'"])),
    )
    
    ur3e_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([ThisLaunchFileDir(), "/ur3e.launch.py"]),
            launch_arguments={
            
                }.items(),
            condition=IfCondition(PythonExpression(["'", ur_setup, "' == 'ur3e'"])),
        )
    return LaunchDescription(declared_arguments + [ ur3e_launch, ur5_launch, ur5e_launch])