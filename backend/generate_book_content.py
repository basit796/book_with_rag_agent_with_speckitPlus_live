"""Generate comprehensive book content for all chapters"""

import os
from pathlib import Path

# Content templates for each chapter
CHAPTER_CONTENT = {
    "module-1-physical-ai/02-physical-constraints.md": """---
sidebar_position: 2
title: The Physical World as a Constraint
---

# The Physical World as a Constraint

## Physics is Non-Negotiable

Unlike software where you can change the rules, bend logic, or patch bugs with creative workarounds, robots must obey the fundamental laws of physics. Gravity doesn't have exceptions. Inertia doesn't pause for debugging. Friction is always present, whether you account for it or not.

Consider a simple task: picking up a coffee mug. In a digital simulation, you can teleport the mug from the table to your hand instantaneously. You can ignore weight, friction, and balance. The virtual hand never slips, never applies too much force, never misjudges the center of mass.

Now try this in the real world with a robot arm. The arm must:
- Sense the mug's exact position (with imperfect cameras)
- Plan a collision-free path to reach it
- Apply precise grip force (too little = drops, too much = crushes)
- Account for the mug's weight and inertia during movement
- Maintain balance if the robot is mobile
- Adapt if the mug moves or is heavier than expected

Every one of these steps involves navigating physical constraints that simply don't exist in purely digital systems.

### Gravity and Weight

Gravity constantly pulls objects downward at 9.8 m/s². This seems obvious, but it has profound implications:

**For Manipulation**: Every object a robot picks up immediately starts falling the moment it's released. Grasping requires continuous force to counteract gravity. The heavier the object, the more torque required from the robot's motors.

**For Locomotion**: Bipedal robots must constantly fight gravity to avoid falling over. Unlike four-legged animals or wheeled robots with inherently stable configurations, humanoids exist in a perpetual state of controlled falling. Every step is a calculated risk.

**For Energy Consumption**: Lifting objects or even holding them in place requires continuous energy expenditure. A robot holding its arm outstretched consumes power fighting gravity, even though it appears motionless.

### Inertia and Momentum

Newton's First Law states that objects resist changes in their state of motion. This manifests as **inertia** (resistance to starting movement) and **momentum** (resistance to stopping).

**Starting Motion**: When a robot arm is stationary and needs to move quickly, it must overcome its own inertia. Heavier arms require more torque to accelerate. This introduces lag between command and execution.

**Stopping Motion**: A robot moving at speed cannot instantly stop. Momentum carries it forward. This is why high-speed robots need sophisticated trajectory planning - they must start slowing down before reaching the target, anticipating the overshoot.

**Real-World Example**: Industrial robot arms moving at high speeds often "wobble" after stopping. This is residual momentum oscillating through the joints. Controllers must actively dampen these oscillations.

### Friction: Friend and Foe

Friction opposes relative motion between surfaces. It's simultaneously essential and problematic for robots.

**Friction Enables Grasping**: Without friction, robot grippers couldn't hold objects. The friction between gripper fingers and object surface provides the grip force. Smooth, slippery objects (wet glass, polished metal) are notoriously hard for robots to grasp because friction is low.

**Friction Enables Walking**: Bipedal and wheeled robots rely on friction between feet/wheels and ground. On ice or oil, friction drops catastrophically, and robots lose the ability to generate forward force. This is why slip detection is critical.

**Friction Resists Motion**: Friction in joints and bearings opposes movement, requiring motors to work harder and consuming energy. Excessive friction causes wear and unpredictable behavior.

**Friction is Unpredictable**: The coefficient of friction varies with surface materials, contamination (dust, oil), temperature, and wear. A robot that works perfectly on a dry tile floor might fail completely on a wet one.

## Sensor Uncertainty and Noise

If physics provides the hard constraints, sensor uncertainty adds the layer of partial knowledge. Robots don't have perfect information about the world - they must act based on noisy, incomplete, and sometimes contradictory sensor data.

### Cameras: The Illusion of Perfect Vision

Humans rely heavily on vision, so it's natural to assume robot cameras provide clear, unambiguous information. But cameras have significant limitations:

**Limited Resolution**: A 1920x1080 camera has about 2 million pixels. Seems like a lot, but that must cover the entire scene. Small objects or distant features occupy only a few pixels, making precise localization difficult.

**Motion Blur**: When the camera or objects move, images blur. Faster motion equals more blur. This is why sports photographers use ultra-fast shutter speeds - but in robotics, faster shutters mean less light, requiring brighter scenes or noisier images.

**Lighting Sensitivity**: Cameras need adequate lighting. Too dark = noisy images. Too bright = saturation and loss of detail. Shadows and highlights obscure features. Backlighting (bright light behind an object) renders the object nearly invisible.

**Depth Ambiguity**: A single camera image is a 2D projection of a 3D world. You can't tell if an object is small-and-close or large-and-far from a single image. This is why stereo cameras, depth sensors, or active SLAM are needed for 3D understanding.

### Depth Sensors: Measuring Distance with Uncertainty

Depth sensors (LIDAR, structured light, time-of-flight cameras) provide distance measurements, but all have noise and failure modes.

**LIDAR Noise**: Each laser pulse has measurement uncertainty, typically 1-5 cm. Over long distances, this compounds. Reflective or transparent surfaces cause false readings. Black surfaces absorb the laser, returning weak signals.

**Structured Light**: Projects patterns and measures distortion. Fails in bright sunlight (pattern washed out) and on featureless surfaces (no pattern to match). Sensitive to surface texture.

**Time-of-Flight Cameras**: Measure light travel time. Prone to interference from other TOF sensors and ambient light. Maximum range limited to ~10 meters for most models.

### IMUs: Drift Over Time

Inertial Measurement Units (IMUs) contain accelerometers and gyroscopes to measure acceleration and rotation. They're essential for balance and orientation estimation in robots.

**The Drift Problem**: IMUs measure changes in motion, not absolute position. Small errors accumulate over time through integration. After a few minutes, an IMU-based position estimate can drift meters from the true location.

This is why robots fuse IMU data with other sensors (cameras, GPS, wheel encoders) - no single sensor provides ground truth.

### Force and Torque Sensors: Feeling the World

Force sensors in robot grippers and joints detect contact forces. This enables delicate manipulation and safe human interaction. But these sensors are noisy, have deadbands (forces too small to detect), and introduce compliance (flex under load) that affects positioning accuracy.

## Actuation Latency and Control Delays

There's always a delay between deciding to act and the action completing. This might be milliseconds, but in a fast-moving robot, milliseconds matter.

### Motor Response Time

Electric motors don't respond instantaneously to commands. They have:
- **Electrical Time Constants**: Current takes time to build up in windings
- **Mechanical Time Constants**: Rotor takes time to overcome inertia and start rotating
- **Gearing Backlash**: Gear teeth have tiny gaps; reversing direction requires taking up the slack first

Total latency from command to motion: typically 10-50 milliseconds.

### Communication Delays

Commands travel from the central computer to motor controllers over communication buses (CAN, EtherCAT, USB). Each message has transmission latency. In multi-robot systems or cloud-connected robots, network delays can reach hundreds of milliseconds.

### Computation Delays

Before sending a command, the robot must process sensor data and compute the appropriate action. Computer vision algorithms, path planning, and inverse kinematics all take time. On embedded processors, this can be 50-200 milliseconds. On powerful GPUs, it drops to 10-50 milliseconds.

**Cascading Delays**: Sense (50 ms) → Compute (100 ms) → Transmit (10 ms) → Actuate (20 ms) = 180 ms total latency. At 5 meters/second, a robot moves 90 centimeters in that time. If it senses an obstacle and needs to stop, it travels nearly a meter before stopping begins.

## Partial Observability: The World is Bigger Than Sensors

Robots have limited sensor range and field of view. They cannot observe everything simultaneously. This is called **partial observability**, and it fundamentally changes how robots must operate.

### Limited Field of View

Cameras typically have 60-120 degree horizontal field of view. A robot can't see behind itself. It can't see around corners. Occlusions (one object blocking another) hide parts of the scene.

**Implication**: Robots must actively move and look around to gather information. Unlike a god's-eye-view simulation, robots must explore and remember.

### Sensor Range Limits

LIDAR might have a 30-meter range. Beyond that, the world is invisible. Cameras lose resolution with distance. Force sensors only detect contact, not proximity.

**Implication**: Robots must navigate closer to sense details, but getting closer risks collision. There's a constant trade-off between information gathering and safety.

### Occlusion and Hidden State

Objects can be hidden behind other objects. A target might be in a drawer, inside a box, or behind furniture. The robot knows it exists (from prior knowledge or instructions) but cannot currently sense it.

**Implication**: Robots need memory and reasoning. They must remember where things were last seen and plan actions that reveal hidden information (open the drawer, move the obstacle).

## Determinism vs Probabilistic Reality

Software is largely deterministic: the same input produces the same output every time (barring bugs or random number generation). Physical robots operate in a probabilistic world where the same action produces different outcomes due to:

- **Sensor Noise**: Measurements vary run-to-run
- **Actuation Variability**: Motors don't produce exactly the same force each time
- **Environmental Changes**: Lighting shifts, objects move, surfaces change
- **Contact Mechanics**: Grasping, pushing, and manipulation involve complex contact dynamics that are chaotic and difficult to predict exactly

**Example**: Command a robot to grasp a pen. Trial 1: Success. Trial 2: Pen rolls away slightly as gripper approaches. Trial 3: Gripper closes 1mm off-center, pen slips out. Trial 4: Success. Same command, different outcomes.

**Implication**: Robot systems must be designed probabilistically. Instead of guaranteeing success, they maximize the probability of success. Control strategies must include error recovery and adaptation.

## Continuous Sensing and Closed-Loop Control

Unlike one-shot perception (classify an image, output a label), robots require **continuous sensing**. The world changes, actions have unintended effects, and adaptation is essential.

### The Control Loop

Robot control follows the Sense-Think-Act-Sense loop continuously:
1. **Sense**: Read sensors to understand current state
2. **Think**: Process data, update world model, plan next action
3. **Act**: Send commands to actuators
4. **Sense** (again): Observe the outcome and adapt

This loop runs at frequencies from 1 Hz (high-level planning) to 1000 Hz (low-level motor control).

### Why Open-Loop Fails

**Open-Loop Control**: Plan a sequence of actions, execute them without feedback, hope for the best.

**Why It Fails**: Actuators have error. The environment is unpredictable. Without feedback, errors compound. A 1-degree error in the first joint creates a 10 cm error at the end-effector. After 5 joints, the robot has no idea where its hand actually is.

### Closed-Loop Control

**Closed-Loop Control**: Continuously measure the outcome of actions and adjust. If the gripper misses the object, sense the miss and try again.

This is robust to disturbances, model errors, and uncertainty. It's why humans can catch a ball even though the throw is never exactly the same twice - we continuously adjust based on visual feedback.

## Why Simulation Comes First

Testing on real robots is:
- **Slow**: Set up hardware, run experiment, analyze, repeat. Maybe 10 trials per hour.
- **Expensive**: Robot wear and tear, broken objects, facility costs.
- **Dangerous**: Fast-moving robots can injure people or damage property.

**Simulation** allows:
- **Rapid Iteration**: Thousands of trials per hour on parallel simulated robots.
- **Safe Exploration**: Try risky behaviors without consequence.
- **Automated Testing**: Run overnight, explore edge cases systematically.
- **Reproducibility**: Exact same initial conditions every time.

### The Reality Gap

But simulation is not perfect. Simulated physics approximates reality. Sensor models are idealized. The **reality gap** is the difference between simulated performance and real-world performance.

Techniques to bridge the gap:
- **Domain Randomization**: Vary simulation parameters to make policies robust
- **Sim-to-Real Transfer**: Train in sim, fine-tune on real robot
- **High-Fidelity Simulation**: Better physics engines (like Isaac Sim) reduce the gap

We'll explore simulation deeply in Module 3.

## Summary

The physical world imposes hard constraints that digital AI never faces:
- Physics is non-negotiable (gravity, inertia, friction)
- Sensors are noisy and incomplete (uncertainty is fundamental)
- Actuators have latency (delays between decision and action)
- Observability is partial (can't see everything at once)
- Outcomes are probabilistic (same action ≠ same result)
- Continuous sensing is required (can't plan once and hope)

These constraints don't make physical AI impossible - they make it different. Understanding these constraints is the first step to building robust robot systems.

In the next chapter, we'll explore how robots are architected to handle these constraints through sensors, compute, and actuators working in harmony.
""",
}

def generate_content(chapter_path, content):
    """Write content to chapter file"""
    file_path = Path(__file__).parent.parent / "Future Ai And Robotics" / "docs" / chapter_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Generated: {chapter_path}")

if __name__ == "__main__":
    print("=== Generating Book Content ===\n")
    
    for chapter_path, content in CHAPTER_CONTENT.items():
        generate_content(chapter_path, content)
    
    print(f"\n✅ Generated {len(CHAPTER_CONTENT)} chapters!")
