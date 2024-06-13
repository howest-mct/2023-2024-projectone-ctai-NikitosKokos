import cv2
import os
import numpy as np
from ultralytics import YOLO

def resize_and_pad(image, target_size):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    h, w = gray_image.shape[:2]
    scale = target_size / max(h, w)
    new_w, new_h = int(w * scale), int(h * scale)
    resized_image = cv2.resize(gray_image, (new_w, new_h))

    top = bottom = (target_size - new_h) // 2
    left = right = (target_size - new_w) // 2

    padded_image = cv2.copyMakeBorder(
        resized_image, top, bottom, left, right,
        borderType=cv2.BORDER_CONSTANT, value=0
    )

    return padded_image

def apply_augmentation(image):
    # Randomly adjust brightness, contrast, saturation
    alpha = 1.0 + np.random.uniform(-0.5, 0.5)  # Random brightness factor
    beta = 0.5 + np.random.uniform(-0.25, 0.25)  # Random contrast factor
    saturation = 0.5 + np.random.uniform(-0.25, 0.25)  # Random saturation factor

    image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * saturation, 0, 255).astype(np.uint8)
    image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    # Randomly rotate image
    angle = np.random.uniform(-15, 15)
    rows, cols = image.shape[:2]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    image = cv2.warpAffine(image, M, (cols, rows))

    return image

def capture_images_with_yolo(user_id):
    response = ""
    try:
        model = YOLO(r"D:\Downloads\Howest\Semester 2\Project_one\2023-2024-projectone-ctai-NikitosKokos\AI\models\detect\train5\weights\best.pt")
        output_dir = f'AI/dataset/{user_id}'
        os.makedirs(output_dir, exist_ok=True)

        # Attempt to open the video capture device
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not cap.isOpened():
            raise Exception("Error: Could not open webcam.")
        
        # Adjust camera settings
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Disable auto exposure (value may vary)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)  # Adjust brightness (0.0 to 1.0)
        cap.set(cv2.CAP_PROP_CONTRAST, 0.5)    # Adjust contrast (0.0 to 1.0)
        cap.set(cv2.CAP_PROP_EXPOSURE, -4)     # Adjust exposure (varies by camera, may need tuning)

        fps = 30
        frames_to_capture = 10

        frame_count = 0
        original_image_count = 0
        augmented_image_count = 0

        while original_image_count < 100:
            if cap is not None:
                ret, frame = cap.read()

                if not ret:
                    response = "Error: Could not read frame."
                    break

                frame_count += 1

                if frame_count % (fps // frames_to_capture) == 0:
                    results_list = model(frame)
                    for results in results_list:
                        if results.boxes is not None and len(results.boxes) > 0:
                            for box in results.boxes.xyxy:
                                x1, y1, x2, y2 = box.cpu().numpy().astype(int)
                                cropped_image = frame[y1:y2, x1:x2]
                                
                                # Apply augmentation and save augmented images
                                for _ in range(3):  # Create 3 augmented versions per original image
                                    augmented_image = apply_augmentation(cropped_image)
                                    resized_image = resize_and_pad(augmented_image, 320)
                                    augmented_image_path = os.path.join(output_dir, f'{augmented_image_count}.jpg')
                                    cv2.imwrite(augmented_image_path, resized_image)
                                    augmented_image_count += 1

                                # Save original image
                                resized_image = resize_and_pad(cropped_image, 320)
                                original_image_path = os.path.join(output_dir, f'{original_image_count}.jpg')
                                cv2.imwrite(original_image_path, resized_image)
                                original_image_count += 1

                                if original_image_count >= 100:
                                    break

        response = "Ok"

    except Exception as e:
        response = f"Exception occurred: {e}"

    finally:
        if cap is not None and cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()

    return response

# # Example usage:
# user_id = 'test'
# result = capture_images_with_augmentation(user_id)
# print("Capture result:", result)
