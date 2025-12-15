---
id: chapter-3-ros-2-fundamentals
title: Chapter 3 - ROS 2 Fundamentals
sidebar_label: 3. ROS 2 Fundamentals
sidebar_position: 3
---

# Chapter 3: ROS 2 Fundamentals

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand the ROS 2 architecture and its core components.
- Create and manage ROS 2 nodes, topics, and services.
- Write basic publisher and subscriber programs in Python.
- Navigate the ROS 2 ecosystem using command-line tools.

## Introduction

The **Robot Operating System (ROS 2)** is the industry-standard middleware for building robot software. It provides a collection of tools, libraries, and conventions for developing modular and reusable robot applications.

ROS 2 is a complete redesign of its predecessor, ROS 1, and includes major improvements in real-time performance, security, and multi-robot support. It is used in research labs, startups, and production systems worldwide.

## Core Concepts

### ROS 2 Architecture

ROS 2 uses a **distributed architecture** where independent programs, called nodes, communicate with each other over well-defined interfaces.

#### Key Components:

1. **Nodes**: Independent processes that perform specific tasks.
2. **Topics**: Channels for sending and receiving messages asynchronously.
3. **Services**: A way for nodes to send a request and receive a response.
4. **Actions**: A mechanism for handling long-running tasks that provide feedback.
5. **Parameters**: Configuration values that can be changed for each node.

### Nodes

A **node** is a single program that performs one function, such as reading a camera feed, controlling a motor, or planning a path.

**Design Philosophy**: A best practice is to have each node be responsible for a single task.

For example, a simple mobile robot might have the following nodes:
- `camera_driver`: Publishes images from a camera.
- `object_detector`: Detects objects in the images.
- `navigation`: Plans paths and sends velocity commands.
- `motor_controller`: Converts velocity commands into motor signals.

### Topics and Messages

**Topics** are channels that enable publish-subscribe communication.

- **Publishers** send messages to a topic.
- **Subscribers** receive messages from a topic.
- Messages have a specific type, such as `sensor_msgs/Image` or `geometry_msgs/Twist`.

```
┌─────────┐         Topic: /camera/image        ┌─────────┐
│ Camera  │ ──────────────────────────────────> │ Detector│
│  Node   │  (Message Type: sensor_msgs/Image)  │  Node   │
└─────────┘                                     └─────────┘
```

### Services

**Services** provide a way for nodes to communicate synchronously through a request-response model.

- A **Client** node sends a request and waits for a response.
- A **Server** node processes the request and returns a result.

Services are useful for querying a robot's state or triggering a one-time action.

```python
# Pseudocode for a service call
response = client.call_async(request)
# ... wait for the future to complete ...
result = response.result()
```

### Actions

**Actions** are used for long-running tasks that need to provide feedback while they are executing. An action consists of:

- A **Goal**: The objective to be achieved.
- **Feedback**: Periodic updates on the task's progress.
- A **Result**: The final outcome of the task.

A good example is a navigation task, like "Navigate to position (x, y)," which can provide periodic updates on the robot's current position as feedback.

## Practical Application

### Example 1: Simple Publisher (Python)

This program creates a node that publishes a "Hello World" message to a topic every second.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.count = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.count}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    node = MinimalPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Explanation:**
1. We create a node called `minimal_publisher`.
2. We then create a publisher that sends messages of type `String` on the `topic` topic, with a queue size of 10.
3. A timer is used to call the `timer_callback` function every 1.0 second.
4. `rclpy.spin()` enters a loop, keeping the node running so it can publish messages.

### Example 2: Simple Subscriber (Python)

This program creates a node that listens for messages on a topic and prints them to the console.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    node = MinimalSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Explanation:**
1. A subscriber is created to listen to the `topic` topic.
2. We register `listener_callback` as the function to handle any incoming messages.
3. The callback function prints the received message to the console.

### Running the Example

```bash
# In Terminal 1, run the publisher
ros2 run my_package publisher_node

# In Terminal 2, run the subscriber
ros2 run my_package subscriber_node

# In Terminal 3, you can use these tools to inspect the system
ros2 topic list
ros2 topic echo /topic
```

### Command-Line Tools

ROS 2 comes with a powerful set of command-line tools for debugging and introspection.

```bash
# List all running nodes
ros2 node list

# List all active topics
ros2 topic list

# Get information about a specific topic
ros2 topic info /camera/image

# Display the messages being published on a topic
ros2 topic echo /camera/image

# Call a service from the command line
ros2 service call /service_name service_type "{request_data}"

# Visualize the node graph
ros2 run rqt_graph rqt_graph
```

## Summary

ROS 2 provides a powerful framework for building modular robotic systems. Its publish-subscribe architecture enables loose coupling between components, making systems easier to develop, test, and scale.

Understanding nodes, topics, and services is essential for working with any ROS 2-based robot, from academic research platforms to commercial humanoids.

**Key Takeaways:**
- ROS 2 uses a distributed architecture with independent nodes.
- Topics enable asynchronous, publish-subscribe communication.
- Services provide a synchronous, request-response pattern.
- Python and C++ are the primary languages supported for ROS 2 development.

## Further Reading

- **Official Documentation**:
  - [ROS 2 Documentation](https://docs.ros.org/en/humble/)
  - [ROS 2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)

- **Books**:
  - *A Concise Introduction to Robot Programming with ROS 2* by Francisco Martín Rico
  - *Programming Robots with ROS* by Morgan Quigley et al. (Note: Primarily for ROS 1, but many concepts are transferable)

- **Online Courses**:
  - [ROS 2 for Beginners (Udemy)](https://www.udemy.com/topic/ros/)
  - [The Construct ROS Learning Platform](https://www.theconstructsim.com/)

- **Community**:
  - [ROS Discourse Forum](https://discourse.ros.org/)
  - [ROS Answers Q&A Site](https://answers.ros.org/)
