
import os
import sys
import argparse
from PIL import Image, ImageEnhance
from tqdm import tqdm

def enhance_image(image_path, output_path, brightness, contrast, sharpness, color):
    """
    Enhances a single image and saves it to the output path.
    """
    try:
        with Image.open(image_path) as img:
            # Enhance brightness
            if brightness != 1.0:
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(brightness)

            # Enhance contrast
            if contrast != 1.0:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(contrast)

            # Enhance sharpness
            if sharpness != 1.0:
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(sharpness)

            # Enhance color saturation
            if color != 1.0:
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(color)

            img.save(output_path)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def main():
    """
    Main function to parse arguments and process images.
    """
    parser = argparse.ArgumentParser(description="Enhance images in a folder.")
    parser.add_argument("input_folder", help="Path to the folder containing images.")
    parser.add_argument("--output_folder", help="Path to the folder to save enhanced images. Defaults to a new 'enhanced_images' folder inside the input folder.")
    parser.add_argument("--brightness", type=float, default=1.2, help="Brightness enhancement factor. 1.0 is original, >1.0 is brighter, <1.0 is darker.")
    parser.add_argument("--contrast", type=float, default=1.5, help="Contrast enhancement factor. 1.0 is original, >1.0 is more contrast.")
    parser.add_argument("--sharpness", type=float, default=2.0, help="Sharpness enhancement factor. 1.0 is original, >1.0 is sharper.")
    parser.add_argument("--color", type=float, default=1.5, help="Color saturation enhancement factor. 1.0 is original, >1.0 is more saturated.")

    args = parser.parse_args()

    if not os.path.isdir(args.input_folder):
        print(f"Error: Input folder not found at {args.input_folder}")
        sys.exit(1)

    output_folder = args.output_folder or os.path.join(args.input_folder, 'enhanced_images')
    os.makedirs(output_folder, exist_ok=True)

    image_files = [f for f in os.listdir(args.input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

    if not image_files:
        print(f"No images found in {args.input_folder}")
        return

    print(f"Found {len(image_files)} images to enhance.")

    with tqdm(total=len(image_files), desc="Enhancing images") as pbar:
        for filename in image_files:
            image_path = os.path.join(args.input_folder, filename)
            output_path = os.path.join(output_folder, f"enhanced_{filename}")
            enhance_image(image_path, output_path, args.brightness, args.contrast, args.sharpness, args.color)
            pbar.update(1)

    print(f"All images have been enhanced and saved to the '{output_folder}' folder.")

if __name__ == "__main__":
    main()
