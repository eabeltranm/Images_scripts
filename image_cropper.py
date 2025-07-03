import os
from PIL import Image

# Prompt for the folder containing images
folder = input('Enter the path to the folder containing images: ')

# Prompt for crop margins
try:
    left = int(input('Enter left margin (pixels): '))
    top = int(input('Enter top margin (pixels): '))
    right = int(input('Enter right margin (pixels): '))
    bottom = int(input('Enter bottom margin (pixels): '))
except ValueError:
    print('Invalid input. Using default margins (0, 0, 0, 0).')
    left = top = right = bottom = 0

# Output folder
output_folder = os.path.join(folder, 'cropped')
os.makedirs(output_folder, exist_ok=True)

# Supported image extensions
img_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

for filename in os.listdir(folder):
    if filename.lower().endswith(img_exts):
        img_path = os.path.join(folder, filename)
        try:
            with Image.open(img_path) as img:
                width, height = img.size
                crop_box = (
                    left,
                    top,
                    width - right,
                    height - bottom
                )
                cropped_img = img.crop(crop_box)
                out_path = os.path.join(output_folder, filename)
                cropped_img.save(out_path)
                print(f'Cropped: {filename} -> {out_path}')
        except Exception as e:
            print(f'Failed to crop {filename}: {e}')
