# Feature Specification: Module 4 - The AI-Robot Brain (NVIDIA Isaac)

**Feature Branch**: `001-isaac-brain`  
**Created**: 2025-12-20  
**Status**: Draft  
**Input**: User description: "Create a detailed feature specification for Module 4: The AI-Robot Brain (NVIDIA Isaac) for a book on humanoid robotics"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Understanding AI-Driven Robotics Fundamentals (Priority: P1)

A reader with knowledge of ROS 2 and simulation (from Modules 2-3) needs to understand how modern AI transforms robotics—specifically how perception, mapping, and navigation work as integrated systems rather than isolated algorithms. They need to grasp why photorealistic simulation matters for AI training and how synthetic data generation enables rapid AI development.

**Why this priority**: This is the foundational mental model shift for the entire module. Without understanding "perception as a pipeline" and "AI-driven autonomy," readers cannot progress to later chapters or modules. This establishes the "why Isaac" answer and positions AI as the brain's infrastructure.

**Independent Test**: Reader can explain to a non-technical friend: (1) why robots need AI-driven perception beyond traditional computer vision, (2) why photorealistic simulation helps train AI models, and (3) what synthetic data is and why it's valuable. Reader can sketch a simple perception pipeline showing preprocessing, inference, and post-processing stages.

**Acceptance Scenarios**:

1. **Given** reader understands ROS 2 topics and simulation basics, **When** they read Chapter 1 on "Why AI Needs Better Simulation," **Then** they can articulate the domain gap problem and explain how photorealism and synthetic data reduce it
2. **Given** reader knows traditional computer vision exists, **When** they learn about AI-based perception pipelines, **Then** they can contrast rule-based CV with learning-based approaches and explain trade-offs
3. **Given** reader understands what sensors produce (images, point clouds), **When** they encounter perception pipeline concepts, **Then** they can describe the flow from raw sensor data through preprocessing, model inference, and post-processing to actionable outputs
4. **Given** reader has seen Gazebo simulations, **When** they learn about Isaac Sim's photorealism and RTX rendering, **Then** they can explain why visual fidelity matters for training vision-based AI models

---

### User Story 2 - Navigating the Isaac Ecosystem (Priority: P2)

A reader preparing to integrate AI into robotic systems needs to understand the Isaac ecosystem's components—Isaac Sim, Isaac ROS, and Isaac Lab—and their distinct roles. They must understand how these tools fit together, how they integrate with ROS 2, and when to use each component. They need conceptual clarity without implementation-level details.

**Why this priority**: Once readers understand why AI matters (P1), they need to understand the tooling landscape. This knowledge is prerequisite for comprehending perception and navigation pipelines (P3-P4) and sets up future modules on VLA and sim-to-real transfer. Without ecosystem clarity, readers will confuse tools and misunderstand their integration points.

**Independent Test**: Reader can draw a diagram showing Isaac Sim, Isaac ROS, and Isaac Lab with their relationships to ROS 2 and explain each component's purpose in 2-3 sentences. Reader can answer: "When would I use Isaac Sim vs Gazebo?" and "What does Isaac ROS accelerate?" with concrete examples.

**Acceptance Scenarios**:

1. **Given** reader understands simulation concepts from Module 3, **When** they learn about Isaac Sim, **Then** they can explain Omniverse, USD format, and RTX rendering at a conceptual level and compare Isaac Sim to Gazebo
2. **Given** reader knows ROS 2 nodes and topics, **When** they encounter Isaac ROS, **Then** they can explain how Isaac ROS provides GPU-accelerated perception nodes that integrate with standard ROS 2 systems
3. **Given** reader understands the ecosystem structure, **When** they see Isaac Lab mentioned, **Then** they can explain its role in RL and policy training (without implementation details)
4. **Given** reader knows both Isaac components, **When** asked about integration, **Then** they can describe how Isaac Sim generates synthetic data, Isaac ROS processes it in real-time, and results flow through ROS 2 topics

---

### User Story 3 - Understanding Perception Pipelines (Priority: P3)

A reader designing or evaluating AI-driven robotic systems needs to understand perception as a multi-stage pipeline involving preprocessing, model inference, and post-processing. They must grasp object detection, semantic segmentation, pose estimation, and sensor fusion at a system architecture level—not algorithm implementation—and understand how Isaac ROS accelerates these pipelines through GPU optimization.

