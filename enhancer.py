
from PIL import Image, ImageEnhance

# Load the image
image_path = "your_image.jpg"  # Replace with your image file path
image = Image.open(image_path)

# Enhance brightness
enhancer_brightness = ImageEnhance.Brightness(image)
image = enhancer_brightness.enhance(1.2)  # Increase brightness by 20%

# Enhance contrast
enhancer_contrast = ImageEnhance.Contrast(image)
image = enhancer_contrast.enhance(1.5)  # Increase contrast by 50%

# Enhance sharpness
enhancer_sharpness = ImageEnhance.Sharpness(image)
image = enhancer_sharpness.enhance(2.0)  # Double the sharpness

# Enhance color saturation
enhancer_color = ImageEnhance.Color(image)
image = enhancer_color.enhance(1.5)  # Increase color saturation by 50%

# Save the enhanced image
image.save("enhanced_image.jpg")
print("Enhanced image saved as 'enhanced_image.jpg'")
