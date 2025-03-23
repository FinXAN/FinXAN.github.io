import os
import sys
import time
import cv2
import numpy as np
from ultralytics import YOLO
from datetime import datetime
import keyboard

# Path to YOLO model
model_path = 'yolo11n_ncnn_model'

# Common standards for box selection
bbox_colors = [(164, 120, 87), (68, 148, 228), (93, 97, 209), (178, 182, 133), (88, 159, 106), 
               (96, 202, 231), (159, 124, 168), (169, 162, 241), (98, 118, 150), (172, 176, 184)]

img_source = 'picamera0'
min_thresh = 0.48
# Resolution to display inference results at
user_res = "640x480" 

if not os.path.exists(model_path):
    print('ERROR: Model path is invalid or model was not found.')
    sys.exit(0)
model = YOLO(model_path, task='detect')
labels = model.names

# We check the idx num from official documentation
train_class_id = 6

# Set up Picamera
from picamera2 import Picamera2
cap = Picamera2()

resW, resH = int(user_res.split('x')[0]), int(user_res.split('x')[1])
cap.configure(cap.create_video_configuration(main={"format": 'XRGB8888', "size": (resW, resH)}))
cap.start()

# Initialize control and status variables
avg_frame_rate = 0
frame_rate_buffer = []
fps_avg_len = 200
# Define the region of interest (ROI) for cropping (This is for my selection for train position)
ymin, ymax = 160, 350
xmin, xmax = 150, 520

# Begin inference loop
while True:
    ## Exit Key
    key = cv2.waitKey(1)& 0xFF
    if key ==27:
        break
    t_start = time.perf_counter()

    # Capture frame from picamera
    frame_bgra = cap.capture_array()
    frame = cv2.cvtColor(np.copy(frame_bgra), cv2.COLOR_BGRA2BGR)


    cropped_frame = frame[ymin:ymax, xmin:xmax]
    results = model(cropped_frame, verbose=False)
    detections = results[0].boxes
    object_count = 0

    for i in range(len(detections)):
        xyxy_tensor = detections[i].xyxy.cpu()  #in CPU memory, For rasberry pi
        xyxy = xyxy_tensor.numpy().squeeze() 
        xmin_detect, ymin_detect, xmax_detect, ymax_detect = xyxy.astype(int)  # Get object index

        # Draw box and label for visualization on the cropped frame
        classidx = int(detections[i].cls.item())
        classname = labels[classidx]

        # For my application, only shows results when detecting train
        # Or restructing the final output layer as single, which can be done refering to my transfer learning example
        if classidx == train_class_id:
            conf = detections[i].conf.item()
            # Threshold for filtering the results
            if conf > min_thresh:
                # Save the cropped image with a timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_filename = f'img_source/train_{timestamp}.png'

                ##---------------------- You can move this line to before object_count +=1 for getting the actual box labelling----------##
                cv2.imwrite(image_filename, cropped_frame)


                print(f"Saved image: {image_filename}")
                # Draw bounding box and label text for visualization on the cropped frame
                color = bbox_colors[classidx % 10]
                cv2.rectangle(cropped_frame, (xmin_detect, ymin_detect), (xmax_detect, ymax_detect), color, 2)

                label = f'{classname}: {int(conf * 100)}%'
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)  #font size
                label_ymin = max(ymin_detect, labelSize[1] + 10)  # Make sure not too close to top of window
                cv2.rectangle(cropped_frame, (xmin_detect, label_ymin - labelSize[1] - 10), 
                              (xmin_detect + labelSize[0], label_ymin + baseLine - 10), color, cv2.FILLED) 
                cv2.putText(cropped_frame, label, (xmin_detect, label_ymin - 7), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    # Calculate and draw framerate
    cv2.putText(cropped_frame, f'FPS: {avg_frame_rate:0.2f}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 255, 255), 2)
    # Display detection results on the cropped frame
    cv2.putText(cropped_frame, f'Number of trains: {object_count}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 255, 255), 2)
    cv2.imshow('YOLO detection results', cropped_frame)  

    # Calculate FPS for this frame
    t_stop = time.perf_counter()
    frame_rate_calc = float(1 / (t_stop - t_start))

    # Finding average FPS over multiple frames
    if len(frame_rate_buffer) >= fps_avg_len:
        temp = frame_rate_buffer.pop(0)
        frame_rate_buffer.append(frame_rate_calc)
    else:
        frame_rate_buffer.append(frame_rate_calc)
    # Calculate average FPS for past frames
    avg_frame_rate = np.mean(frame_rate_buffer)

# Clean up
print(f'Average pipeline FPS: {avg_frame_rate:.2f}')
cap.stop()
cv2.destroyAllWindows()