**Why this priority**: Perception is the robot's primary interface with the world. Understanding perception pipelines prepares readers for navigation (P4) and advanced AI modules (P5). This knowledge enables reasoning about system performance, failure modes, and integration points. Must follow ecosystem understanding (P2) to contextualize Isaac ROS's role.

**Independent Test**: Reader can sketch a perception pipeline diagram showing: sensor input → preprocessing → model inference → post-processing → semantic output (e.g., detected objects, segmentation masks). Reader can explain why perception is a pipeline, not just "running a model," and identify at least two failure points in the pipeline with mitigation strategies.

**Acceptance Scenarios**:

1. **Given** reader understands camera and LiDAR sensor outputs, **When** they learn about perception pipelines, **Then** they can describe preprocessing steps (calibration, filtering, normalization) and why they matter
2. **Given** reader knows AI models exist, **When** they encounter object detection and segmentation in context, **Then** they can explain what these models output (bounding boxes, masks, confidence scores) and how robots use this information
3. **Given** reader understands single-sensor perception, **When** they learn about sensor fusion, **Then** they can explain why combining camera and LiDAR improves robustness and describe conceptual fusion approaches
4. **Given** reader knows standard perception pipelines, **When** they learn about Isaac ROS, **Then** they can explain how GPU acceleration reduces latency and increases throughput without implementation details
5. **Given** reader understands perception outputs, **When** presented with failure scenarios (occlusions, lighting changes, novel objects), **Then** they can reason about why failures occur and conceptual mitigation strategies

---

### User Story 4 - Understanding Mapping and Navigation Systems (Priority: P4)

A reader architecting autonomous robotic systems needs to understand VSLAM (Visual Simultaneous Localization and Mapping), navigation stacks like Nav2, and how perception, localization, planning, and control integrate into autonomous navigation. They must understand maps as probabilistic beliefs, navigation as planning under uncertainty, and common failure modes—all at a system reasoning level without mathematical algorithm details.

**Why this priority**: Navigation synthesizes perception (P3) with decision-making and represents the culmination of Module 4's content. Understanding navigation prepares readers for VLA integration (Module 6) where language-guided navigation emerges. Must follow perception (P3) since navigation depends on perception outputs.

**Independent Test**: Reader can draw a navigation system diagram showing: perception → localization → global planning → local planning → control, with feedback loops. Reader can explain the SLAM loop closure problem conceptually and describe two scenarios where navigation might fail with root cause analysis.

**Acceptance Scenarios**:

1. **Given** reader understands perception outputs, **When** they learn about VSLAM, **Then** they can explain how robots simultaneously build maps and localize within them at a conceptual level
2. **Given** reader knows maps are created, **When** they learn about probabilistic mapping, **Then** they can explain why maps contain uncertainty and how this affects navigation decisions
3. **Given** reader understands localization basics, **When** they encounter Nav2 architecture, **Then** they can describe the navigation pipeline: global planner (path from A to B), costmaps (obstacle representation), local planner (dynamic obstacle avoidance), and controllers
4. **Given** reader understands navigation components, **When** presented with failure cases (dynamic obstacles, loop closure failures, kidnapped robot problem), **Then** they can reason about root causes and explain why navigation is challenging
5. **Given** reader knows navigation requires perception, **When** they see full system integration, **Then** they can trace data flow from camera images through perception and localization to path planning and motor commands
6. **Given** reader understands Module 4 content, **When** asked about preparation for future modules, **Then** they can explain how navigation foundations enable VLA-guided autonomy and sim-to-real transfer

---

### User Story 5 - Evaluating Synthetic Data Generation Strategies (Priority: P5)

A technical decision-maker or advanced reader needs to understand synthetic data generation's advantages, limitations, and trade-offs. They must grasp domain randomization, photorealism vs diversity, automatic labeling, and when synthetic data reduces (but doesn't eliminate) real-world data needs. This knowledge informs decisions about simulation investments and AI training strategies.

**Why this priority**: This is advanced strategic knowledge building on foundational concepts (P1-P4). While important for technical decision-makers, casual readers can defer this. It bridges Module 4 to Module 7 (sim-to-real transfer) but isn't prerequisite for Module 5-6.

**Independent Test**: Reader can evaluate a synthetic data generation proposal and identify: (1) what makes synthetic data valuable here, (2) what domain gaps remain, (3) what diversity strategies are needed, and (4) how much real data is still required. Reader can compare two sim-to-real approaches and recommend one with justification.

**Acceptance Scenarios**:

