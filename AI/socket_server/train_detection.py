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
            epochs=5, 
            imgsz=(320, 320),
            verbose=True,
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

# train_detection()
# import torch

# def check_cuda():
#     if torch.cuda.is_available():
#         print("CUDA is available.")
#         print("Number of GPUs:", torch.cuda.device_count())
#         print("Current GPU:", torch.cuda.current_device())
#         print("GPU name:", torch.cuda.get_device_name(torch.cuda.current_device()))
#     else:
#         print("CUDA is not available.")
