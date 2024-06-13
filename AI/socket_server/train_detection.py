from ultralytics import YOLO

def train_detection():
    response = ""
    try:
        # Load the YOLO model
        model = YOLO(model="yolov8s-cls.pt")
        # model = YOLO(model="yolov8n.pt")
        
        # Set the device to GPU
        device = 'cuda'
        
        # Train the model on the GPU
        model.train(
            data="D:\\Downloads\\Howest\\Semester 2\\Project_one\\2023-2024-projectone-ctai-NikitosKokos\\AI\\facerecognition-2", 
            epochs=10,
            imgsz=320,
            # verbose=True,
            verbose=False,
            batch=8,
            device=device
        )
        
        # Validate the model
        model.val()
        
        # Export the model
        model.export()
        
        response = "Training completed successfully."
    except Exception as e:
        response = f"Exception occurred: {e}"
    
    return response

# if __name__ == '__main__':
#     print(train_detection())