1. **Given** reader understands photorealistic simulation, **When** they learn about synthetic data generation, **Then** they can explain automatic labeling and calculate effort savings compared to manual annotation
2. **Given** reader knows synthetic data exists, **When** they encounter domain randomization, **Then** they can explain texture, lighting, and object variation strategies and why diversity matters as much as realism
3. **Given** reader understands domain gap concepts, **When** evaluating synthetic-only training, **Then** they can identify failure modes and explain when real-world data is still essential
4. **Given** reader knows Module 4 content, **When** planning a robotics AI project, **Then** they can outline a synthetic data strategy balancing photorealism, diversity, and real-world validation

---

### Edge Cases

- **Perception failure recovery**: What happens when all perception models fail simultaneously (e.g., complete sensor occlusion or adversarial conditions)? How should navigation systems respond?
- **SLAM in symmetrical environments**: How does VSLAM handle environments with repetitive patterns (e.g., long hallways, warehouses) where loop closure becomes ambiguous?
- **Map staleness**: What happens when the environment changes significantly after map creation (furniture moved, construction)? How long can a map remain valid?
- **GPU resource contention**: How do multiple Isaac ROS perception pipelines share limited GPU resources? What happens under resource exhaustion?
- **Sim-to-real lighting gaps**: When does photorealistic training still fail in real-world deployment due to lighting conditions not present in simulation?
- **Navigation in crowds**: How do navigation stacks handle highly dynamic environments with many moving obstacles (humans, other robots)? When do traditional planners break down?
- **Sensor calibration drift**: What happens when camera or LiDAR calibration degrades over time? How does this affect perception and SLAM accuracy?
- **Partial map scenarios**: How does a robot navigate when only partial maps are available or when transitioning between mapped and unmapped regions?

## Requirements *(mandatory)*

### Functional Requirements

#### Chapter 1: Why AI Needs Better Simulation

- **FR-001**: Content MUST explain the domain gap problem (sim-to-real transfer) using concrete examples from visual perception
- **FR-002**: Content MUST contrast traditional computer vision (rule-based, hand-crafted features) with AI-based perception (learned features, data-driven)
- **FR-003**: Content MUST explain photorealism's role in training vision-based AI models with visual comparisons
- **FR-004**: Content MUST define synthetic data and demonstrate automatic labeling advantages (effort, cost, scale)
- **FR-005**: Content MUST include thought experiment: generating 1 million labeled images in simulation vs real world
- **FR-006**: Content MUST address misconception: "photorealism = perfect simulation" by explaining physics accuracy and diversity also matter
- **FR-007**: Content MUST prepare reader for Isaac ecosystem introduction by establishing "why better simulation matters for AI"
- **FR-008**: Content MUST include visual comparison: synthetic vs real images with labels (bounding boxes, segmentation masks)

#### Chapter 2: Isaac Sim Overview

- **FR-009**: Content MUST explain NVIDIA Omniverse platform at a conceptual level (collaborative simulation, USD format)
- **FR-010**: Content MUST explain USD (Universal Scene Description) as a scene representation standard without implementation details
- **FR-011**: Content MUST explain RTX rendering and ray tracing's role in photorealism at a conceptual level
- **FR-012**: Content MUST clearly distinguish Isaac Sim, Isaac ROS, and Isaac Lab roles and relationships
- **FR-013**: Content MUST compare Isaac Sim vs Gazebo across: photorealism, physics accuracy, AI-specific features, and ecosystem integration
- **FR-014**: Content MUST explain "physics-for-AI" (e.g., contact-rich manipulation, soft-body simulation) without mathematical details
- **FR-015**: Content MUST address "when to use Isaac Sim" vs "when Gazebo suffices" with decision criteria
- **FR-016**: Content MUST explain Isaac Sim's integration with ROS 2 at a system architecture level
- **FR-017**: Content MUST include ecosystem diagram showing Isaac Sim, Isaac ROS, Isaac Lab, ROS 2, and data flows
- **FR-018**: Content MUST reference Module 3 (simulation fundamentals) and show progression to AI-driven simulation

#### Chapter 3: Isaac ROS Pipelines

