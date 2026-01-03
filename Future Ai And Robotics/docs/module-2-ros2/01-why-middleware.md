---
sidebar_position: 1  
title: Why Robots Need Middleware
---

# Why Robots Need Middleware

## The Complexity of Robot Software

A robot isn't a single program—it's dozens of concurrent processes:
- Camera drivers publishing images at 30 FPS
- LIDAR nodes publishing point clouds at 10 Hz  
- Localization estimating pose at 50 Hz
- Path planners computing trajectories at 1 Hz
- Motor controllers executing at 1000 Hz

Each process runs independently, potentially on different computers (laptop + embedded controller + GPU). They must communicate reliably, share data, and coordinate actions. **This is where middleware comes in**.

## What is Middleware?

Middleware is software between the operating system and application code, providing:
- **Inter-process communication**: Send data between processes
- **Message serialization**: Convert data structures to bytes and back
- **Discovery**: Processes find each other automatically
- **Quality of Service**: Reliability, latency, bandwidth guarantees

Without middleware, you'd write custom networking code, handle TCP/UDP sockets, implement message formats, and manage process discovery manually—hundreds of hours of error-prone work.

ROS 2 (Robot Operating System 2) is the dominant robotics middleware providing publish-subscribe messaging, services, actions, parameters, and built on DDS (Data Distribution Service) standard.

## The Sense-Compute-Act Pipeline

Data flow through a mobile robot using ROS 2:

1. **Camera Driver**: Captures images, publishes to `/camera/image` at 30 Hz
2. **Object Detector**: Subscribes to images, runs inference, publishes `/objects`
3. **Path Planner**: Subscribes to objects and pose, computes path, publishes `/cmd_vel`
4. **Motor Controller**: Subscribes to velocity commands, controls motors, publishes odometry

Each process is independent. Add sensors? Publish more topics. Swap algorithms? Replace one node without touching others. This **modularity** is middleware's key advantage.

## Why Not Just Use Sockets?

ROS 2 solves: automatic discovery (no hardcoded IPs), data types (message definitions with serialization), QoS policies (reliability/latency control), tooling (`ros2 topic echo`, `ros2 bag`, `rqt_graph`), and time synchronization.

Middleware abstracts networking challenges, letting developers focus on robot behavior.

## Summary

Robots are distributed systems with concurrent processes. ROS 2 middleware enables inter-process communication, automatic discovery, QoS guarantees, and provides debugging tools.

Next: ROS 2 architecture and core concepts.
