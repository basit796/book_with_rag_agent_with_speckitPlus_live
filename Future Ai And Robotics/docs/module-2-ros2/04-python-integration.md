---
sidebar_position: 4
title: Python Agents and ROS
---

# Python Agents and ROS

## Why Python for Robotics?

Python is widely used in robotics because it's:
- **Rapid prototyping**: Quick iteration for testing algorithms
- **Rich ecosystem**: NumPy, OpenCV, PyTorch, scikit-learn readily available
- **Readable**: Clear syntax reduces bugs
- **ROS 2 support**: First-class Python client library (`rclpy`)

For performance-critical code (control loops, perception pipelines), C++ is preferred. Most robots use both: C++ for low-level control, Python for high-level logic.

## Creating a ROS 2 Python Node

Minimal node structure:

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        self.get_logger().info('Node started')

def main():
    rclpy.init()
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

**Key components**:
- `rclpy.init()`: Initialize ROS 2 context
- `Node` class: Base for all nodes  
- `rclpy.spin()`: Process callbacks (subscriptions, timers, services)
- Cleanup: destroy node, shutdown

## Publishers and Subscribers

**Publisher example** (camera simulator):
```python
from sensor_msgs.msg import Image

class CameraNode(Node):
    def __init__(self):
        super().__init__('camera')
        self.pub = self.create_publisher(Image, '/camera/image', 10)
        self.timer = self.create_timer(0.033, self.publish_image)  # 30 Hz
    
    def publish_image(self):
        msg = Image()
        # Fill msg with image data
        self.pub.publish(msg)
```

**Subscriber example** (object detector):
```python
class DetectorNode(Node):
    def __init__(self):
        super().__init__('detector')
        self.sub = self.create_subscription(
            Image, '/camera/image', self.image_callback, 10)
    
    def image_callback(self, msg):
        # Process image, detect objects
        self.get_logger().info('Received image')
```

## Integrating AI Models

Common pattern: Load PyTorch/TensorFlow model in node, run inference on sensor data.

**Object detection example**:
```python
import torch
from torchvision.models import detection

class AIDetectorNode(Node):
    def __init__(self):
        super().__init__('ai_detector')
        self.model = detection.fasterrcnn_resnet50_fpn(pretrained=True)
        self.model.eval()
        
        self.sub = self.create_subscription(Image, '/camera/image', self.detect, 10)
        self.pub = self.create_publisher(DetectionArray, '/detections', 10)
    
    def detect(self, msg):
        # Convert ROS Image to tensor
        img_tensor = self.ros_to_tensor(msg)
        
        # Run inference
        with torch.no_grad():
            predictions = self.model([img_tensor])
        
        # Publish detections
        det_msg = self.to_detection_msg(predictions)
        self.pub.publish(det_msg)
```

## NumPy and OpenCV Integration

ROS 2 images can be converted to NumPy arrays using `cv_bridge`:

```python
from cv_bridge import CvBridge

bridge = CvBridge()

def image_callback(self, msg):
    # ROS Image -> NumPy array
    cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
    
    # Process with OpenCV
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    
    # NumPy array -> ROS Image
    edge_msg = bridge.cv2_to_imgmsg(edges, encoding='mono8')
    self.pub.publish(edge_msg)
```

## Best Practices

1. **Use classes**: Inherit from `Node` for clean organization
2. **Descriptive names**: Clear node/topic names aid debugging
3. **QoS profiles**: Match communication patterns (sensor data vs commands)
4. **Logging**: Use `self.get_logger()` instead of `print()`
5. **Shutdown handling**: Clean up resources in `destroy_node()`
6. **Avoid blocking**: Long computations block callbacks; use threading or separate processes

## Summary

Python + ROS 2 enables rapid development of robot software. Use `rclpy` for nodes, publishers/subscribers, services, and actions. Integrate AI models (PyTorch/TensorFlow), computer vision (OpenCV), and numerical computing (NumPy) seamlessly.

For real-time control, use C++. For high-level logic and AI integration, Python excels.

Next module: Simulation and why it's essential before deploying to real hardware.
