import cv2
import time
from ultralytics import YOLO
import os

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

def predict_user(user_id):
    response = ''
    try:
        # Load the YOLO models
        detection_model = YOLO(r"D:\Downloads\Howest\Semester 2\Project_one\2023-2024-projectone-ctai-NikitosKokos\AI\models\detect\train5\weights\best.pt")
        # Load the YOLO classification model for the specific user
        classification_model_path = fr"D:\Downloads\Howest\Semester 2\Project_one\2023-2024-projectone-ctai-NikitosKokos\AI\models\classify\{user_id}\best.pt"
        classification_model = YOLO(classification_model_path)

        # Attempt to open the video capture device
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not cap.isOpened():
            raise Exception("Error: Could not open webcam.")
        
        # Adjust camera settings
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Disable auto exposure (value may vary)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)  # Adjust brightness (0.0 to 1.0)
        cap.set(cv2.CAP_PROP_CONTRAST, 0.5)    # Adjust contrast (0.0 to 1.0)
        cap.set(cv2.CAP_PROP_EXPOSURE, -4)     # Adjust exposure (varies by camera, may need tuning)

        # Initialize variables for capturing frames and timing
        start_time = time.time()
        duration = 5  # capture for 5 seconds
        total_frames = 0
        first_run = True

        # Directory to save high-confidence images
        save_dir = r"D:\Downloads\Howest\Semester 2\Project_one\2023-2024-projectone-ctai-NikitosKokos\AI\dataset\login"
        os.makedirs(save_dir, exist_ok=True)

        while ((time.time() - start_time < duration) or first_run) and not response:
            ret, frame = cap.read()

            if not ret:
                response = "Error: Could not read frame."
                break

            total_frames += 1

            # Use detection model to detect objects in the frame
            results_list = detection_model(frame)
            for results in results_list:
                if results.boxes is not None and len(results.boxes) > 0:
                    for box in results.boxes.xyxy:
                        x1, y1, x2, y2 = box.cpu().numpy().astype(int)
                        cropped_image = frame[y1:y2, x1:x2]
                        
                        # Convert cropped image to grayscale
                        gray_cropped_image = resize_and_pad(cropped_image, 320)

                        # Use classification model to classify the grayscale cropped image
                        classification_results = classification_model(gray_cropped_image)

                        if classification_results and len(classification_results) > 0:
                            classification_result = classification_results[0]
                            if classification_result.probs is not None:
                                class_probs = classification_result.probs.cpu().numpy()

                                # Access the top1 attribute for the predicted class
                                predicted_class = classification_result.probs.top1
                                if classification_result.names[predicted_class] == 'user':
                                    if classification_result.probs.top1conf > 0.9:
                                        response = 'Ok'
                                        # Save the high-confidence image
                                        timestamp = time.strftime("%Y%m%d-%H%M%S")
                                        image_path = os.path.join(save_dir, f"{user_id}_{timestamp}.jpg")
                                        cv2.imwrite(image_path, gray_cropped_image)

            if first_run:
                first_run = False

        print('Time elapsed:', round((time.time() - start_time), 2))

    except Exception as e:
        response = f"Exception occurred: {e}"

    finally:
        if cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()

    return response