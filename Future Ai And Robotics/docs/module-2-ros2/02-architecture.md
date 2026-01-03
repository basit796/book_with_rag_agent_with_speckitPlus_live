---
sidebar_position: 2
title: ROS 2 Architecture  
---

# ROS 2 Architecture

## Core Concepts

ROS 2 organizes software into **nodes**—independent processes performing specific functions (camera_driver, slam_node, path_planner).

### Topics (Publish-Subscribe)

Named buses for streaming data. Publishers send messages; subscribers receive copies. Example: `/camera/image` topic published by camera_driver at 30 Hz, subscribed by object_detector and person_tracker. Many-to-many: multiple publishers and subscribers allowed.

### Services (Request-Reply)

Synchronous request-reply. Example: `/reset_map` service where navigation node requests map reset, mapping node replies with status. Used for configuration, querying state, triggering actions. Blocking until reply received.

### Actions (Long-Running Tasks)

Handle goal-oriented tasks with feedback and cancellation. Example: `/navigate_to_goal` action sends goal position, receives periodic feedback (current position, distance remaining), and final result (success/failure). Used for navigation, grasping, motion sequences.

## DDS Foundation

ROS 2 built on DDS (Data Distribution Service)—OMG standard for real-time publish-subscribe. Implementations: Fast DDS (default), Cyclone DDS, Connext DDS. Provides Quality of Service (QoS) configuration, automatic discovery via multicast UDP, and zero-copy transport support.

## Launch Files and Parameters

**Launch files** start multiple nodes together. Example: `robot.launch.py` can start camera_driver, object_detector, and path_planner with one command: `ros2 launch my_robot robot.launch.py`

**Parameters** are key-value settings (camera_fps: 30, max_speed: 1.5). Set via launch file, command line, or YAML. Nodes can declare parameters and register callbacks for changes.

## Communication Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| Topic | Streaming sensor data | Camera images, LIDAR scans |
| Service | Quick request-reply | Get pose, reset odometry |
| Action | Long tasks with feedback | Navigate, grasp object |

## Computational Graph

All nodes and connections form the **computational graph**. Visualize with: `ros2 run rqt_graph rqt_graph` showing nodes (boxes), topics (edges), publishers/subscribers (arrows).

## Summary

ROS 2 provides nodes (independent processes), topics (streaming data), services (request-reply), actions (long tasks with feedback), DDS foundation, launch files (orchestration), and parameters (configuration). This modular architecture enables building complex robots from reusable components.
