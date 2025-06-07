import os
from PIL import Image

def resize_images_in_folder(folder_path, new_width, new_height):
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return

    # Create an output folder
    output_folder = os.path.join(folder_path, "resized")
    os.makedirs(output_folder, exist_ok=True)

    # Process each PNG file in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".png"):
            file_path = os.path.join(folder_path, filename)
            try:
                with Image.open(file_path) as img:
                    resized_img = img.resize((new_width, new_height))
                    output_path = os.path.join(output_folder, filename)
                    resized_img.save(output_path)
                    print(f"Resized and saved: {output_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

# Get user input for dimensions
folder_path = "C:\\Users\\eabeltranm\\Pictures\\Screenshots"  # Replace with your folder path
try:
    new_width = int(input("Enter the desired width in pixels: "))
    new_height = int(input("Enter the desired height in pixels: "))
    resize_images_in_folder(folder_path, new_width, new_height)
except ValueError:
    print("Please enter valid numbers for width and height.")