import os
import cv2

def grayscale_images_in_folder(folder_path):
    try:
        # Iterate over all files in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            # Check if the file is an image (you can add more extensions if needed)
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Read the image in color
                image = cv2.imread(file_path, cv2.IMREAD_COLOR)
                
                # Convert to grayscale
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                
                # Overwrite the original image with the grayscale version
                cv2.imwrite(os.path.join(folder_path, 'c_'+filename), gray_image)
                
                print(f"Converted {filename} to grayscale.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
folder_path = r'D:\Downloads\Howest\Semester 2\Project_one\2023-2024-projectone-ctai-NikitosKokos\AI\dataset\5'
grayscale_images_in_folder(folder_path)
