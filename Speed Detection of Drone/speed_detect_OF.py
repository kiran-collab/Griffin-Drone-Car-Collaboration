import cv2
import numpy as np

def km_to_miles(speed_kmh):
    # Conversion factor: 1 km = 0.621371 miles
    speed_mileh = speed_kmh * 0.621371
    return int(speed_mileh)

# Initialize video capture from a video file or camera (0 for default camera)
cap = cv2.VideoCapture('Testing3.mp4')

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
#fps = int(cap.get(5))

fps = frames_per_sec = int(cap.get(cv2.CAP_PROP_FPS))

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_Testing3.avi', fourcc, fps, (frame_width, frame_height))

speed_list = []
# Parameters for Lucas-Kanade optical flow
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Initialize variables for tracking
prev_frame = None
prev_pts = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ppm = 8
    

    if prev_frame is not None:
        # Calculate optical flow
        pts, status, error = cv2.calcOpticalFlowPyrLK(prev_frame, gray, prev_pts, None, **lk_params)

        # Select good points
        good_pts = pts[status == 1]
        prev_good_pts = prev_pts[status == 1]

        if len(good_pts) > 0 and len(prev_good_pts) > 0:
            # Calculate the average displacement between consecutive frames
            displacement = np.mean(np.abs(good_pts - prev_good_pts))

            d_meters = displacement/ppm
            time_constant = frames_per_sec*3600
            time_constant = time_constant/1000
            speed = d_meters * time_constant
            speed = km_to_miles(int(speed))

            # Define a constant to scale the displacement to speed (you may need to calibrate this)
            #speed_constant = 0.1  # Adjust this value based on your camera and scene setup

            # Calculate the speed (you can use other units like mph or km/h depending on your setup)
            #speed = displacement * speed_constant

            # Display the speed on the frame
            #cv2.putText(frame, f'Speed: {speed:.2f} pixels/frame', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Speed: {speed:2f} miles/hr', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            speed_list.append(speed)
            #print(speed_list)
            cv2.putText(frame, f'Avg. Speed: {sum(speed_list)/len(speed_list):.2f} miles/hr', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


        # Update previous points and frame
        prev_pts = good_pts.reshape(-1, 1, 2)
        prev_frame = gray

    else:
        # For the first frame, initialize points for tracking
        prev_frame = gray
        prev_pts = cv2.goodFeaturesToTrack(prev_frame, maxCorners=100, qualityLevel=0.3, minDistance=0)

    # Display the frame with optical flow information
    cv2.imshow('Optical Flow', frame)
    out.write(frame)

    if cv2.waitKey(30) & 0xFF == 27:  # Press 'Esc' to exit
        break

# Release video capture and close all OpenCV windows
cap.release()
out.release()
cv2.destroyAllWindows()
