#!/usr/bin/env python3
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from control_msgs.action import GripperCommand


class GripperClient(Node):

    def __init__(self):
        super().__init__('gripper_client')
        self._action_client = ActionClient(
            self,
            GripperCommand,
            '/robotiq_gripper_controller/gripper_cmd'
        )

    def send_goal(self, position: float, max_effort: float):
        goal_msg = GripperCommand.Goal()
        goal_msg.command.position = position
        goal_msg.command.max_effort = max_effort

        self.get_logger().info(f'Sending goal: position={position}, max_effort={max_effort}')

        self._action_client.wait_for_server()

        return self._action_client.send_goal_async(goal_msg)


def main(args=None):
    rclpy.init(args=args)

    gripper_client = GripperClient()

    # Example: fully close gripper (position=0.0, max_effort=60.0)
    #future = gripper_client.send_goal(0.7, 60.0)
    #future = gripper_client.send_goal(0.7, 0.01)
    future = gripper_client.send_goal(0.0, 0.01)

    rclpy.spin_until_future_complete(gripper_client, future)

    if future.result() is not None:
        goal_handle = future.result()
        gripper_client.get_logger().info("Goal sent successfully")

        # Optionally wait for the result
        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(gripper_client, result_future)
        if result_future.result() is not None:
            gripper_client.get_logger().info(f"Result: {result_future.result().result}")
    else:
        gripper_client.get_logger().error("Failed to send goal")

    gripper_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
