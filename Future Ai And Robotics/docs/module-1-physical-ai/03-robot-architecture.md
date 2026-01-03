---
sidebar_position: 3
title: Anatomy of a Robot
---

# Anatomy of a Robot

## The Three Core Components

Every robot, from simple warehouse bots to humanoids, consists of three fundamental components: **sensors** (to perceive), **compute** (to think), and **actuators** (to act). Think of these as eyes/ears, brain, and muscles.

### Sensors: Perceiving the World

Robots use various sensors to understand their environment:

**Vision Sensors**:
- RGB cameras: capture color images for object detection, scene understanding
- Depth cameras: provide 3D information using stereo, structured light, or time-of-flight
- Event cameras: detect pixel-level brightness changes with microsecond precision

**Position and Motion Sensors**:
- IMUs (Inertial Measurement Units): measure acceleration and rotation rates
- Encoders: track joint angles and motor positions precisely
- GPS: outdoor global positioning (meter-level accuracy)

**Range Sensors**:
- LIDAR: laser-based distance measurement, 360° scanning, 0.1-100 meter range
- Ultrasonic: short-range proximity detection (0.1-5 meters)
- Radar: long-range detection through fog/rain

**Contact and Force Sensors**:
- Force/torque sensors: measure interaction forces at wrist or fingertips
- Tactile sensors: distributed touch sensing across gripper surfaces
- Pressure sensors: detect contact and grip pressure

Each sensor provides different information. Cameras give rich visual data but struggle with precise distances. LIDAR provides accurate 3D geometry but no color or texture. Robust robots fuse multiple sensor types.

### Compute: The Robot Brain

Processing sensor data and controlling actuators requires computational power:

**Embedded Controllers**:
- Microcontrollers (Arduino, STM32): simple, real-time control loops
- Single-board computers (Raspberry Pi, NVIDIA Jetson): vision processing, ROS2 nodes
- Suitable for low-latency motor control and basic perception

**GPU-Accelerated Compute**:
- NVIDIA GPUs: deep learning inference for computer vision
- Process camera streams at 30-60 FPS with neural networks
- Enable real-time object detection, pose estimation, segmentation

**Cloud Offloading**:
- Send data to remote servers for heavy computation
- Useful for training, mapping, high-level planning
- Introduces latency (50-500 ms), unsuitable for real-time control

The compute hierarchy typically splits into:
- **Low-level control** (1-10 kHz): motor PID loops on microcontrollers
- **Mid-level perception** (10-100 Hz): vision processing on embedded GPUs  
- **High-level planning** (1-10 Hz): task planning, decision-making

### Actuators: Taking Action

Actuators convert electrical signals into mechanical motion:

**Electric Motors**:
- DC brushed motors: simple, inexpensive, limited precision
- Brushless DC motors: efficient, powerful, require electronic speed controllers
- Servo motors: include encoder feedback, precise position control
- Stepper motors: discrete steps, no feedback needed, can lose steps under load

**Specialized Actuators**:
- Linear actuators: telescoping motion (extend/retract)
- Pneumatic actuators: compressed air, high force, soft compliance
- Hydraulic actuators: high power density, used in heavy-duty robots
- Series elastic actuators: include springs for impact absorption and force control

Each actuator type has trade-offs in cost, weight, power, precision, and control complexity. Humanoid robots often use brushless motors with high gear reduction for strength while maintaining backdrivability.

## The Sense-Think-Act Control Loop

Robot control isn't a one-time process—it's a continuous loop:

```
SENSE → THINK → ACT → SENSE → THINK → ACT → ...
```

1. **SENSE**: Read all sensors (cameras, IMU, encoders, LIDAR)
2. **THINK**: Process data, update world model, compute desired action
3. **ACT**: Send commands to motors and actuators
4. **SENSE**: Observe results, detect deviations, repeat

This closed-loop control is essential because:
- Actuators have error (commanded 45° might result in 44.8°)
- Environment changes unpredictably (object moves, floor is slippery)
- Disturbances occur (bump from human, wind gust, uneven terrain)

### Control Frequencies Matter

Different tasks require different loop speeds:

**High-Frequency (100-1000 Hz)**:
- Motor torque control
- Balance control for bipeds
- Collision reaction
- Real-time: <10 ms latency requirement

**Medium-Frequency (10-100 Hz)**:
- Vision-based tracking
- Trajectory following
- Grasping adjustments
- Near-real-time: 10-100 ms acceptable

**Low-Frequency (1-10 Hz)**:
- Path planning
- Task sequencing
- High-level decision making
- Soft-real-time: 100-1000 ms acceptable

## AI Model vs AI System

A crucial distinction often missed:

**AI Model**: A neural network trained to map inputs to outputs. Example: object detection model that finds cups in images. Just software. No hardware dependencies.

**AI System**: The model integrated with sensors, actuators, compute hardware, and environment. The **behavior emerges from this integration**, not just the model.

Example: An object detection model achieves 95% accuracy on test images. Deployed on a robot:
- Cameras provide lower quality images than training data (lighting, motion blur)
- Model runs slower on embedded GPU (30 FPS vs 100 FPS offline)
- Detections must trigger motor commands with latency constraints
- System success rate drops to 70% due to integration challenges

The lesson: Training a good model is necessary but insufficient. The **system integration** determines real-world performance.

## Power and Thermal Management

Robots have limited onboard power. Battery capacity constrains operation time.

**Power Consumers**:
- Motors: 50-200W each (humanoid has 20+ motors)
- Compute: 10-100W (depends on GPU usage)
- Sensors: 1-20W (cameras, LIDAR)
- Total: 500-2000W for a humanoid robot

**Battery Capacity**:
- Typical Li-ion pack: 1-5 kWh
- Runtime: 30 minutes to 4 hours depending on activity
- Charging: 1-4 hours

**Heat Generation**:
Motors and compute generate heat. Without cooling, components overheat and throttle or fail. Robots use:
- Passive cooling: heatsinks, thermal interface materials
- Active cooling: fans (noisy, power-hungry)
- Liquid cooling: for high-power systems

Thermal management impacts design: compute can't run at full capacity continuously, motors must duty-cycle, and heavy activity shortens runtime.

## Communication Buses and Real-Time Systems

Components must communicate reliably and quickly:

**Common Buses**:
- **CAN bus**: automotive standard, 1 Mbps, robust, real-time
- **EtherCAT**: industrial Ethernet, 100 Mbps, microsecond synchronization
- **I2C/SPI**: short-range sensor communication on PCBs
- **USB**: cameras, development, not hard-real-time

**Real-Time Operating Systems (RTOS)**:
Standard Linux isn't real-time—process scheduling has unpredictable delays. Robotics uses:
- RT-PREEMPT Linux: real-time kernel patches
- FreeRTOS, Zephyr: dedicated RTOS for microcontrollers
- Guarantees: tasks execute within deterministic time bounds

ROS 2 (Robot Operating System 2) uses DDS for inter-process communication with Quality-of-Service guarantees, enabling real-time performance on RTOS platforms.

## Summary

Robot anatomy consists of:
- **Sensors**: cameras, LIDAR, IMU, encoders, force sensors (perceive)
- **Compute**: microcontrollers, embedded GPUs, cloud (think)
- **Actuators**: motors, servos, linear actuators (act)

These components interact through the **Sense-Think-Act loop** running at appropriate frequencies. The distinction between an AI model and an AI system is critical—integration challenges dominate real-world deployment.

Next chapter examines why humanoid robots specifically are valuable despite their complexity.
