#Final Code


import tkinter as tk
from ttkbootstrap import Style
from PIL import Image, ImageTk
import subprocess

def open_live_cam():
    subprocess.Popen(["python", "Live cam\live_main.py"])

def open_img_edi():
    subprocess.Popen(["python", "Static cam\editor_main.py"])

def open_han_det():
    subprocess.Popen(["python", "Live cam Hand Detection\det_main.py"])

# Create the main Tkinter window
window = tk.Tk()
window.title('Minor Project')
window.geometry('600x500')

# Create a ttkbootstrap Style object
style = Style(theme='morph')

# Load button images
image1 = Image.open('img/button1.png')
image2 = Image.open('img/button2.png')
image3 = Image.open('img/button3.png')

# Resize button images to fit the desired size
image1 = image1.resize((50, 50), Image.ANTIALIAS).convert("RGBA")
image2 = image2.resize((50, 50), Image.ANTIALIAS).convert("RGBA")
image3 = image3.resize((50, 50), Image.ANTIALIAS).convert("RGBA")

# Create PhotoImage objects from the resized images
image1_tk = ImageTk.PhotoImage(image1)
image2_tk = ImageTk.PhotoImage(image2)
image3_tk = ImageTk.PhotoImage(image3)

# Create a custom button class with round appearance
class RoundButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(bd=0, relief=tk.FLAT, highlightthickness=0)
        self.config(width=50, height=50)
        self.config(image=kwargs['image'], compound=tk.CENTER)
        self.config(command=kwargs['command'])
        self.config(cursor='hand2')
        self.config(background='#190831')

# Create the custom round buttons
button1 = RoundButton(window, image=image1_tk, command=open_live_cam)
button2 = RoundButton(window, image=image2_tk, command=open_img_edi)
button3 = RoundButton(window, image=image3_tk, command=open_han_det)

# Place the buttons in the center row
button1.place(relx=0.25, rely=0.6, anchor=tk.CENTER)
button2.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
button3.place(relx=0.75, rely=0.6, anchor=tk.CENTER)

# Add the text below the buttons
label1 = tk.Label(window, text="Live Cam", font=("Perpetua Titling MT", 12), fg='white')
label1.place(relx=0.25, rely=0.7, anchor=tk.CENTER)
label2 = tk.Label(window, text="Image Editor", font=("Perpetua Titling MT", 12), fg='white')
label2.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
label3 = tk.Label(window, text="Hand Detection", font=("Perpetua Titling MT", 12), fg='white')
label3.place(relx=0.75, rely=0.7, anchor=tk.CENTER)

# Add the text "MINOR PROJECT" at the top
label = tk.Label(window, text="MINOR PROJECT", font=("Perpetua Titling MT", 35), fg='white')
label.pack(side=tk.TOP, pady=20)
label = tk.Label(window, text="Live Cam Editor, Image Editor, and Hand Detection are cutting-edge", font=("Perpetua", 15))
label.pack(side=tk.TOP, pady=5)
label = tk.Label(window, text="tools that harness the power of computer vision and image", font=("Perpetua", 15))
label.pack(side=tk.TOP, pady=5)
label = tk.Label(window, text="processing to provide captivating visual experiences, precise", font=("Perpetua", 15))
label.pack(side=tk.TOP, pady=5)
label = tk.Label(window, text="image editing capabilities, and advanced hand tracking functionalities.", font=("Perpetua", 15))
label.pack(side=tk.TOP, pady=5)

# Add the text Footer
label1 = tk.Label(window, text="Shaury Shobit & Priya Kumari", font=("Harrington", 9), fg='white')
label1.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

# Start the Tkinter event loop
window.mainloop()
