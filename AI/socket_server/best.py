import os
import shutil

def get_the_best_model():
    # Find the folder with the highest number containing weights/best.pt
    classify_runs_dir = r"D:\Downloads\Howest\Semester 2\Project_one\2023-2024-projectone-ctai-NikitosKokos\runs\classify"
    highest_num = -1
    highest_num_dir = None

    for folder_name in os.listdir(classify_runs_dir):
        if folder_name.startswith("train") and folder_name[5:].isdigit():
            folder_num = int(folder_name[5:])
            weights_dir = os.path.join(classify_runs_dir, folder_name, "weights")
            best_pt_path = os.path.join(weights_dir, "best.pt")

            if os.path.exists(best_pt_path) and folder_num > highest_num:
                highest_num = folder_num
                highest_num_dir = folder_name

    if highest_num_dir:
        best_pt_path = os.path.join(classify_runs_dir, highest_num_dir, "weights", "best.pt")
        destination_dir = r"D:\Downloads\Howest\Semester 2\Project_one\2023-2024-projectone-ctai-NikitosKokos\AI\models\classify"
        os.makedirs(destination_dir, exist_ok=True)
        destination_path = os.path.join(destination_dir, "best.pt")
        shutil.copyfile(best_pt_path, destination_path)
        print(f"Copied {best_pt_path} to {destination_path}")
    else:
        print("No valid training directories found with weights/best.pt.")