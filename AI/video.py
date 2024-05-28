from ultralytics import YOLO

# Load your trained model
model = YOLO(r"D:\Downloads\Howest\Semester 2\Project_one\2023-2024-projectone-ctai-NikitosKokos\AI\runs\detect\train4\weights\best.pt")

results = model.predict(source='1', show=True)

print(results)