- **FR-019**: Content MUST define perception pipeline with three stages: preprocessing, inference, post-processing
- **FR-020**: Content MUST explain object detection outputs (bounding boxes, class labels, confidence scores) and use cases
- **FR-021**: Content MUST explain semantic segmentation outputs (per-pixel class labels) and use cases
- **FR-022**: Content MUST explain pose estimation (6DoF: position + orientation) and use cases in manipulation
- **FR-023**: Content MUST explain sensor fusion combining camera and LiDAR data at a conceptual level
- **FR-024**: Content MUST explain GPU acceleration benefits: reduced latency, increased throughput, real-time performance
- **FR-025**: Content MUST show Isaac ROS integration with standard ROS 2 systems (topics, nodes, message types)
- **FR-026**: Content MUST include perception pipeline diagram showing data flow from sensors through processing stages
- **FR-027**: Content MUST include case study: Isaac ROS perception pipeline performance (latency, FPS) compared to CPU-based alternatives
- **FR-028**: Content MUST explain perception failure modes: occlusions, lighting changes, novel objects, adversarial conditions
- **FR-029**: Content MUST address misconception: "one perception model solves all problems" by explaining pipeline integration and fusion
- **FR-030**: Content MUST prepare reader for navigation by showing perception as input to localization and planning

#### Chapter 4: Mapping & Navigation

- **FR-031**: Content MUST explain VSLAM (Visual Simultaneous Localization and Mapping) at a system level without mathematical algorithms
- **FR-032**: Content MUST explain loop closure problem in SLAM with visual examples and failure cases
- **FR-033**: Content MUST explain maps as probabilistic beliefs (uncertainty, confidence) rather than ground truth
- **FR-034**: Content MUST explain Nav2 architecture: global planner, local planner, costmaps, recovery behaviors
- **FR-035**: Content MUST explain costmaps as obstacle representations combining static maps and dynamic sensor data
- **FR-036**: Content MUST explain path planning vs trajectory planning distinction
- **FR-037**: Content MUST explain localization methods (particle filters concept) without implementation details
- **FR-038**: Content MUST show navigation as integrated system: perception → localization → planning → control with feedback loops
- **FR-039**: Content MUST include navigation decision flow diagram: sensor data through perception, localization, planning, to motor commands
- **FR-040**: Content MUST include SLAM failure case studies: symmetrical environments, dynamic objects, lighting changes, kidnapped robot
- **FR-041**: Content MUST include navigation scenario: robot with partial map uncertainty, demonstrating probabilistic reasoning
- **FR-042**: Content MUST address misconception: "SLAM produces perfect maps" by explaining error accumulation and drift
- **FR-043**: Content MUST address misconception: "navigation is just pathfinding" by explaining localization, planning, control integration
- **FR-044**: Content MUST prepare reader for VLA integration (Module 6) by explaining navigation as foundation for language-guided autonomy
- **FR-045**: Content MUST explain recovery behaviors when navigation fails (e.g., clearing costmaps, rotating in place)

#### Cross-Chapter Integration & Pedagogy

- **FR-046**: Content MUST maintain consistent terminology across all chapters with glossary references
- **FR-047**: Each chapter MUST reference previous module concepts (Physical AI, ROS 2, simulation) showing progression
- **FR-048**: Each chapter MUST include learning objectives and success criteria at chapter start
- **FR-049**: Content MUST use consistent visual style for diagrams (perception pipelines, navigation stacks, ecosystem architecture)
- **FR-050**: Content MUST include "Common Misconceptions" section in each chapter addressing specific false beliefs
- **FR-051**: Content MUST include "Connection to Previous Modules" and "Preview of Next Modules" in each chapter
- **FR-052**: Content MUST balance NVIDIA-specific tools (Isaac) with general AI-robotics concepts (perception, SLAM, Nav2)
- **FR-053**: Content MUST avoid CUDA code, GPU kernel details, deep learning training code, and deployment instructions
- **FR-054**: Content MUST remain accessible to readers without GPU programming expertise
- **FR-055**: Content MUST use analogies and thought experiments to explain abstract concepts (e.g., maps as beliefs)

#### Synthetic Data Generation (Integrated Across Chapters)

