# Running the project
# Terminal 1
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch  turtlebot3_gazebo turtlebot3_house.launch.py 

# Terminal 2
ros2 launch slam_toolbox online_async_launch.py

# Terminal 3
pkill -f rviz2
ros2 launch nav2_bringup rviz_launch.py

# Terminal 4
colcon build --packages-select gesture_turtlebot
source install/setup.bash
ros2 run gesture_turtlebot gesture_recognition

# Terminal 5
source install/setup.bash
ros2 run gesture_turtlebot gesture_to_cmd

# Terminal 6 (Won't need teleop once guestures are working)
ros2 run turtlebot3_teleop teleop_keyboard


# Terminal 7 — spawn controller
colcon build --packages-select gesture_turtlebot
source install/setup.bash
ros2 run gesture_turtlebot spawn_controller



# To rebuild everything and start in a clean slate
pkill -f ros2
pkill -f gazebo
pkill -f gzserver
pkill -f gzclient
pkill -f rviz2
sleep 2
ros2 node list
rm -rf build/ install/ log/
colcon build
source install/setup.bash