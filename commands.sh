# start gazebo
ros2 launch  turtlebot3_gazebo turtlebot3_house.launch.py 

# start teleop for keyboard control
ros2 run turtlebot3_teleop teleop_keyboard

# start SLAM toolbox
ros2 launch slam_toolbox online_async_launch.py

# start rviz for visualization of SLAM
ros2 launch nav2_bringup rviz_launch.py
