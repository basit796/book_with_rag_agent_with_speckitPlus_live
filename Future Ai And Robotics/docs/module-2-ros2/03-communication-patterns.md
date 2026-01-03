---
sidebar_position: 3
title: Communication Patterns
---

# Communication Patterns

## Topics: Streaming Data

Topics are ideal for continuous sensor streams. **Publisher** nodes send messages; **subscriber** nodes receive. Topic has a name (`/camera/image`) and message type (`sensor_msgs/Image`).

**Characteristics**: Asynchronous (publisher doesn't wait), one-to-many (multiple subscribers), best-effort or reliable delivery (QoS configurable), typically high frequency (10-100 Hz).

**Python Example**:
```python
# Publisher
pub = node.create_publisher(Image, '/camera/image', 10)
pub.publish(img_msg)

# Subscriber  
sub = node.create_subscription(Image, '/camera/image', callback, 10)
```

**Use cases**: Camera images, LIDAR scans, IMU data, odometry, joint states.

## Services: Synchronous Calls

Services provide request-reply pattern. Client sends request and **blocks** until server replies. Service has name (`/reset_odometry`) and service type (defining request/response messages).

**Characteristics**: Synchronous (blocking), one-to-one, reliable delivery, typically low frequency (on-demand).

**Python Example**:
```python
# Server
srv = node.create_service(Trigger, '/reset_odom', handle_reset)

# Client
client = node.create_client(Trigger, '/reset_odom')
response = client.call(request)  # Blocks
```

**Use cases**: Configuration changes, state queries, triggering one-shot operations.

## Actions: Long Tasks with Feedback

Actions handle long-running goal-oriented tasks. Client sends goal, server provides periodic feedback and final result. Client can cancel mid-execution.

**Characteristics**: Asynchronous with feedback, goal-cancel-result pattern, typically seconds to minutes duration.

**Python Example**:
```python
# Action client
client = ActionClient(node, NavigateToPos, '/navigate')
goal = NavigateToPos.Goal(x=5.0, y=3.0)
future = client.send_goal_async(goal, feedback_callback=fb_cb)
```

**Use cases**: Navigation to goal, object grasping, manipulation sequences, long-running planning.

## Quality of Service (QoS)

QoS policies control communication behavior:

**Reliability**: Best-effort (UDP-like, may lose messages) vs Reliable (TCP-like, guaranteed delivery). Sensors often use best-effort; commands use reliable.

**Durability**: Volatile (new subscribers miss old messages) vs Transient Local (new subscribers get last N messages). Configuration topics use transient local.

**History**: Keep last N messages vs keep all. Affects memory and latency.

**Deadline**: Maximum time between messages. Detect missing sensor data.

Example: Camera topic uses best-effort + volatile (real-time stream). Map topic uses reliable + transient-local (new nodes need current map).

## TF2: Transform Library

Robots have many coordinate frames: world, robot_base, camera, gripper. **TF2** manages transforms between frames.

**Transform Tree**: Hierarchical tree of frames. Example: world → robot_base → camera_link → camera_optical.

**Lookups**: Query transform between any two frames at any time. TF2 interpolates if exact timestamp unavailable.

**Use cases**: Convert camera detections to world coordinates, compute gripper target poses, display sensor data in rviz.

## Parameter System

Parameters configure node behavior without recompilation. Declared at node startup, get/set at runtime, YAML file loading supported.

**Types**: Integer, float, string, boolean, arrays.

**Dynamic reconfigure**: Nodes register callbacks triggered when parameters change.

Example: Adjust `camera_fps` parameter from 30 to 60 FPS without restarting node.

## Lifecycle Nodes

Standard nodes start immediately. **Lifecycle nodes** have explicit state transitions: Unconfigured → Inactive → Active → Finalized.

**Use cases**: Resource management (allocate hardware in configure step), controlled startup (activate only when dependencies ready), graceful shutdown.

Managed via lifecycle service calls or launch file orchestration.

## Summary

ROS 2 communication patterns:
- **Topics**: streaming data, asynchronous, high frequency
- **Services**: request-reply, synchronous, on-demand
- **Actions**: long tasks, feedback, cancellation

Supporting systems: QoS policies (reliability/durability control), TF2 (coordinate transforms), parameters (configuration), lifecycle nodes (controlled startup/shutdown).

Choose pattern based on data flow: continuous → topic, quick query → service, long task → action.
