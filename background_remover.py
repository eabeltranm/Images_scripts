import os
import threading
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# --- INTEGRAL IMPORT FIX ---
# We define these as None first so the editor knows they exist even if import fails
remove_fn = None
session_fn = None
IMPORT_READY = False

try:
    from rembg import remove, new_session
    remove_fn = remove
    session_fn = new_session
    IMPORT_READY = True
except ImportError:
    pass

class HighPrecisionRemover:
    def __init__(self, root):
        self.root = root
        self.root.title("Teacher's High-Precision Image Tool")
        self.root.geometry("700x550")
        self.session = None
        self.setup_ui()

    def setup_ui(self):
        # Folder Selection
        folder_frame = ttk.LabelFrame(self.root, text=" 1. Folder Selection ", padding=10)
        folder_frame.pack(fill="x", padx=20, pady=10)
        self.path_var = tk.StringVar()
        ttk.Entry(folder_frame, textvariable=self.path_var).pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(folder_frame, text="Browse", command=self.browse).pack(side="right")

        # Engine Settings
        engine_frame = ttk.LabelFrame(self.root, text=" 2. Engine Settings ", padding=10)
        engine_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(engine_frame, text="Model:").grid(row=0, column=0, padx=5)
        self.model_var = tk.StringVar(value="isnet-general-use")
        model_chooser = ttk.Combobox(engine_frame, textvariable=self.model_var, state="readonly")
        model_chooser['values'] = ("isnet-general-use", "u2net", "u2net_human_seg")
        model_chooser.grid(row=0, column=1, padx=5)

        # Progress and Status
        self.status_var = tk.StringVar(value="System Ready")
        ttk.Label(self.root, textvariable=self.status_var).pack(pady=5)
        self.progress_var = tk.DoubleVar()
        ttk.Progressbar(self.root, variable=self.progress_var, maximum=100).pack(fill="x", padx=20, pady=10)

        self.btn = ttk.Button(self.root, text="Start Processing", command=self.start_thread)
        self.btn.pack(pady=20)

    def browse(self):
        directory = filedialog.askdirectory()
        if directory: self.path_var.set(directory)

    def start_thread(self):
        # Error fix: Check if callable before starting
        if not IMPORT_READY or remove_fn is None or session_fn is None:
            messagebox.showerror("Error", "AI Engine not found. Run the terminal fix!")
            return
        threading.Thread(target=self.run_process, daemon=True).start()

    def run_process(self):
        # We use local references to satisfy the editor's "None" check
        rem_func = remove_fn
        sess_func = session_fn
        
        if rem_func is None or sess_func is None: return

        self.btn.state(['disabled'])
        folder = self.path_var.get()
        files = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        try:
            self.status_var.set("Loading AI Model...")
            self.session = sess_func(self.model_var.get())
            
            for i, name in enumerate(files):
                self.status_var.set(f"Processing: {name}")
                input_p = os.path.join(folder, name)
                output_p = os.path.join(folder, f"clean_{os.path.splitext(name)[0]}.png")

                with Image.open(input_p) as img:
                    # High precision removal
                    result = rem_func(
                        img, 
                        session=self.session,
                        alpha_matting=True,
                        alpha_matting_foreground_threshold=240
                    )
                    
                    # --- INTEGRAL SAVE FIX ---
                    # Handles all 3 possible return types from rembg to fix "save" attribute errors
                    if isinstance(result, Image.Image):
                        result.save(output_p)
                    elif isinstance(result, np.ndarray):
                        Image.fromarray(result).save(output_p)
                    elif isinstance(result, bytes):
                        with open(output_p, "wb") as f:
                            f.write(result)

                self.progress_var.set(((i+1)/len(files))*100)

            self.status_var.set("Successfully Completed!")
            messagebox.showinfo("Success", "All images processed with high precision.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.btn.state(['!disabled'])

if __name__ == "__main__":
    root = tk.Tk()
    app = HighPrecisionRemover(root)
    root.mainloop()