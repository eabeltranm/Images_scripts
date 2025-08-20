# How to Use the Image Enhancer Script

This guide explains how to use the `enhancer.py` script to enhance your images.

## 1. Activate the Virtual Environment

Before running the script, you need to activate the Python virtual environment. Open your command line or terminal and run the following command from the project's root directory:

```bash
.\.venv\Scripts\activate.bat
```

## 2. Run the Script

Once the virtual environment is activated, you can run the script.

### Basic Usage (Standard Enhancement)

To enhance all the images in a folder using the standard enhancement settings, use the following command. Replace `"C:\path\to\your\images"` with the actual path to your folder.

```bash
python enhancer.py "C:\path\to\your\images"
```

By default, the enhanced images will be saved in a new folder called `enhanced_images` inside the folder you specified.

### Customizing Enhancement Factors

You can customize the enhancement factors by adding optional arguments to the command.

Here are the available options:

*   `--brightness`: Adjusts the brightness. (Default: 1.2)
*   `--contrast`: Adjusts the contrast. (Default: 1.5)
*   `--sharpness`: Adjusts the sharpness. (Default: 2.0)
*   `--color`: Adjusts the color saturation. (Default: 1.5)

For all factors, a value of `1.0` means no change.

**Example:**

To make the images slightly less bright and more colorful, you could run:

```bash
python enhancer.py "C:\path\to\your\images" --brightness 1.1 --color 1.8
```

### Specifying a Different Output Folder

If you want to save the enhanced images to a different folder, you can use the `--output_folder` argument:

```bash
python enhancer.py "C:\path\to\your\images" --output_folder "C:\path\to\your\custom_output_folder"
```

## 3. Get Help

To see a full list of all the available commands and their descriptions, you can use the `-h` or `--help` flag:

```bash
python enhancer.py -h
```
