import cv2
from ultralytics import YOLO
import os

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

        fps = 30
        frames_to_capture = 10

        frame_count = 0
        image_count = 0

        while image_count < 50:
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
                                image_path = os.path.join(output_dir, f'{image_count}.jpg')
                                cv2.imwrite(image_path, cropped_image)
                                image_count += 1

        response = "Ok"

    except Exception as e:
        response = f"Exception occurred: {e}"

    finally:
        if cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()

    return response
