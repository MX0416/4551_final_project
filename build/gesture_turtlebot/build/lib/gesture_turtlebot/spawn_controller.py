import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import subprocess


class SpawnControllerNode(Node):
    def __init__(self):
        super().__init__('spawn_controller')
        self.subscription = self.create_subscription(
            String,
            '/gesture',
            self.gesture_callback,
            10
        )
        self.odom_subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )
        self.tb2_spawned = False
        self.last_spawn_attempt = 0.0
        self.tb1_x = -2.0
        self.tb1_y = -0.5
        self.get_logger().info('Spawn controller node started')

    def odom_callback(self, msg):
        self.tb1_x = msg.pose.pose.position.x
        self.tb1_y = msg.pose.pose.position.y

    def gesture_callback(self, msg):
        if msg.data == 'SPAWN_TB2' and not self.tb2_spawned:
            now = self.get_clock().now().nanoseconds / 1e9
            if now - self.last_spawn_attempt > 10.0:
                self.last_spawn_attempt = now
                self.get_logger().info('SPAWN_TB2 gesture detected — spawning TB2...')
                self.spawn_tb2()

    def spawn_tb2(self):
        x = self.tb1_x
        y = self.tb1_y
        self.get_logger().info(f'Spawning TB2 at TB1 position: x={x:.2f}, y={y:.2f}')

        cmd = [
            'gz', 'service',
            '-s', '/world/default/create',
            '--reqtype', 'gz.msgs.EntityFactory',
            '--reptype', 'gz.msgs.Boolean',
            '--timeout', '1000',
            '--req', f"sdf_filename: '/opt/ros/jazzy/share/turtlebot3_gazebo/models/turtlebot3_burger/model.sdf', name: 'tb2', pose: {{position: {{x: {x}, y: {y}, z: 0.5}}}}"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if 'true' in result.stdout:
            self.tb2_spawned = True
            self.get_logger().info('TB2 spawned successfully!')
        else:
            self.get_logger().error(f'Spawn failed: {result.stderr}')


def main(args=None):
    rclpy.init(args=args)
    node = SpawnControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()