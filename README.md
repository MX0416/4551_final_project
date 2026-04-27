### Project overview:

1. Control a turtlebot with hand gestures through the laptop's webcam using OpenCV and MediaPipe
3. Run the ROS2 SLAM toolbox, and visualize with Rviz2
4. A special hand gesture to spawn a second turtlebot at the first turtlebot's starting location
5. Autonomously navigate the second turtlebot to the first turtlebox using the SLAM constructed map built by the first turtlebot



Project structure:
- gesture_recognition: the perception layer, translating raw pixels into a high level semantic string like TURN_LEFT
- gesture_to_cmd: the translation layer, it maps those semantic strings into physical movement commands, like TwistStamped to move the turtlebot in simulation
- spawn_controller: this spawns a second turtlebot names tb2, and the goal from here on is to have tb2 use its own sensors to navigate to tb1 given tb1's current location in the gazobo environment