- **FR-056**: Content MUST explain domain randomization: texture, lighting, object placement variation
- **FR-057**: Content MUST explain diversity vs photorealism trade-off in synthetic data generation
- **FR-058**: Content MUST explain automatic labeling for object detection, segmentation, depth, pose
- **FR-059**: Content MUST address when synthetic data reduces (but doesn't eliminate) real-world data needs
- **FR-060**: Content MUST include example calculation: effort/cost savings of synthetic vs manually labeled data
- **FR-061**: Content MUST explain sim-to-real gap and mitigation strategies conceptually (deferred to Module 7 for details)

#### Visual & Diagram Requirements

- **FR-062**: Content MUST include Isaac ecosystem diagram (Sim, ROS, Lab, ROS 2, relationships)
- **FR-063**: Content MUST include perception pipeline diagram (sensor → preprocess → inference → post-process → output)
- **FR-064**: Content MUST include navigation system diagram (perception → localization → global planner → local planner → control)
- **FR-065**: Content MUST include Nav2 architecture diagram with component relationships
- **FR-066**: Content MUST include VSLAM concept diagram showing mapping and localization simultaneously
- **FR-067**: Content MUST include synthetic vs real image comparison with labels
- **FR-068**: Content MUST include sensor fusion concept diagram (camera + LiDAR → fused representation)
- **FR-069**: All diagrams MUST be technology-agnostic where possible, showing concepts not implementations

#### Reader Engagement & Assessment

- **FR-070**: Each chapter MUST include thought experiments for active reader engagement
- **FR-071**: Each chapter MUST include case studies or scenarios demonstrating concepts
- **FR-072**: Content MUST include "Check Your Understanding" questions at chapter end testing conceptual knowledge
- **FR-073**: Content MUST include failure analysis scenarios where readers reason about root causes
- **FR-074**: Module MUST conclude with "Module 4 Synthesis" connecting all chapters and previewing Module 5+

### Key Entities

- **Isaac Sim**: Photorealistic simulation environment built on Omniverse, using USD for scene description and RTX for rendering. Primary use: synthetic data generation for AI training and testing AI-driven robotics systems.

- **Isaac ROS**: GPU-accelerated perception and AI pipeline components that integrate with ROS 2. Includes object detection, segmentation, pose estimation, VSLAM, and sensor processing nodes optimized for real-time performance.

- **Isaac Lab**: Reinforcement learning framework for robot policy training in simulation. Mentioned for ecosystem completeness; detailed coverage deferred to later modules.

- **Perception Pipeline**: Multi-stage data processing flow transforming raw sensor data (images, point clouds) into semantic understanding (objects, segmentation, poses). Stages: preprocessing (calibration, filtering) → inference (AI model) → post-processing (NMS, tracking).

- **VSLAM System**: Visual Simultaneous Localization and Mapping system that uses camera images to build environment maps while localizing robot within those maps. Includes feature extraction, map management, loop closure detection, and pose estimation.

- **Nav2 Stack**: ROS 2 navigation framework including global planners (path planning), local planners (dynamic obstacle avoidance), costmaps (obstacle representation), localization, and recovery behaviors.

- **Costmap**: Probabilistic grid representation of environment obstacles combining static map data and dynamic sensor inputs. Used by planners to compute collision-free paths. Includes layers: static, obstacle, inflation.

- **Synthetic Data**: Automatically labeled training data generated in simulation. Includes images with bounding boxes, segmentation masks, depth maps, pose annotations. Enables large-scale data generation without manual labeling.

- **Domain Gap**: Difference between simulated and real-world data distributions causing AI models to underperform when deployed. Mitigation strategies: photorealism, domain randomization, real-world fine-tuning.

- **Loop Closure**: SLAM process of recognizing previously visited locations to correct accumulated drift and improve map consistency. Failure cases: symmetrical environments, perceptual aliasing, lighting changes.

### Assumptions

- **Assumption 1**: Readers have completed Modules 1-3 and understand Physical AI concepts, ROS 2 architecture, and simulation fundamentals
- **Assumption 2**: Readers are familiar with basic sensor types (cameras, LiDAR, IMU) and their outputs from Module 3
- **Assumption 3**: Readers have conceptual understanding of machine learning (models, training, inference) but not deep learning specifics
- **Assumption 4**: Module focuses on conceptual understanding; implementation details deferred to practical tutorials outside main book content
- **Assumption 5**: NVIDIA Isaac ecosystem is used as primary example, but general AI-robotics concepts are applicable to other platforms
- **Assumption 6**: Readers do not have GPU programming experience; content avoids CUDA and low-level optimization details
- **Assumption 7**: Mathematical formulations (SLAM algorithms, Bayesian filters) are avoided in favor of system-level reasoning
- **Assumption 8**: Readers will not deploy to real hardware in this module; focus is on simulation-based understanding
- **Assumption 9**: VLA (Vision-Language-Action) integration and sim-to-real transfer are explicitly deferred to Modules 6-7
- **Assumption 10**: Diagrams and visuals are essential for comprehension; text-only explanations are insufficient for pipeline and system architecture concepts

## Success Criteria *(mandatory)*

### Measurable Outcomes

**Chapter 1: Why AI Needs Better Simulation**

- **SC-001**: 90% of readers can explain the domain gap problem using a concrete example (e.g., lighting differences between sim and real)
- **SC-002**: 85% of readers can contrast traditional CV and AI-based perception with at least two distinguishing characteristics
- **SC-003**: 95% of readers can define synthetic data and name two advantages over real-world data collection
- **SC-004**: Reader can complete thought experiment (1M labeled images) in under 5 minutes with reasonable cost/effort estimates

**Chapter 2: Isaac Sim Overview**

- **SC-005**: 90% of readers can distinguish Isaac Sim, Isaac ROS, and Isaac Lab roles in 2-3 sentences each
- **SC-006**: 85% of readers can compare Isaac Sim vs Gazebo across three dimensions (photorealism, physics, AI features)
- **SC-007**: 80% of readers can explain USD and Omniverse at a conceptual level without implementation details
- **SC-008**: Reader can sketch Isaac ecosystem diagram showing components and relationships in under 10 minutes
- **SC-009**: Reader can answer "When should I use Isaac Sim vs Gazebo?" with decision criteria

**Chapter 3: Isaac ROS Pipelines**

- **SC-010**: 95% of readers can sketch a perception pipeline with three stages (preprocess, inference, post-process)
- **SC-011**: 90% of readers can explain object detection, segmentation, and pose estimation use cases
- **SC-012**: 85% of readers can explain why sensor fusion improves robustness over single-sensor perception
- **SC-013**: 80% of readers can name two perception failure modes and explain one mitigation strategy
- **SC-014**: Reader can describe Isaac ROS role in GPU acceleration without mentioning CUDA or kernel details
- **SC-015**: Reader can trace data flow from camera through Isaac ROS pipeline to ROS 2 topic output

**Chapter 4: Mapping & Navigation**

- **SC-016**: 90% of readers can explain VSLAM conceptually (simultaneous mapping and localization) without mathematics
- **SC-017**: 85% of readers can describe the loop closure problem and why it's challenging
- **SC-018**: 90% of readers can explain maps as probabilistic beliefs rather than ground truth
- **SC-019**: 85% of readers can describe Nav2 architecture with at least three components (global planner, local planner, costmaps)
- **SC-020**: 80% of readers can sketch navigation system diagram showing perception → localization → planning → control
- **SC-021**: 90% of readers can analyze a navigation failure scenario and identify root cause (e.g., localization error, dynamic obstacle)
- **SC-022**: Reader can explain why navigation is more than pathfinding with two additional required capabilities

**Cross-Chapter & Module Integration**

- **SC-023**: 90% of readers can verbally explain AI perception and navigation concepts to a non-technical friend in under 3 minutes
- **SC-024**: 85% of readers can connect Module 4 concepts to previous modules (Physical AI, ROS 2, simulation) with specific examples
- **SC-025**: 80% of readers can anticipate how Module 4 prepares for Module 6 (VLA) and Module 7 (sim-to-real)
- **SC-026**: Reader completes module in 4-6 hours with full conceptual understanding (not skimming)
- **SC-027**: 75% of readers report increased confidence in discussing AI-robotics systems in technical contexts
- **SC-028**: Reader can evaluate an AI-robotics system design proposal and identify potential issues in perception or navigation

**Content Quality & Accessibility**

- **SC-029**: Zero instances of CUDA code, GPU kernel details, or deep learning training implementation
- **SC-030**: All diagrams render clearly and support understanding without requiring external references
- **SC-031**: Terminology is consistent across all chapters with glossary support
- **SC-032**: 90% of readers without GPU expertise report content is accessible and understandable
- **SC-033**: Each chapter includes at least two thought experiments or case studies for active engagement
- **SC-034**: "Check Your Understanding" questions at chapter end have 80%+ correct response rate

**Synthetic Data Understanding**

- **SC-035**: 85% of readers can explain domain randomization and its purpose in synthetic data generation
- **SC-036**: 80% of readers can articulate when synthetic data reduces (but doesn't eliminate) real-world data needs
- **SC-037**: Reader can estimate effort savings from synthetic data generation for a sample perception task

**Advanced Reasoning (Optional for Advanced Readers)**

- **SC-038**: Advanced readers (30%) can evaluate trade-offs between photorealism and diversity in synthetic data strategies
- **SC-039**: Advanced readers can reason about multi-stage perception-navigation-control system failures and propagation effects
- **SC-040**: Advanced readers can propose mitigation strategies for at least three edge cases (SLAM in symmetrical environments, sensor occlusion, map staleness)
