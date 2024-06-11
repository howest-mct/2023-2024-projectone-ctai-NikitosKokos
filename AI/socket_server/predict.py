import cv2
import time
from ultralytics import YOLO
import os

def predict_user(user_id):
   response = ''
   try:
      # Load the YOLO model
      detection_model = YOLO(r"D:\Downloads\Howest\Semester 2\Project_one\2023-2024-projectone-ctai-NikitosKokos\AI\models\detect\train5\weights\best.pt")
      classification_model = YOLO(r"D:\Downloads\Howest\Semester 2\Project_one\2023-2024-projectone-ctai-NikitosKokos\AI\models\classify\best.pt")

      # Attempt to open the video capture device
      cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

      if not cap.isOpened():
         raise Exception("Error: Could not open webcam.")

      # Initialize variables for capturing frames and timing
      start_time = time.time()
      duration = 5  # capture for 5 seconds
      total_frames = 0
      correct_predictions = 0
      first_run = True

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
                  
                  # Use classification model to classify the cropped image
                  classification_results = classification_model(cropped_image)

                  if classification_results and len(classification_results) > 0:
                     classification_result = classification_results[0]
                     if classification_result.probs is not None:
                        class_probs = classification_result.probs.cpu().numpy()

                        # Access the top1 attribute for the predicted class
                        predicted_class = classification_result.probs.top1
                        # print(f"Predicted class: {classification_result.probs.top1conf}, User ID: {user_id}")
                        if classification_result.names[predicted_class] == str(user_id):
                           if classification_result.probs.top1conf > 0.9:
                              response = 'Ok'


         # Calculate accuracy
         # if total_frames > 0:
         #    accuracy = (correct_predictions / total_frames) * 100
         # else:
         #    accuracy = 0

         # response = accuracy

         if first_run:
            start_time = time.time()
            first_run = False
         print('helloo', round((time.time() - start_time)))
         

   except Exception as e:
      response = f"Exception occurred: {e}"

   finally:
      if cap.isOpened():
         cap.release()
      cv2.destroyAllWindows()

   return response