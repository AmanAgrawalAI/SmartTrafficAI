
SmartTrafficAI
🚦 AI-Based Intelligent Traffic Management & Emergency Vehicle Detection System

SmartTrafficAI is a Computer Vision–based intelligent traffic management system built using Python, YOLO, OpenCV, and EasyOCR.

The system analyzes live traffic video, detects vehicles in multiple lanes, prioritizes emergency vehicles, detects license plates, and dynamically selects the appropriate traffic signal based on traffic congestion.

🎯 Project Features
🚑 Detects emergency vehicles such as Ambulance, Fire Truck, and Police vehicles
🚗 Detects and counts vehicles in Left, Middle, and Right lanes
🚨 Automatically gives priority to the lane containing an emergency vehicle
🚦 Dynamically controls traffic signals based on lane congestion
🟢 Gives an emergency lane a longer green signal duration
🟡 Assigns a waiting/yellow signal to the medium-priority lane
🔴 Stops lower-priority lanes when required
🔢 Detects vehicle license plates using a YOLO model
📝 Reads detected license plate text using EasyOCR
📊 Displays live vehicle count, active lane, green time, lane status, and emergency status
🧠 How It Works
1. Vehicle & Emergency Vehicle Detection

The system uses a custom YOLO model to detect traffic vehicles and emergency vehicles from video frames.

Emergency classes include:

Ambulance
Fire Truck
Police

When an emergency vehicle is detected, its lane is identified and given immediate traffic priority.

2. Lane-Based Vehicle Counting

The video frame is divided into three lanes:

LEFT
MIDDLE
RIGHT

Each detected vehicle is assigned to a lane based on the horizontal position of its bounding-box center.

The system then counts the number of vehicles in each lane.

3. Emergency Priority System

If an emergency vehicle is detected:

The emergency vehicle's lane receives priority
The corresponding signal changes to EMERGENCY GO
Green signal time is set to 45 seconds
Other lanes remain stopped

This helps create a clear path for emergency vehicles.

4. Intelligent Traffic Management

When no emergency vehicle is present, the system compares the number of vehicles in all three lanes.

Highest traffic lane → 🟢 GO
Medium traffic lane → 🟡 WAIT
Remaining lane → 🔴 STOP

The normal green signal duration is set to 25 seconds in the current implementation.

5. License Plate Detection & OCR

A separate YOLO model detects license plate regions.

The detected license plate is then:

Cropped from the video frame
Processed using EasyOCR
Restricted to alphanumeric characters
Displayed with the detected text and confidence score
🛠️ Tech Stack
Python
OpenCV
Ultralytics YOLO
EasyOCR
📂 Project Files
SmartTrafficAI/
│
├── main.py
├── New_emergency-best.pt
├── license_plate_best.pt
│
└── videos/
    └── traffic.mp4

Note: The YOLO model files and video file should be placed in the appropriate paths before running the project.

▶️ Installation

Install the required Python libraries:

pip install opencv-python ultralytics easyocr
🚀 Run the Project
python main.py

Press Q to close the Smart Traffic AI window.

📺 System Output

The system displays:

Detected vehicles with bounding boxes
Emergency vehicle alerts
License plate detection and OCR results
Total vehicle count
Active green lane
Green signal duration
Left, Middle, and Right lane status
Dynamic traffic signals for all three lanes
Detection Colors
🟢 Green → Emergency Vehicle
🔴 Red → Normal Car
🟡 Yellow → License Plate
🔮 Future Improvements
Real-time CCTV camera integration
Automatic traffic signal hardware control
Vehicle tracking to avoid duplicate counting
Improved OCR preprocessing for better license plate recognition
Dynamic green signal timing based on real-time congestion
Support for more vehicle classes
Web dashboard for traffic monitoring
Cloud deployment and real-time alerts
👨‍💻 Author

Aman Agrawal

⭐ If you find this project interesting, consider giving the repository a star!
