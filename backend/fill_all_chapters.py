"""Fill all 'coming soon' chapters with concise Physical AI & Robotics content"""

from pathlib import Path

CHAPTERS = {
    "module-1-physical-ai/03-robot-architecture.md": """---
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
""",

    "module-1-physical-ai/04-why-humanoids.md": """---
sidebar_position: 4
title: Why Humanoids?
---

# Why Humanoids?

## The Human-Designed World

Look around. Stairs. Doorknobs. Light switches. Chairs. Tables. Handles. Buttons at standing height. Our entire built environment is designed for the human body—two legs, two arms, ~170 cm tall, hands with opposable thumbs.

This creates a challenge for robots. A wheeled robot can't climb stairs. A quadruped can't turn doorknobs. An industrial arm can't walk to different locations. To navigate and manipulate in human spaces without expensive modifications, **the robot needs a human-like form**.

### Infrastructure Examples

**Stairs**: 40% of multi-story buildings lack elevators globally. Stairs are compact, require no power, and work during emergencies. Wheeled robots are confined to ground floors.

**Doorknobs**: Round knobs require grasping and twisting—impossible for most robot grippers. Lever handles are easier but still need dexterous manipulation.

**Counters and Shelves**: Designed for standing humans (90-110 cm height). Objects stored at this height are unreachable for low robots.

**Narrow Spaces**: Hallways, aisles between furniture, crowded rooms. A wheeled robot with wide base can't squeeze through; a humanoid with narrow profile can.

## The Humanoid Form Factor

Humanoid robots mimic human proportions and capabilities:

**Two Legs (Bipedal Locomotion)**:
- Navigate stairs, curbs, uneven terrain
- Narrow footprint (30-40 cm width) fits through tight spaces
- Dynamically unstable—requires active balance control

**Two Arms**:
- Reach in multiple directions simultaneously  
- Carry objects while walking
- Stabilize during complex manipulation

**Human-Scale Height**:
- Reach counters, shelves, sinks
- Make eye contact with humans (social interaction)
- Operate switches, buttons at standard heights

**Dexterous Hands**:
- 5-fingered hands (or 3-4 finger grippers)
- Opposable thumb enables precision grasping
- Multi-point contact for stable grasps

### Why Bipedal Locomotion is Hard

Walking on two legs is **dynamically unstable**. Unlike quadrupeds (dogs, tables) which are inherently stable, bipeds must constantly adjust to avoid falling.

**Zero Moment Point (ZMP)**: For a biped to remain balanced, the ZMP (center of pressure) must stay within the support polygon (footprint area). Step outside, and the robot tips over.

**Control Frequency**: Balance control runs at 100-1000 Hz. Each millisecond, the robot must:
1. Measure body tilt (IMU)
2. Compute corrective torques (inverse dynamics)
3. Command ankle/hip motors (actuation)

**Energy Cost**: Bipedal walking consumes more energy than wheels on flat ground. But wheels can't climb stairs—the versatility justifies the cost.

## Application Domains for Humanoids

Where do humanoids excel compared to other robot forms?

### Elderly Care and Assistance

**Problem**: Aging populations need help with daily tasks—fetching objects, medication reminders, fall detection, companionship.

**Why Humanoids**: Homes have stairs, narrow bathrooms, furniture-filled rooms. Humanoids can retrieve items from shelves, assist with standing up (stable grip points), and navigate tight spaces.

**Alternatives**: Wheeled assistive robots exist but are confined to ground floors and can't reach high shelves.

### Hospitality and Service

**Problem**: Hotels, restaurants, retail stores need robots for customer service—delivering items, answering questions, cleaning.

**Why Humanoids**: Navigate multi-floor buildings, open doors, carry trays, interact with customers at eye level (less intimidating).

**Example**: Pepper (SoftBank) and Relay (Savioke) robots in hotels. Pepper is humanoid for social interaction; Relay is wheeled but limited to elevators and flat floors.

### Domestic Household Tasks

**Problem**: Homes need cleaning, cooking, laundry, organizing. These tasks involve diverse manipulations in varied spaces.

**Why Humanoids**: Humanoid hands can fold laundry, load dishwashers, operate appliances. Bipedal legs navigate between rooms, climb stairs to upper floors.

**Challenge**: Dexterity requirements are extreme. Folding clothes, handling fragile items, and cooking require human-level manipulation that current humanoids can't match.

### Warehouse and Logistics

**Problem**: E-commerce warehouses need picking and packing. Items vary in size, weight, fragility.

**Why Humanoids**: Can reach high shelves, navigate aisles, handle diverse objects with dexterous grippers. Existing warehouses don't need restructuring.

**Alternatives**: Specialized warehouse robots (Kiva/Amazon Robotics) are faster and cheaper but require custom infrastructure (shelves brought to stationary pickers).

## Trade-Offs: Humanoids vs Alternatives

Humanoids aren't always the best choice. Let's compare:

### Humanoid vs Wheeled Robot

**Wheeled Advantages**:
- Faster on flat ground (3-5 m/s vs 1-2 m/s walking)
- More stable (no balance required)
- Simpler control (2-4 motors vs 20+)
- Cheaper to build

**Wheeled Disadvantages**:
- Can't climb stairs
- Limited manipulation reach (low mounted arms)
- Requires flat, smooth floors

**When to use wheels**: Warehouses with flat floors, outdoor delivery on sidewalks, hospital corridors with ramps.

### Humanoid vs Quadruped

**Quadruped Advantages**:
- Inherently stable (four contact points)
- Better on rough terrain (can handle slopes, rocks)
- Faster locomotion (Spot runs at 1.6 m/s)
- Proven reliability (Boston Dynamics Spot)

**Quadruped Disadvantages**:
- Can't operate human interfaces (doorknobs, switches)
- Limited manipulation (single arm on some models)
- Height limitation (50-80 cm tall)

**When to use quadrupeds**: Inspection tasks (factories, construction sites), outdoor terrain navigation, surveillance.

### Humanoid vs Industrial Arm

**Industrial Arm Advantages**:
- Extremely precise (±0.1 mm repeatability)
- High payload (10-100 kg)
- Proven reliability in manufacturing
- Fast motions (2-3 m/s tool speed)

**Industrial Arm Disadvantages**:
- Fixed location (bolted to floor or table)
- No mobility—can't move to different workspaces
- Requires structured environment

**When to use arms**: Assembly lines, welding, pick-and-place in fixed locations.

### The Humanoid Choice

Choose humanoids when:
- ✅ Environment is designed for humans (stairs, doors, furniture)
- ✅ Tasks require dexterous manipulation (grasping varied objects)
- ✅ Mobility across multi-floor spaces is needed
- ✅ Human-robot interaction benefits from similar form (social acceptance)

Avoid humanoids when:
- ❌ Flat ground only (use wheels)
- ❌ Rough terrain (use quadrupeds)  
- ❌ Fixed location (use industrial arms)
- ❌ Cost and complexity must be minimized

## Social Acceptance and Uncanny Valley

Humans respond differently to different robot forms:

**Anthropomorphism**: People attribute human-like qualities to humanoid robots—intentions, emotions, personality. This increases trust and comfort.

**Uncanny Valley**: But if a humanoid looks *almost* human, small imperfections become disturbing. Stiff movements, expressionless faces, or jerky motions trigger discomfort.

**Design Strategy**:
- **Clearly robotic**: Metallic, angular, non-human face (Boston Dynamics Atlas, Agility Robotics Digit). Functional, no pretense of being human.
- **Stylized humanoid**: Smooth surfaces, simple face, cartoon-like (Softbank Pepper). Friendly, approachable.
- **Avoid realism**: Don't try for human skin, detailed faces unless perfected (Hanson Robotics Sophia caused mixed reactions).

For service and assistive applications, **clearly robotic** or **stylized** humanoids perform better socially.

## Current Humanoid Platforms

**Boston Dynamics Atlas**:
- Height: 1.5 m, Weight: 89 kg
- 28 hydraulic actuators
- Backflips, parkour, dynamic locomotion
- Research platform, not commercially available

**Agility Robotics Digit**:
- Height: 1.65 m, Weight: 45 kg
- Electric actuators, bipedal
- Autonomous navigation, box carrying
- Deployed in warehouses (Amazon trials)

**Tesla Optimus**:
- Height: 1.73 m, Weight: 57 kg
- 28 electric actuators, hands with 11 DoF
- Target: mass production for household tasks
- Under development (prototypes shown 2022-2024)

**Figure 01**:
- Height: 1.7 m, Weight: 60 kg
- Electric actuators, VR teleoperation for learning
- Target: industrial and warehouse applications

**Unitree H1**:
- Height: 1.8 m, Weight: 47 kg
- High-speed bipedal locomotion
- Research and development platform

## Challenges Ahead

Building capable humanoids remains extremely difficult:

**Balance and Locomotion**: Walking on varied terrain, recovering from pushes, climbing stairs reliably.

**Dexterity**: Human-level manipulation—tying knots, handling fragile objects, using tools.

**Perception**: Real-time 3D scene understanding in cluttered, dynamic environments.

**Power**: Batteries limit runtime to 1-4 hours; continuous operation requires frequent recharging.

**Cost**: Current humanoids cost $50K-$500K. Mass adoption requires <$20K price point.

**Safety**: 50+ kg humanoid moving at 1 m/s carries significant momentum. Safe human interaction is critical.

Despite challenges, progress is accelerating. Better actuators, improved AI (vision models, reinforcement learning), and simulation tools (Module 4: Isaac) are making humanoids increasingly viable.

## Summary

Humanoids are valuable because:
- Human environments favor human form factors (stairs, doors, shelves)
- Bipedal locomotion enables navigation in tight, multi-floor spaces
- Dexterous hands enable diverse manipulation tasks
- Social acceptance benefits from familiar form

Trade-offs exist:
- More complex and expensive than wheels or quadrupeds
- Balance control is challenging
- Not optimal for all tasks (use specialized robots when possible)

Humanoids shine in homes, hospitals, hotels—anywhere designed for people. As costs drop and capabilities improve, humanoids will increasingly assist with daily tasks.

Next module explores ROS 2—the middleware that connects sensors, compute, and actuators into coordinated robot systems.
""",
}

def main():
    """Generate content for all chapters"""
    base_path = Path(__file__).parent.parent / "Future Ai And Robotics" / "docs"
    
    print("=== Filling Book Chapters ===\n")
    
    for chapter_path, content in CHAPTERS.items():
        full_path = base_path / chapter_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ {chapter_path}")
    
    print(f"\n✅ Filled {len(CHAPTERS)} chapters successfully!")

if __name__ == "__main__":
    main()
