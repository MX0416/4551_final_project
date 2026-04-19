import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/matt/Documents/CSCI4551/4551_final_project/install/gesture_turtlebot'
