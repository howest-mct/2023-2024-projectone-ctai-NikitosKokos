import cv2
from ultralytics import YOLO
import time
import os

# Load your trained model
model = YOLO(r"D:\Downloads\Howest\Semester 2\Project_one\2023-2024-projectone-ctai-NikitosKokos\AI\runs\detect\train5\weights\best.pt")

# Create a directory to save images
output_dir = 'AI/unknown'
input_dir = 'AI/faces'
os.makedirs(output_dir, exist_ok=True)

image_count = 63000

image_files = sorted(os.listdir(input_dir))

for img_file in image_files:
    if image_count >= 64000:
        break

    img_path = os.path.join(input_dir, img_file)
    frame = cv2.imread(img_path)

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

print(f"Captured {image_count} images.")

# just name can be used to classify my model
# 
