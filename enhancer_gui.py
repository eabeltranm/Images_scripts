
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import threading
from PIL import Image, ImageEnhance

def enhance_image(image_path, output_path, brightness, contrast, sharpness, color):
    """
    Enhances a single image and saves it to the output path.
    """
    try:
        with Image.open(image_path) as img:
            if brightness != 1.0:
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(brightness)
            if contrast != 1.0:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(contrast)
            if sharpness != 1.0:
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(sharpness)
            if color != 1.0:
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(color)
            img.save(output_path)
            return True
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False

class EnhancerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Image Enhancer")
        master.geometry("500x400")

        # --- Input Folder ---
        self.input_frame = tk.LabelFrame(master, text="Input Folder", padx=10, pady=10)
        self.input_frame.pack(padx=10, pady=10, fill="x")

        self.input_path = tk.StringVar()
        self.input_entry = tk.Entry(self.input_frame, textvariable=self.input_path, width=50)
        self.input_entry.pack(side=tk.LEFT, expand=True, fill="x", padx=(0, 10))
        self.browse_button = tk.Button(self.input_frame, text="Browse...", command=self.browse_folder)
        self.browse_button.pack(side=tk.RIGHT)

        # --- Enhancement Factors ---
        self.factors_frame = tk.LabelFrame(master, text="Enhancement Factors", padx=10, pady=10)
        self.factors_frame.pack(padx=10, pady=10, fill="x")

        self.factors = {
            "Brightness": tk.DoubleVar(value=1.2),
            "Contrast": tk.DoubleVar(value=1.5),
            "Sharpness": tk.DoubleVar(value=2.0),
            "Color": tk.DoubleVar(value=1.5),
        }

        for factor, var in self.factors.items():
            row = tk.Frame(self.factors_frame)
            row.pack(fill="x", pady=2)
            label = tk.Label(row, text=f"{factor}:", width=10, anchor="w")
            label.pack(side=tk.LEFT)
            entry = tk.Entry(row, textvariable=var, width=10)
            entry.pack(side=tk.LEFT, padx=5)

        # --- Action Buttons ---
        self.action_frame = tk.Frame(master, padx=10, pady=10)
        self.action_frame.pack(fill="x")

        self.start_button = tk.Button(self.action_frame, text="Start Enhancement", command=self.start_enhancement, bg="#4CAF50", fg="white")
        self.start_button.pack(side=tk.RIGHT)

        # --- Progress Bar & Status ---
        self.progress_frame = tk.LabelFrame(master, text="Progress", padx=10, pady=10)
        self.progress_frame.pack(padx=10, pady=10, fill="x")

        self.progress = ttk.Progressbar(self.progress_frame, orient="horizontal", length=100, mode="determinate")
        self.progress.pack(fill="x", pady=5)

        self.status_label = tk.Label(self.progress_frame, text="Select a folder to begin.", anchor="w")
        self.status_label.pack(fill="x")

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.input_path.set(folder_selected)
            self.status_label.config(text=f"Folder selected: {os.path.basename(folder_selected)}")

    def start_enhancement(self):
        input_folder = self.input_path.get()
        if not input_folder or not os.path.isdir(input_folder):
            messagebox.showerror("Error", "Please select a valid input folder.")
            return

        self.start_button.config(state=tk.DISABLED)
        self.progress["value"] = 0

        # Run enhancement in a separate thread
        thread = threading.Thread(target=self.enhancement_thread, args=(input_folder,))
        thread.start()

    def enhancement_thread(self, input_folder):
        output_folder = os.path.join(input_folder, "enhanced_images_gui")
        os.makedirs(output_folder, exist_ok=True)

        image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        total_files = len(image_files)

        if total_files == 0:
            self.master.after(0, lambda: self.status_label.config(text="No images found in the selected folder."))
            self.master.after(0, lambda: self.start_button.config(state=tk.NORMAL))
            return

        self.master.after(0, lambda: self.status_label.config(text=f"Enhancing {total_files} images..."))

        for i, filename in enumerate(image_files):
            image_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"enhanced_{filename}")
            
            success = enhance_image(image_path, output_path, 
                                    self.factors["Brightness"].get(),
                                    self.factors["Contrast"].get(),
                                    self.factors["Sharpness"].get(),
                                    self.factors["Color"].get())
            
            progress_value = int(((i + 1) / total_files) * 100)
            self.master.after(0, lambda p=progress_value: self.progress.config(value=p))

        self.master.after(0, lambda: self.status_label.config(text=f"Enhancement complete! Images saved in '{os.path.basename(output_folder)}'."))
        self.master.after(0, lambda: messagebox.showinfo("Success", f"Enhancement complete!\n\nSaved to: {output_folder}"))
        self.master.after(0, lambda: self.start_button.config(state=tk.NORMAL))

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancerGUI(root)
    root.mainloop()
