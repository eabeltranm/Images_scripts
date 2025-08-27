import os
import numpy as np
from PIL import Image
from rembg import remove
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Background Remover")
        self.root.geometry("600x400")
        
        # Configure root grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(1, weight=1)
        
        # Directory selection
        self.dir_var = tk.StringVar()
        ttk.Label(main_frame, text="Image Directory:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.dir_var, width=50).grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(main_frame, text="Browse", command=self.select_directory).grid(row=0, column=2, padx=5, pady=5)
        
        # Create frame for the listbox and scrollbar
        list_frame = ttk.Frame(root)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Listbox to show files
        self.file_listbox = tk.Listbox(list_frame, height=10)
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Progress frame
        progress_frame = ttk.Frame(root)
        progress_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.S), padx=10, pady=10)
        progress_frame.columnconfigure(0, weight=1)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        self.status_label.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Process button
        self.process_button = ttk.Button(progress_frame, text="Remove Backgrounds", command=self.process_images)
        self.process_button.grid(row=2, column=0, pady=10)
        
    def select_directory(self):
        directory_path = filedialog.askdirectory(title="Select Image Directory")
        if directory_path:
            self.dir_var.set(directory_path)
            self.update_file_list(directory_path)
    
    def update_file_list(self, directory):
        self.file_listbox.delete(0, tk.END)
        if os.path.isdir(directory):
            image_files = [f for f in os.listdir(directory) 
                         if f.lower().endswith((".png", ".jpg", ".jpeg"))]
            for file in image_files:
                self.file_listbox.insert(tk.END, file)
            
            if not image_files:
                self.status_var.set("No image files found in selected directory")
            else:
                self.status_var.set(f"Found {len(image_files)} image(s)")
    
    def process_images(self):
        directory_path = self.dir_var.get()
        if not directory_path:
            messagebox.showerror("Error", "Please select a directory first")
            return
        
        if not os.path.isdir(directory_path):
            messagebox.showerror("Error", "Selected directory does not exist")
            return
        
        image_files = [f for f in os.listdir(directory_path) 
                      if f.lower().endswith((".png", ".jpg", ".jpeg"))]
        
        if not image_files:
            messagebox.showinfo("Info", "No image files found in selected directory")
            return
        
        # Disable the process button while processing
        self.process_button.state(['disabled'])
        
        total_files = len(image_files)
        processed = 0
        
        for filename in image_files:
            try:
                input_path = os.path.join(directory_path, filename)
                output_filename = os.path.splitext(filename)[0] + "_nobg.png"
                output_path = os.path.join(directory_path, output_filename)
                
                self.status_var.set(f"Processing: {filename}")
                self.root.update()
                
                with Image.open(input_path) as img:
                    img = img.convert("RGBA")
                    output_img = remove(img)
                    
                    if isinstance(output_img, Image.Image):
                        output_img.save(output_path)
                    elif isinstance(output_img, bytes):
                        with open(output_path, 'wb') as f:
                            f.write(output_img)
                    elif isinstance(output_img, np.ndarray):
                        Image.fromarray(output_img).save(output_path)
                    else:
                        raise TypeError(f"Unexpected output type from rembg: {type(output_img)}")
                
                processed += 1
                progress = (processed / total_files) * 100
                self.progress_var.set(progress)
                self.root.update()
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not process {filename}: {str(e)}")
        
        # Re-enable the process button
        self.process_button.state(['!disabled'])
        
        if processed == total_files:
            self.status_var.set("Completed successfully!")
            messagebox.showinfo("Success", "All images processed successfully!")
        else:
            self.status_var.set(f"Completed with {total_files - processed} errors")

if __name__ == "__main__":
    root = tk.Tk()
    app = BackgroundRemoverApp(root)
    root.mainloop()
