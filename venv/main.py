# main.py

import os
import tkinter as tk
from tkinter import filedialog, LEFT, ttk, Toplevel
from pdf2image import convert_from_path
from PIL import Image
import pytesseract as pt
import threading


pt.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'


class File:
    def __init__(self, file_path):
        self.path = file_path
        self.name, self.extension = \
            os.path.splitext(os.path.basename(self.path))


def folder_dialog():
    global FOLDER_PATH
    dir = "C:\\Users\\Seiya\\source\\repos\\document_parser\\sample_docs"
    FOLDER_PATH = filedialog.askdirectory(parent=root, initialdir=dir)
    lbl["text"] = FOLDER_PATH


def get_files(folder_path):
    global FILES
    paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]
    file_paths = [p for p in paths if os.path.isfile(p)]
    FILES = [File(p) for p in file_paths]
    body = "Ext" + "\t" + "Filename" + "\n\n"
    for f in FILES:
        body += f.extension + "\t" + f.name + "\n"
    lbl_files["text"] = body


def abort():
    global running
    running = False
    lbl_abort["text"] = "Abort requested"


def start_process(files):
    print("start new thread")
    t = threading.Thread(target=process(files))
    t.start()

def process(files):
    # Set global running
    global running
    running = True

    # Progress bar
    popup = tk.Tk()
    popup.geometry("250x150+500+500")
    tk.Label(popup, text="Files being processed").grid(row=0, column=0)
    progress = 0
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=100)
    progress_bar.grid(row=1, column=0)
    popup.pack_slaves()
    progress_step = float(100.0/len(files))

    for f in files[:5]:
        popup.update()
        if not running:
            break
        if f.extension == ".pdf":
            # Convert to png images (if not already)
            images = convert_from_path(f.path)

            # Save as temp file
            temp_paths = []
            for i in range(len(images)):
                temp_path = "temp\\page_" + str(i) + ".jpg"
                images[i].save(temp_path, "JPEG")
                temp_paths.append(temp_path)
            
            # Convert image to text
            for p in temp_paths:
                """
                print("Processing...", p)
                image = Image.open(p)
                #image = image.resize((300,150))
                custom_config = r'-l eng --oem 3 --psm 6' 
                text = pt.image_to_string(image, config=custom_config)
                print(text)"""

                # Delete temp file
                os.remove(p)
        progress += progress_step
        progress_var.set(progress)

    popup.destroy()


if __name__ == "__main__":
    # Setup root
    root = tk.Tk()
    root.title("Document Parser Program")
    root_width = 1000
    root_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - root_width/2)
    center_y = int(screen_height/2 - root_height/2)
    root.geometry(f"{root_width}x{root_height}+{center_x}+{center_y}")
    root.resizable(False, False)
    root.iconbitmap("assets\\root_icon.ico")

    # Folder dialog button
    btn_get_folder = tk.Button(
        root, text="Select folder", command=lambda: folder_dialog())
    btn_get_folder.pack()

    # Folder path label
    lbl = tk.Label(root, text="No folder selected yet")
    lbl.pack()

    # Get files in folder button
    btn_get_files = tk.Button(
        root, text="Get files", command=lambda: get_files(FOLDER_PATH))
    btn_get_files.pack()

    # Found files label
    lbl_files = tk.Label(root, text="", justify=LEFT)
    lbl_files.pack()

    # Start process button
    btn_process = tk.Button(
        root, text="Start", command=lambda: start_process(FILES))
    btn_process.pack()

    # Cancel button
    btn_cancel = tk.Button(root, text="Abort", command=lambda: abort()).pack()

    # Found files label
    lbl_abort = tk.Label(root, text="")
    lbl_abort.pack()

    # Show root
    root.mainloop()
