import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import TwistStamped

class GestureToCmdNode(Node):
    def __init__(self):
        super().__init__('gesture_to_cmd')
        self.subscription = self.create_subscription(
            String,
            '/gesture',
            self.gesture_callback,
            10
        )
        self.publisher = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.get_logger().info('Gesture to cmd_vel node started')

    def gesture_callback(self, msg):
        twist = TwistStamped()
        twist.header.stamp = self.get_clock().now().to_msg()
        twist.header.frame_id = 'base_link'

        if msg.data == 'FORWARD':
            twist.twist.linear.x = 0.2
            twist.twist.angular.z = 0.0
        elif msg.data == 'STOP':
            twist.twist.linear.x = 0.0
            twist.twist.angular.z = 0.0
        elif msg.data == 'TURN_LEFT':
            twist.twist.linear.x = 0.0
            twist.twist.angular.z = 0.5
        elif msg.data == 'TURN_RIGHT':
            twist.twist.linear.x = 0.0
            twist.twist.angular.z = -0.5
        elif msg.data == 'SPAWN_TB2':
            twist.twist.linear.x = 0.0
            twist.twist.angular.z = 0.0

        self.publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = GestureToCmdNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()