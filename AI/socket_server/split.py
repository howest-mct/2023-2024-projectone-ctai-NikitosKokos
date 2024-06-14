import os
import shutil
import random

def split_dataset_by_class(class_name, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1):
    dataset_path = r"D:\Downloads\Howest\Semester 2\Project_one\2023-2024-projectone-ctai-NikitosKokos\AI\facerecognition-2"
    dataset_images = r'D:\Downloads\Howest\Semester 2\Project_one\2023-2024-projectone-ctai-NikitosKokos\AI\dataset'
    
    # Create train, val, and test directories if they don't exist
    for split in ['train', 'val', 'test']:
        split_path = os.path.join(dataset_path, split, 'user')
        if not os.path.exists(split_path):
            os.makedirs(split_path)
        else:
            # Clear the directory if it already exists
            for filename in os.listdir(split_path):
                file_path = os.path.join(split_path, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
    
    # List all images in the class folder
    class_images = [img for img in os.listdir(os.path.join(dataset_images, class_name)) if img.endswith(('.jpg', '.jpeg', '.png'))]
    random.shuffle(class_images)
    
    # Calculate the number of images for each split
    num_images = len(class_images)
    num_train = int(train_ratio * num_images)
    num_val = int(val_ratio * num_images)
    num_test = num_images - num_train - num_val
    
    # Move images to train, val, and test directories
    for i, img in enumerate(class_images):
        img_path = os.path.join(dataset_images, class_name, img)
        if i < num_train:
            dest_folder = 'train'
        elif i < num_train + num_val:
            dest_folder = 'val'
        else:
            dest_folder = 'test'
        
        dest_path = os.path.join(dataset_path, dest_folder, 'user', img)
        shutil.copy(img_path, dest_path)
    
    print(f"Split user {class_name} images into train ({num_train}), val ({num_val}), and test ({num_test}) sets.")


# if __name__ == '__main__':
#     class_name = "unknown"  # Change this to the name of your class folder
#     split_dataset_by_class(class_name, train_ratio=0.7)
    # train_detection()