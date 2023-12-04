# Griffin: Drone-Car-Collaboration

This is the official implementation for our paper titled "Griffin: Real-time Road Event Detection by Collaborative UAV and Ground Vehicle" (in-progress)

[[Paper]](https://drive.google.com/file/d/1uCIxh5hbrb4kFi26-uINK4sL9AW1DUMA/view?usp=drive_link)

# Description

Autonomous Vehicles rely heavily on sensing the environment for movement guidance and event detection. Yet, their sensing capabilities may be restricted, potentially compromising accuracy and response time leading to hazardous accidents. It is observed that UAV provides more flexible and comprehensive view, but suffer from limited resources and have never been used to guide ground vehicles in a real-time fashion.  To mitigate and solve the above, we introduces Griffin, a novel system that achieves Real-time Road Event Detection by utilizing the resources of a pair of drone and ground vehicle in a collaborative fashion. Our contributions are as follows: 1) we collect a dataset of 350 bird-eye view, road trajectory video clips, to emulate dissimilar lighting, flight settings, weather, and road conditions; We use offline algorithms to assist human annotation and build the ground truth for the collected dataset; 2) we introduce a partitioning-based distributed image processing approach, which adapts to the dynamic network condition and drone resource status and detects road events in a latency/accuracy -optimal fashion; 3) we implement the griffin system and measure its performance in real-world usage scenario and using our dataset. We evaluate the system's performance in terms of its latency, energy consumption, and accuracy, by deploying it on a Jetson Nano as the drone's process unit and an edge server as the road side unit or the car-mounted computer. Our results show that compared with ground-vehicle-based sensing, Griffin can improve the responding time for event detection by xxx percent, while causing a insignificant impact on the drone's flight time.

# System Overview

<div align="center">
<img src="https://github.com/kiran-collab/Griffin-Drone-Car-Collaboration/assets/75129341/cdb370eb-bb3c-457e-adc1-40f5bf48aebf" >
</div>

# Modules

The following are the modules that are in development. The module implementations can be found in their respective folders.
1. Speed Detection of Ground Vehicles in Birdview datasets

_We use Yolo-V8 for tracking Ground Vehicles in Birdview trajectory datasets, followed by speed detection of the corresponding vehicles_

![speed detection-gif](https://github.com/kiran-collab/Griffin-Drone-Car-Collaboration/assets/75129341/d6309ca1-d67e-4f9a-9277-3020c0e3e1f0)

2. Speed Detection of Drone

_Using Lucas-Kanade optical flow approach, we calculate the speed of drone from the video stream_

3. Frame partitioning and model offloading

_An offline demonstration of the basic concept of frame partitioning combined with model offloading_

4. Energy consumption estimation for JetsonNano device

_We take inspiration from [[Jeston Power]](https://github.com/opendr-eu/jetson_power) for measuring the energy consumption of JetsonNanoTx2 that is mounted on-top of drone_


