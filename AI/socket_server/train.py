from ultralytics import YOLO
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import os

# Custom Dataset class to load images
class CustomDataset(Dataset):
    def __init__(self, root_dir, subset='train', transform=None):
        self.root_dir = root_dir
        self.subset = subset
        self.transform = transform
        self.img_labels = []
        self.img_paths = []

        subset_dir = os.path.join(root_dir, subset)
        for label in os.listdir(subset_dir):
            label_dir = os.path.join(subset_dir, label)
            if os.path.isdir(label_dir):
                for img_file in os.listdir(label_dir):
                    if img_file.endswith(('.png', '.jpg', '.jpeg')):
                        self.img_paths.append(os.path.join(label_dir, img_file))
                        self.img_labels.append(0 if label == '2' else 1)  # Assuming 'user' is class 0 and 'unknown' is class 1

        print(f"Loaded {len(self.img_paths)} images from {os.path.join(root_dir, subset)}")

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, idx):
        img_path = self.img_paths[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.img_labels[idx]
        if self.transform:
            image = self.transform(image)
        return image, label

def train_detection():
    response = ""
    try:
        # Load the YOLO model
        model = YOLO(model="yolov8s-cls.pt").to('cuda')

        # Set the device to GPU
        device = 'cuda'

        # Set the dataset path
        data_path = "D:\\Downloads\\Howest\\Semester 2\\Project_one\\2023-2024-projectone-ctai-NikitosKokos\\AI\\facerecognition-2"

        # Define transformations for training data
        train_transforms = transforms.Compose([
            transforms.RandomHorizontalFlip(),
            transforms.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5, hue=0.5),
            transforms.RandomRotation(degrees=15),
            transforms.ToTensor()
        ])

        # Define transformations for validation data
        val_transforms = transforms.Compose([
            transforms.ToTensor()
        ])

        # Create the custom datasets
        train_dataset = CustomDataset(root_dir=data_path, subset='train', transform=train_transforms)
        val_dataset = CustomDataset(root_dir=data_path, subset='val', transform=val_transforms)
        
        if len(train_dataset) == 0:
            raise ValueError(f"No images found in the train dataset path: {os.path.join(data_path, 'train')}")
        if len(val_dataset) == 0:
            raise ValueError(f"No images found in the val dataset path: {os.path.join(data_path, 'val')}")

        # Train the model using built-in method with AMP
        model.train(
            data=data_path,  # Specify the dataset path
            epochs=10,
            batch=8,  # Specify the batch size
            imgsz=320,  # Specify the image size
            device=device,
            workers=4,  # Specify the number of workers
            augment=True  # Enable data augmentation
        )

        # Validate the model
        model.val()

        # Export the model
        model.export()

        response = "Training completed successfully."

    except Exception as e:
        response = f"Exception occurred: {e}"
        raise

    return response

if __name__ == '__main__':
    print(train_detection())
