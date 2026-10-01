# SmartTrafficAI 🚦

**AI-based intelligent traffic management and emergency vehicle detection system**

SmartTrafficAI is a computer-vision system built with Python, Ultralytics YOLO, OpenCV and EasyOCR. It analyzes traffic video, counts vehicles in three lanes, detects emergency vehicles (ambulance, fire truck, police), gives their lane priority on the signal, and reads license plates with OCR.

<!-- TODO: add a 30-60 second demo video or GIF here, e.g. ![Demo](assets/demo.gif) -->

---

## Results

The emergency-vehicle model was trained on a custom dataset of **15,369 images** (train/val/test). The dataset combines Kaggle images with self-collected images that I annotated manually (Roboflow and CVAT), and the classes were balanced.

**Training setup:** YOLO11s (Ultralytics) · 50 epochs · 640 px · Tesla T4 GPU (Kaggle) · ~3.1 hours · ~4 ms inference per image

**Validation performance (2,258 images, 2,883 instances):**

| Class | Images | Instances | Precision | Recall | mAP@50 | mAP@50-95 |
|---|---|---|---|---|---|---|
| **All** | 2,258 | 2,883 | 0.934 | 0.898 | **0.949** | 0.801 |
| Car | 792 | 925 | 0.950 | 0.936 | 0.974 | 0.869 |
| Ambulance | 550 | 644 | 0.922 | 0.913 | 0.955 | 0.809 |
| Police | 316 | 566 | 0.923 | 0.898 | 0.945 | 0.806 |
| Fire truck | 629 | 748 | 0.941 | 0.846 | 0.921 | 0.718 |

Fire truck has the lowest recall and mAP@50-95, so adding more varied fire-truck images is the next dataset improvement.

<!-- TODO: add training plots, e.g.
![Confusion Matrix](assets/confusion_matrix.png)
![PR Curve](assets/PR_curve.png)
-->

---

## Features

- Detects emergency vehicles: ambulance, fire truck and police car
- Detects and counts vehicles in the Left, Middle and Right lanes
- Gives priority to the lane that contains an emergency vehicle
- Selects the signal state for each lane from lane congestion
- Gives the emergency lane a longer green time (45 s)
- Marks the medium-traffic lane as wait (yellow) and the remaining lane as stop (red)
- Detects license plates with a separate YOLO model and reads the text with EasyOCR
- Shows live vehicle count, active lane, green time, lane status and emergency status

## How It Works

**1. Vehicle and emergency-vehicle detection**
A custom YOLO model detects vehicles and emergency vehicles in each video frame. When an emergency vehicle is found, its lane is identified and given immediate priority.

**2. Lane-based counting**
The frame is split into three lanes (Left, Middle, Right). Each detection is assigned to a lane using the horizontal position of its bounding-box center, and vehicles are counted per lane.

**3. Emergency priority**
If an emergency vehicle is detected:
- its lane signal changes to `EMERGENCY GO`
- green time is set to 45 seconds
- all other lanes stay stopped

**4. Normal traffic management**
With no emergency vehicle, the three lane counts are compared:
- highest traffic lane → 🟢 GO
- medium traffic lane → 🟡 WAIT
- remaining lane → 🔴 STOP

Normal green time is currently fixed at 25 seconds.

**5. License plate detection and OCR**
A second YOLO model finds plate regions. Each plate is cropped from the frame, read with EasyOCR (restricted to alphanumeric characters), and shown with the text and confidence score.

**Detection colors:** 🟢 emergency vehicle · 🔴 normal car · 🟡 license plate

---

## Tech Stack

Python · Ultralytics YOLO · OpenCV · EasyOCR

## Project Structure

```
SmartTrafficAI/
├── main.py
├── New_emergency-best.pt      # emergency vehicle detection model
├── license_plate_best.pt      # license plate detection model
├── requirements.txt
└── videos/
    └── traffic.mp4            # place your input video here
```

> The model files and the input video must be in the paths used by `main.py` before you run the project.

## Installation and Usage

```bash
git clone https://github.com/AmanAgrawalAI/SmartTrafficAI.git
cd SmartTrafficAI
pip install -r requirements.txt
python main.py
```

Press **Q** to close the Smart Traffic AI window.

## Screenshots


**Fire truck detection**
<img width="1241" height="779" alt="Screenshot 2026-08-23 210604" src="https://github.com/user-attachments/assets/37a588ea-6c0a-458c-8c05-acd91a027203" />


**Ambulance detection**
<img width="1246" height="780" alt="Screenshot 2026-08-23 210907" src="https://github.com/user-attachments/assets/7fabe297-4047-4039-9ac2-7153f2da3d60" />


**Police detection**
<img width="1239" height="777" alt="Screenshot 2026-08-23 211207" src="https://github.com/user-attachments/assets/4b4fdd25-4bed-44d6-9415-32cf035278a3" />


**Ambulance detection at night**
<img width="1238" height="781" alt="Screenshot 2026-08-23 210715" src="https://github.com/user-attachments/assets/79372dbd-2d78-43b5-9dfc-8534c1607f8f" />


**Ambulance from a different angle**
<img width="1240" height="777" alt="Screenshot 2026-08-23 210301" src="https://github.com/user-attachments/assets/56f83582-5c52-4f1e-9000-3c1cc8efef9e" />


---

## Limitations and Future Improvements

- Green time is fixed (25 s normal, 45 s emergency); make it adapt to real-time congestion
- Add vehicle tracking to avoid counting the same vehicle twice
- Improve OCR preprocessing for better plate recognition
- Add more fire-truck and night-time images to improve recall
- Integrate live CCTV input and signal hardware control
- Web dashboard, cloud deployment and real-time alerts

## Author

**Aman Kumar**
GitHub: [AmanAgrawalAI](https://github.com/AmanAgrawalAI) · LinkedIn: [aman-kumar-788677378](https://linkedin.com/in/aman-kumar-788677378)

## License

Released under the MIT License.

⭐ If you find this project useful, consider giving the repository a star!
