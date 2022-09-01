# SLAMbot

<img src="assets/bot.png?raw=true" />

<img src="assets/ui.png?raw=true" />

# Features
 - RPI 4 + RPI CAM + Infrared + Steerable Head + Ultrasonic. Freenove 4WD Kit.
 - Source code gotten from the kit, gutted and reworked to be more pythonic and interface with my additions.
 - Implemented and Tested Line Following Algorithm w/ Camera using ROS(Robot Operating System), then ported it over. [Link](https://github.com/owolabioromidayo/line_follower)
 - Person Detection and Tracking using a wrapper for YOLOv4. The model is VERY slow on the Rpi tho.
 - Web Teleoperation Interface with Camera Stream and Overlays using Flask (as shown in image above). The overlays are for Line Following (a yellow circle in the direction of the line) and Person tracking ( a green circle on the person being tracked).
 
 
# Next Steps
 - Implementing Monocular Visual SLAM (Simultaneous Localization and Mapping) from scratch as ROS doesnt give me enough control or understanding. I'm thinking of writing SLAM but i dont think this robot can carry it. I can set up a stream server from my PC and relay info ( this can also be applied to the YoLo problem), but my internet is too slow for that. 
<br/> (Might discard this if i find better things to do w/ my time. There are so many impls of SLAM already).
