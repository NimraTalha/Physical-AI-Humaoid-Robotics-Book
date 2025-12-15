---
id: chapter-2-basics-of-humanoid-robotics
title: Chapter 2 - Basics of Humanoid Robotics
sidebar_label: 2. Basics of Humanoid Robotics
sidebar_position: 2
---

# Chapter 2: Basics of Humanoid Robotics

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand the mechanical structure of humanoid robots.
- Identify key actuator technologies and their trade-offs.
- Explain the role of sensors in humanoid perception and control.
- Describe the fundamentals of robot kinematics and dynamics.

## Introduction

Humanoid robots are designed to mimic the human form and its movements. Their bipedal (two-legged) structure and human-like design enable them to navigate environments and use tools that were created for people.

Building humanoid robots presents unique engineering challenges, such as achieving stable bipedal locomotion, coordinating dozens of joints, and maintaining balance under dynamic conditions.

## Core Concepts

### Mechanical Fundamentals

#### Degrees of Freedom (DOF)

A **degree of freedom** is an independent direction in which a part of the robot can move. Human-like robots typically have:

- **Arms**: 7 DOF per arm (3 in the shoulder, 1 in the elbow, 3 in the wrist)
- **Legs**: 6 DOF per leg (3 in the hip, 1 in the knee, 2 in the ankle)
- **Torso**: 3 DOF (for bending and twisting)
- **Head**: 2-3 DOF (for panning and tilting)

A full humanoid robot can easily have a total of **25-30 DOF**.

#### Kinematic Chains

- **Serial Chain**: A series of joints connected in sequence, like the links in a human arm.
- **Parallel Chain**: A setup where multiple actuators control a single joint, which can increase strength and stability.
- **Closed-Loop Chain**: A structure that forms a closed loop, which is often used in legs to provide better stability.

### Actuator Technologies

Actuators are the components responsible for moving the robot's joints.

#### 1. Electric Motors

**Advantages:**
- Provide precise position control.
- Offer high repeatability for consistent movements.
- Are easy to integrate with digital controllers.

**Types:**
- **DC Brushless Motors**: Known for their high efficiency and long lifespan.
- **Servo Motors**: Come with built-in components for position feedback.
- **Stepper Motors**: Excellent for precise, incremental motion.

#### 2. Hydraulic Actuators

**Advantages:**
- Offer a very high power-to-weight ratio, making them great for heavy lifting.
- Are well-suited for heavy-duty applications.

**Disadvantages:**
- Require a hydraulic pump and careful fluid management.
- Tend to be maintenance-intensive.
- Carry a risk of fluid leaks.

#### 3. Pneumatic Actuators

**Advantages:**
- Are naturally compliant (less rigid), which makes them safer for human interaction.
- Are very lightweight.

**Disadvantages:**
- Offer lower precision compared to electric motors.
- Require a source of compressed air.

### Sensors for Perception and Control

#### Vision Sensors

- **RGB Cameras**: Provide color imaging for object recognition.
- **Depth Cameras** (e.g., Intel RealSense): Used for 3D environment mapping.
- **Stereo Cameras**: Enable depth perception using parallax, similar to human vision.

#### Proprioceptive Sensors

These sensors provide information about the robot's own state.

- **Encoders**: Measure joint angles to provide position feedback.
- **IMU (Inertial Measurement Unit)**: Detects the robot's orientation and acceleration, crucial for balance.
- **Force/Torque Sensors**: Measure the interaction forces at the joints or end-effectors.

#### Tactile Sensors

- **Pressure Sensors**: Detect contact and help control grip force.
- **Skin Sensors**: Provide a sense of touch across the robot's body.

### Kinematics and Dynamics

#### Forward Kinematics

Given a set of joint angles, forward kinematics calculates the position of the robot's end-effector (like its hand).

```
Position = f(θ₁, θ₂, ..., θₙ)
```

**Example**: With the angles of the shoulder, elbow, and wrist joints, you can determine exactly where the hand is in 3D space.

#### Inverse Kinematics

Given a desired position for the end-effector, inverse kinematics calculates the joint angles required to get there.

```
(θ₁, θ₂, ..., θₙ) = f⁻¹(desired position)
```

**Challenge**: This is a much harder problem to solve and can often have multiple solutions or even no solution if the target is outside the robot's reachable workspace.

#### Dynamics

Dynamics govern how forces and torques affect the robot's motion. The primary **equation of motion** is:

```
τ = M(q)q̈ + C(q,q̇)q̇ + G(q)
```

Where:
- **τ**: The joint torques, which are the control inputs.
- **M(q)**: The inertia matrix of the robot.
- **C(q,q̇)**: The Coriolis and centrifugal forces.
- **G(q)**: The gravitational forces.

## Practical Application

### Walking Control

Enabling a humanoid to walk requires solving several problems simultaneously:

1. **Gait Planning**: Defining the trajectory of the feet and the robot's center of mass.
2. **Balance Control**: Keeping the robot's center of pressure within its support polygon (the area formed by its feet).
3. **Compliance**: Allowing the robot to absorb impacts and adapt to uneven terrain.

A key stability criterion for walking is the **Zero Moment Point (ZMP)**, which is the point on the ground where the net moment from gravity and inertial forces is zero.

### Example: Simple Balance Controller

```python
# Pseudocode for balance control
def balance_controller(imu_data, target_orientation):
    error = target_orientation - imu_data.orientation
    torque_correction = PID_control(error)
    apply_torque_to_ankle_joints(torque_correction)
```

This simple controller adjusts the ankle torques to help the robot maintain an upright posture.

## Summary

Humanoid robots combine mechanical design, actuation, sensing, and control to achieve human-like motion. The field draws on mechanical engineering, control theory, and AI to create machines that can successfully navigate and interact with human environments.

**Key Takeaways:**
- Humanoids have 25-30 degrees of freedom to mimic human motion.
- The choice of actuator (electric, hydraulic, or pneumatic) involves trade-offs in power, precision, and safety.
- Sensors provide crucial feedback for perception (vision) and control (encoders, IMUs).
- Kinematics and dynamics are mathematical tools that are essential for planning and executing motion.

## Further Reading

- **Books**:
  - *Humanoid Robotics: A Reference* by Ambarish Goswami and Prahlad Vadakkepat
  - *Introduction to Robotics: Mechanics and Control* by John J. Craig

- **Research Papers**:
  - "Bipedal Walking Control Based on Capture Point Dynamics" (IROS 2011)
  - "Atlas: A Hydraulic Humanoid Robot" by Boston Dynamics

- **Online Resources**:
  - [NASA Valkyrie Robot](https://www.nasa.gov/feature/valkyrie)
  - [Unitree Robotics H1](https://www.unitree.com/h1)
  - [Open Dynamics Engine (ODE) Tutorial](https://www.ode.org/)
