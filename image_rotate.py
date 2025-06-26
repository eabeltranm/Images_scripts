import os
from PIL import Image

# Prompt for the folder containing images
folder = input('Enter the path to the folder containing images: ')

# Prompt for desired format
format_map = {'jpeg': 'JPEG', 'jpg': 'JPEG', 'png': 'PNG', 'bmp': 'BMP', 'gif': 'GIF'}
format_input = input('Enter the desired image format (jpeg, png, bmp, gif): ').strip().lower()
img_format = format_map.get(format_input, 'JPEG')

# Prompt for rotation
rotate_choice = input('Do you want to rotate the images? (y/n): ').strip().lower()
if rotate_choice == 'y':
    try:
        rotate_degrees = float(input('Enter degrees to rotate (e.g., 90, 180): '))
    except ValueError:
        print('Invalid input. No rotation will be applied.')
        rotate_degrees = None
else:
    rotate_degrees = None

# Prompt for resizing
resize_choice = input('Do you want to resize the images? (y/n): ').strip().lower()
if resize_choice == 'y':
    try:
        new_width = int(input('Enter new width: '))
        new_height = int(input('Enter new height: '))
        new_size = (new_width, new_height)
    except ValueError:
        print('Invalid input. No resizing will be applied.')
        new_size = None
else:
    new_size = None

# Output folder
output_folder = os.path.join(folder, 'output')
os.makedirs(output_folder, exist_ok=True)

# Supported image extensions
img_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

for filename in os.listdir(folder):
    if filename.lower().endswith(img_exts):
        img_path = os.path.join(folder, filename)
        try:
            with Image.open(img_path) as img:
                # Rotate if needed
                if rotate_degrees is not None:
                    img = img.rotate(rotate_degrees, expand=True)
                # Resize if needed
                if new_size is not None:
                    img = img.resize(new_size)
                # Convert RGBA/LA to RGB if saving as JPEG
                if img_format == 'JPEG' and img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
                    else:  # 'LA'
                        background.paste(img.convert('RGBA'), mask=img.split()[1])  # 1 is the alpha channel
                    img = background
                # Save in new format
                base_name = os.path.splitext(filename)[0]
                out_path = os.path.join(output_folder, f"{base_name}.{format_input}")
                img.save(out_path, img_format)
                print(f"Processed: {filename} -> {out_path}")
        except Exception as e:
            print(f"Failed to process {filename}: {e}")
