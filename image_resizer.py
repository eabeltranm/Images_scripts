import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Resizer")
        self.root.geometry("400x300")
        
        # Create and set up the main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Folder selection
        ttk.Label(main_frame, text="Select Folder:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.folder_path = tk.StringVar()
        folder_entry = ttk.Entry(main_frame, textvariable=self.folder_path, width=40)
        folder_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_folder).grid(row=0, column=2, pady=5)
        
        # Width input
        ttk.Label(main_frame, text="Width (pixels):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.width_var = tk.StringVar()
        width_entry = ttk.Entry(main_frame, textvariable=self.width_var, width=10)
        width_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Height input
        ttk.Label(main_frame, text="Height (pixels):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.height_var = tk.StringVar()
        height_entry = ttk.Entry(main_frame, textvariable=self.height_var, width=10)
        height_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=3, column=0, columnspan=3, sticky=tk.W+tk.E, pady=10)
        
        # Status label
        self.status_var = tk.StringVar()
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=4, column=0, columnspan=3, pady=5)
        
        # Resize button
        ttk.Button(main_frame, text="Resize Images", command=self.resize_images).grid(row=5, column=0, columnspan=3, pady=10)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)

    def resize_images(self):
        folder_path = self.folder_path.get()
        
        try:
            new_width = int(self.width_var.get())
            new_height = int(self.height_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for width and height")
            return

        if not folder_path:
            messagebox.showerror("Error", "Please select a folder")
            return

        if not os.path.exists(folder_path):
            messagebox.showerror("Error", f"Folder '{folder_path}' does not exist")
            return

        # Create output folder
        output_folder = os.path.join(folder_path, "resized")
        os.makedirs(output_folder, exist_ok=True)

        # Get list of PNG files
        png_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.png')]
        total_files = len(png_files)

        if total_files == 0:
            messagebox.showinfo("Info", "No PNG files found in the selected folder")
            return

        # Process each file
        for i, filename in enumerate(png_files):
            file_path = os.path.join(folder_path, filename)
            try:
                with Image.open(file_path) as img:
                    resized_img = img.resize((new_width, new_height))
                    output_path = os.path.join(output_folder, filename)
                    resized_img.save(output_path)
                    
                    # Update progress
                    progress = (i + 1) / total_files * 100
                    self.progress_var.set(progress)
                    self.status_var.set(f"Processing: {i+1}/{total_files}")
                    self.root.update()

            except Exception as e:
                messagebox.showerror("Error", f"Error processing {filename}: {str(e)}")
                return

        self.status_var.set("Completed!")
        messagebox.showinfo("Success", "All images have been resized successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()