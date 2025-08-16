import os
from PIL import Image
from rembg import remove
import tkinter as tk
from tkinter import filedialog

def select_directory():
    """Opens a dialog to select a directory."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    directory_path = filedialog.askdirectory(title="Select Image Directory")
    return directory_path

def remove_background_from_images_in_directory(directory_path):
    """Removes the background from all images in a given directory."""
    if not os.path.isdir(directory_path):
        print(f"Error: Directory not found at '{directory_path}'")
        return

    print(f"Selected directory: {directory_path}")
    found_image = False
    for filename in os.listdir(directory_path):
        print(f"Found file: {filename}")
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            found_image = True
            input_path = os.path.join(directory_path, filename)
            output_filename = os.path.splitext(filename)[0] + "_nobg.png"
            output_path = os.path.join(directory_path, output_filename)

            try:
                import numpy as np
                with Image.open(input_path) as img:
                    img = img.convert("RGBA")
                    output_img = remove(img)
                    # Handle different output types from rembg
                    if isinstance(output_img, Image.Image):
                        output_img.save(output_path)
                    elif isinstance(output_img, bytes):
                        with open(output_path, 'wb') as f:
                            f.write(output_img)
                    elif isinstance(output_img, np.ndarray):
                        Image.fromarray(output_img).save(output_path)
                    else:
                        raise TypeError(f"Unexpected output type from rembg: {type(output_img)}")
                print(f"Removed background from {filename} and saved as {output_filename}")
            except Exception as e:
                print(f"Could not process {filename}: {e}")
    if not found_image:
        print("No image files (.png, .jpg, .jpeg) found in the selected directory.")

if __name__ == "__main__":
    image_directory = select_directory()
    print(f"User selected: {image_directory}")
    if image_directory:
        remove_background_from_images_in_directory(image_directory)
    else:
        print("No directory selected. Exiting.")
