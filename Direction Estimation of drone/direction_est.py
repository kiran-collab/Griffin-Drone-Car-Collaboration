import cv2
import numpy as np

# Perform calibration to determine the mapping from pixel coordinates to real-world coordinates
# This step is crucial and requires knowledge about the camera setup

#Calibration to be done based on camera setup

# Example calibration values (replace these with your actual calibration values)
pixels_per_meter = 0.5  # Adjust this value based on your calibration
origin_x, origin_y = 320, 240  # Adjust these values based on your calibration

ret, frame = cap.read()
# Initialize video capture
video_file = 'video_file4.mp4'
cap = cv2.VideoCapture(video_file)  # Use 0 for default camera, change it if using an external camera

# Set up initial tracking window
ret, frame = cap.read()
bbox = cv2.selectROI(frame, False)
tracker = cv2.TrackerKCF_create()
tracker.init(frame, bbox)

while True:
    # Read a new frame
    ret, frame = cap.read()

    # Update the tracker
    success, bbox = tracker.update(frame)

    # Draw bounding box
    if success:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (0, 255, 0), 2)

        # Calculate the center of the bounding box
        center_x = int((p1[0] + p2[0]) / 2)
        center_y = int((p1[1] + p2[1]) / 2)

        # Convert pixel coordinates to real-world coordinates
        x_meters = (center_x - origin_x) / pixels_per_meter
        y_meters = (center_y - origin_y) / pixels_per_meter

        # Determine the cardinal direction
        if x_meters > 0:
            direction_x = "East"
        else:
            direction_x = "West"

        if y_meters > 0:
            direction_y = "South"
        else:
            direction_y = "North"

        cv2.putText(frame, f"Direction: {direction_y}, {direction_x}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Object Tracking', frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()