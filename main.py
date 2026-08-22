import cv2
from ultralytics import YOLO
import easyocr  # Stable EasyOCR for Windows CPU

# Helper function to determine traffic signal colors based on lane status
def get_light_colors(status):
    if "GO" in status:
        return (50, 50, 50), (50, 50, 50), (0, 255, 0)      # Only Green On
    elif status == "WAIT":
        return (50, 50, 50), (0, 255, 255), (50, 50, 50)    # Only Yellow On
    else:
        return (0, 0, 255), (50, 50, 50), (50, 50, 50)      # Only Red On

# 1. Emergency vehicles detection model
model_emergency = YOLO("New_emergency-best.pt")

# 1.5 License plate detection model
model_license_plate = YOLO("license_plate_best.pt")

# Initialize EasyOCR Reader for Windows CPU
reader = easyocr.Reader(['en'], gpu=False)

# Model name and class display
print("Your model class names are:", model_emergency.names)

# Load video file
cap = cv2.VideoCapture("videos/traffic.mp4")

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
        
    # Frame resize
    frame = cv2.resize(frame, (1000, 600))
    
    # 2. Define lanes: Left lane, Middle lane, Right lane
    cv2.line(frame, (330, 0), (330, 600), (255, 0, 0), 2)
    cv2.line(frame, (660, 0), (660, 600), (255, 0, 0), 2)
    
    # Reset variables for each frame
    vehicle_count = 0
    left_count = 0
    middle_count = 0
    right_count = 0
    
    emergency_detected = False
    detected_type = ""
    current_lane = "MIDDLE" # Default lane
    
    # 3. Prediction Model (Accuracy conf=0.5)
    results = model_emergency(frame, conf=0.5)
    
    # Process detected vehicles
    for result in results:
        for box in result.boxes:
            # Vehicles class id
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            class_id = int(box.cls[0])
            conf = float(box.conf[0])
            
            class_name = model_emergency.names[class_id].lower()
            
            vehicle_count += 1
            center_x = (x1 + x2) // 2
            
            # Count vehicles based on lane position
            if center_x < 330:
                left_count += 1
                lane_of_this_vehicle = "LEFT"
            elif center_x < 660:
                middle_count += 1
                lane_of_this_vehicle = "MIDDLE"
            else:
                right_count += 1
                lane_of_this_vehicle = "RIGHT"
                
            # Check Emergency vehicles (ambulance, fire_truck, police)
            if class_name in ['ambulance', 'fire_truck', 'police']:
                emergency_detected = True
                current_lane = lane_of_this_vehicle  # Save lane
                detected_type = f"{class_name.upper()} DETECTED"
                
                # Green Box on Emergency vehicles
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"EMERGENCY: {class_name.upper()} ({conf:.2f})", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                            
            elif class_name == 'car':
                # Red box on normal vehicles
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, f"CAR ({conf:.2f})", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # 3.5 License Plate Detection & EasyOCR Logic
    lp_results = model_license_plate(frame, conf=0.4)
    for lp_result in lp_results:
        for lp_box in lp_result.boxes:
            x1_lp, y1_lp, x2_lp, y2_lp = map(int, lp_box.xyxy[0])
            conf_lp = float(lp_box.conf[0])
            
            # Crop the license plate region safely
            h, w, _ = frame.shape
            plate_crop = frame[max(0, y1_lp):min(h, y2_lp), max(0, x1_lp):min(w, x2_lp)]
            
            plate_text = "READING..."
            if plate_crop.size > 0:
                try:
                    allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                    ocr_res = reader.readtext(plate_crop, allowlist=allowed_chars)
                    if ocr_res:
                        # Extract recognized text
                        plate_text = ocr_res[0][1].upper().replace(" ", "")
                except Exception:
                    plate_text = "ERROR"
            
            # Draw Yellow box for license plates
            cv2.rectangle(frame, (x1_lp, y1_lp), (x2_lp, y2_lp), (0, 255, 255), 2)
            # Display text (Size=0.6, Thickness=2)
            cv2.putText(frame, f"{plate_text} ({conf_lp:.2f})", (x1_lp, y1_lp - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    # 4. ADVANCED SMART TRAFFIC LOGIC
    left_status, middle_status, right_status = "STOP", "STOP", "STOP"
    left_text_color, middle_text_color, right_text_color = (0, 0, 255), (0, 0, 255), (0, 0, 255) # Red
    
    green_lane = "MIDDLE"
    green_time = 25
    
    # Case 1: Emergency vehicles detected
    if emergency_detected:
        green_lane = current_lane
        green_time = 45
        
        if green_lane == "LEFT":
            left_status = "EMERGENCY GO"
            left_text_color = (0, 255, 0)
        elif green_lane == "MIDDLE":
            middle_status = "EMERGENCY GO"
            middle_text_color = (0, 255, 0)
        elif green_lane == "RIGHT":
            right_status = "EMERGENCY GO"
            right_text_color = (0, 255, 0)
            
    # Case 2: Normal traffic based on traffic congestion
    else:
        lane_counts = {"LEFT": left_count, "MIDDLE": middle_count, "RIGHT": right_count}
        sorted_lanes = sorted(lane_counts.items(), key=lambda item: item[1], reverse=True)
        
        # FIXED: Extract correct strings from tuples
        highest_lane = sorted_lanes[0][0]  
        medium_lane = sorted_lanes[1][0]   
        
        green_lane = highest_lane
        
        # A. High traffic lane -> AUTO GREEN (GO)
        if highest_lane == "LEFT":
            left_status = "GO"
            left_text_color = (0, 255, 0)
        elif highest_lane == "MIDDLE":
            middle_status = "GO"
            middle_text_color = (0, 255, 255) # Yellow color warning if busy
        elif highest_lane == "RIGHT":
            right_status = "GO"
            right_text_color = (0, 255, 0)
            
        # B. Medium traffic lane -> WAIT (YELLOW)
        if medium_lane == "LEFT":
            left_status = "WAIT"
            left_text_color = (0, 255, 255)
        elif medium_lane == "MIDDLE":
            middle_status = "WAIT"
            middle_text_color = (0, 255, 255)
        elif medium_lane == "RIGHT":
            right_status = "WAIT"
            right_text_color = (0, 255, 255)

    # Get light colors for all lanes
    l_red, l_yel, l_grn = get_light_colors(left_status)
    m_red, m_yel, m_grn = get_light_colors(middle_status)
    r_red, r_yel, r_grn = get_light_colors(right_status)

    # SIGNAL 1: LEFT LANE
    cv2.rectangle(frame, (25, 30), (85, 210), (30, 30, 30), -1)
    cv2.circle(frame, (55, 60), 12, l_red, -1)
    cv2.circle(frame, (55, 120), 12, l_yel, -1)
    cv2.circle(frame, (55, 180), 12, l_grn, -1)
    cv2.putText(frame, "LEFT", (30, 225), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    # SIGNAL 2: MIDDLE LANE
    cv2.rectangle(frame, (95, 30), (155, 210), (30, 30, 30), -1)
    cv2.circle(frame, (125, 60), 12, m_red, -1)
    cv2.circle(frame, (125, 120), 12, m_yel, -1)
    cv2.circle(frame, (125, 180), 12, m_grn, -1)
    cv2.putText(frame, "MID", (105, 225), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    # SIGNAL 3: RIGHT LANE
    cv2.rectangle(frame, (165, 30), (225, 210), (30, 30, 30), -1)
    cv2.circle(frame, (195, 60), 12, r_red, -1)
    cv2.circle(frame, (195, 120), 12, r_yel, -1)
    cv2.circle(frame, (195, 180), 12, r_grn, -1)
    cv2.putText(frame, "RIGHT", (170, 225), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    # Right panel
    cv2.rectangle(frame, (680, 30), (980, 360), (20, 20, 20), -1)

    # Main text info
    cv2.putText(frame, f"Total Vehicles: {vehicle_count}", (690, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, f"Active Lane: {green_lane}", (690, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, f"Green Time: {green_time}s", (690, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Dynamic emergency display text
    if emergency_detected:
        cv2.putText(frame, detected_type, (690, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "NORMAL TRAFFIC", (690, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    # Live vehicle counts
    cv2.putText(frame, f"Left Lane: {left_count} - {left_status}", (690, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.5, left_text_color, 2)
    cv2.putText(frame, f"Middle Lane: {middle_count} - {middle_status}", (690, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, middle_text_color, 2)
    cv2.putText(frame, f"Right Lane: {right_count} - {right_status}", (690, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.5, right_text_color, 2)

    # Show window
    cv2.imshow("Smart Traffic AI", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
