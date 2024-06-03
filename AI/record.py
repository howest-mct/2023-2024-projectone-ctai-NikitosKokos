import cv2
from ultralytics import YOLO
import time
import os

# Load your trained model
model = YOLO(r"D:\Downloads\Howest\Semester 2\Project_one\2023-2024-projectone-ctai-NikitosKokos\AI\runs\detect\train5\weights\best.pt")

# Create a directory to save images
output_dir = 'captured_images'
os.makedirs(output_dir, exist_ok=True)

# Open webcam (source=0)
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

fps = 30  # Assuming the webcam captures at 30 frames per second
capture_duration = 5  # Capture duration in seconds
frames_to_capture = 10  # Number of frames to capture per second

start_time = time.time()
frame_count = 0
image_count = 0

while image_count < 50:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    frame_count += 1

    # Process every (fps // frames_to_capture)th frame
    if frame_count % (fps // frames_to_capture) == 0:
        # Predict using the YOLO model
        results_list = model(frame)
        
        # Check if predictions are present in each Results object
        for results in results_list:
            if results.boxes is not None and len(results.boxes) > 0:
                # Iterate through the bounding boxes and save images containing them
                for box in results.boxes.xyxy:
                    x1, y1, x2, y2 = box.numpy().astype(int)  # Convert the bounding box to a NumPy array
                    # Crop the region containing the detected object
                    cropped_image = frame[y1:y2, x1:x2]
                    
                    # Save the cropped image
                    image_path = os.path.join(output_dir, f'image_{image_count}.jpg')
                    cv2.imwrite(image_path, cropped_image)
                    image_count += 1

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

print(f"Captured {image_count} images.")

# just name can be used to classify my model
# 
