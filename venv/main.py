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
        self.text = ""


def folder_dialog():
    dir = "C:\\Users\\Seiya\\source\\repos\\document_parser\\sample_docs"
    folder_path = filedialog.askdirectory(parent=root, initialdir=dir)
    lbl["text"] = folder_path

    global FILES
    paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]
    file_paths = [p for p in paths if os.path.isfile(p)]
    FILES = [File(p) for p in file_paths]
    body = "Ext" + "\t" + "Filename" + "\n\n"
    for f in FILES:
        body += f.extension + "\t" + f.name + "\n"
    lbl_files["text"] = body


def process(files):
    lbl_thread["text"] = "Thread running"
    for f in files:
        if abort:
            lbl_thread["text"] = "Process aborted"
            btn_process["state"] = "active"
            btn_abort["state"] = "disabled"
            return
        if f.extension == ".pdf":
            # Convert to png images (if not already)
            images = convert_from_path(f.path)

            # Process image
            text = ""
            for i in range(len(images)):
                if abort:
                    lbl_thread["text"] = "Process aborted"
                    btn_process["state"] = "active"
                    btn_abort["state"] = "disabled"
                    return
                # Save image
                temp_path = "temp\\page_" + str(i) + ".jpg"
                images[i].save(temp_path, "JPEG")

                # Convert image
                print("Processing...", temp_path)
                image = Image.open(temp_path)
                #image = image.resize((300,150))
                custom_config = r'-l eng --oem 3 --psm 6' 
                text += pt.image_to_string(image, config=custom_config)

                # Delete image
                os.remove(temp_path)
            
            # Assign text to file
            f.text = text
            print("Text count: ", len(text))

    lbl_thread["text"] = "Process finished"
    btn_process["state"] = "active"
    btn_abort["state"] = "disabled"
    return


def start_process(files):
    global abort
    abort = False
    new_thread = threading.Thread(target=process, args=(files,))
    new_thread.start()
    btn_abort["state"] = "active"
    btn_process["state"] = "disabled"
    

def abort_process():
    global abort
    abort = True
    lbl_thread["text"] = "Abort requested..."
    
def donothing():
   x = 0

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

    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=donothing)
    filemenu.add_command(label="Open", command=donothing)
    filemenu.add_command(label="Save", command=donothing)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index", command=donothing)
    helpmenu.add_command(label="About...", command=donothing)
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.config(menu=menubar)

    # Folder dialog button
    btn_get_folder = tk.Button(
        root, text="Select folder", command=lambda: folder_dialog())
    btn_get_folder.pack()

    # Folder path label
    lbl = tk.Label(root, text="No folder selected yet")
    lbl.pack()

    # Found files label
    lbl_files = tk.Label(root, text="", justify=LEFT)
    lbl_files.pack()

    # Start process button
    btn_process = tk.Button(
        root, text="Start", command=lambda: start_process(FILES))
    btn_process.pack()

    # Abort process button
    btn_abort = tk.Button(
        root, text="Abort", state="disabled" , command=lambda: abort_process())
    btn_abort.pack()

    # Thread status label
    lbl_thread = tk.Label(root, text="No status")
    lbl_thread.pack()

    # Show root
    root.mainloop()
