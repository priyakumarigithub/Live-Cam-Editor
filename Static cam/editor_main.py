#Final Code for Static Image Editor


import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
from ttkbootstrap import Style



def open_image():
    global img, img_tk, img_label
    file_path = filedialog.askopenfilename(title="Open Image")
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((400, 400))  # Resize the image to fit in the panel
        img_tk = ImageTk.PhotoImage(img)
        img_label.config(image=img_tk)


def update_adjustments(event=None):
    brightness = float(brightness_scale.get()) / 50.0
    contrast = float(contrast_scale.get()) / 50.0
    sharpness = float(sharpness_scale.get()) / 50.0

    enhancer = ImageEnhance.Brightness(img)
    img_enhanced = enhancer.enhance(brightness)

    enhancer = ImageEnhance.Contrast(img_enhanced)
    img_enhanced = enhancer.enhance(contrast)

    enhancer = ImageEnhance.Sharpness(img_enhanced)
    img_enhanced = enhancer.enhance(sharpness)

    img_tk_enhanced = ImageTk.PhotoImage(img_enhanced)
    img_label.config(image=img_tk_enhanced)
    img_label.image = img_tk_enhanced


def rotate():
    global img
    img = img.rotate(90)
    img_tk = ImageTk.PhotoImage(img)
    img_label.config(image=img_tk)
    img_label.image = img_tk


def flip():
    global img
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    img_tk = ImageTk.PhotoImage(img)
    img_label.config(image=img_tk)
    img_label.image = img_tk


def blur():
    global img
    img = img.filter(ImageFilter.BLUR)
    img_tk = ImageTk.PhotoImage(img)
    img_label.config(image=img_tk)
    img_label.image = img_tk


def emboss():
    global img
    img = img.filter(ImageFilter.EMBOSS)
    img_tk = ImageTk.PhotoImage(img)
    img_label.config(image=img_tk)
    img_label.image = img_tk


def edge_enhance():
    global img
    img = img.filter(ImageFilter.FIND_EDGES)
    img_tk = ImageTk.PhotoImage(img)
    img_label.config(image=img_tk)
    img_label.image = img_tk


def resize():
    global img
    img = img.resize((200, 300))
    img_tk = ImageTk.PhotoImage(img)
    img_label.config(image=img_tk)
    img_label.image = img_tk


def crop():
    global img
    img = img.crop((100, 100, 400, 400))
    img_tk = ImageTk.PhotoImage(img)
    img_label.config(image=img_tk)
    img_label.image = img_tk

def change_img():
    global img
    imgname = filedialog.askopenfilename(title="Change Image")
    if imgname:
        img = Image.open(imgname)
        img = img.resize((480, 360))
        img_tk = ImageTk.PhotoImage(img)
        img_label.config(image=img_tk)
        img_label.image = img_tk

def save():
    global img
    savefile = filedialog.asksaveasfile(defaultextension=".jpg")
    if savefile:
        img_enhanced = img.copy()  # Create a copy of the original image
        enhancer = ImageEnhance.Brightness(img_enhanced)
        brightness = float(brightness_scale.get()) / 50.0
        img_enhanced = enhancer.enhance(brightness)
        enhancer = ImageEnhance.Contrast(img_enhanced)
        contrast = float(contrast_scale.get()) / 50.0
        img_enhanced = enhancer.enhance(contrast)
        enhancer = ImageEnhance.Sharpness(img_enhanced)
        sharpness = float(sharpness_scale.get()) / 50.0
        img_enhanced = enhancer.enhance(sharpness)
        img_rgb = img_enhanced.convert("RGB")
        img_rgb.save(savefile.name)
    
def reset():
    global img, img_tk

    # Reset the image to its original state
    img = Image.open("Static cam\default1.jpg")
    img.thumbnail((400, 400))
    img_tk = ImageTk.PhotoImage(img)
    img_label.config(image=img_tk)
    img_label.image = img_tk

    # Reset the sliders to their default values
    brightness_scale.set(50)
    contrast_scale.set(50)
    sharpness_scale.set(50)

def close():
    root.destroy()

root = tk.Tk()
root.title("Static Image Editor")
root.geometry("800x400")

#Style for ttkbootstrap
style = Style(theme="vapor")
style.configure("TButton", font=("Helvetica"))
style.configure("Horizontal.TScale")

# Add the text "Image Editor" at the top
label = tk.Label(root, text="Image Editor", font=("Perpetua Titling MT", 30), fg='white')
label.pack(side=tk.TOP, pady=0)

# Default image in editor
img = Image.open("Static cam\default1.jpg")
img = img.resize((400, 400))

# Left panel to display the image
left_panel = tk.Frame(root)
left_panel.pack(side=tk.LEFT, padx=10, pady=10)

img_label = tk.Label(left_panel)
img_label.pack()

# Right panel for sliders
right_panel = tk.Frame(root)
right_panel.pack(side=tk.TOP, padx=10, pady=10)

# Create style for the sliders
style = Style(theme='morph')

# Brightness slider
brightness_label = ttk.Label(right_panel, text="Brightness")
brightness_label.pack(pady=10)
brightness_scale = ttk.Scale(right_panel, from_=0, to=100, orient=tk.HORIZONTAL, command=update_adjustments)
brightness_scale.set(50)
brightness_scale.pack()

# Contrast slider
contrast_label = ttk.Label(right_panel, text="Contrast")
contrast_label.pack(pady=10)
contrast_scale = ttk.Scale(right_panel, from_=0, to=100, orient=tk.HORIZONTAL, command=update_adjustments)
contrast_scale.set(50)
contrast_scale.pack()

# Sharpness slider
sharpness_label = ttk.Label(right_panel, text="Sharpness")
sharpness_label.pack(pady=10)
sharpness_scale = ttk.Scale(right_panel, from_=0, to=100, orient=tk.HORIZONTAL, command=update_adjustments)
sharpness_scale.set(50)
sharpness_scale.pack()

# Buttons for additional functions
# Bottom panel for buttons
bottom_panel = tk.Frame(root)
bottom_panel.pack(side=tk.BOTTOM, padx=10, pady=10)

# Button row 1
row1_frame = tk.Frame(bottom_panel)
row1_frame.pack(side=tk.TOP)

rotate_button = tk.Button(row1_frame, text="Rotate", command=rotate, width=10)
rotate_button.pack(side=tk.LEFT, padx=5, pady=5)

flip_button = tk.Button(row1_frame, text="Flip", command=flip, width=10)
flip_button.pack(side=tk.LEFT, padx=5, pady=5)

blur_button = tk.Button(row1_frame, text="Blur", command=blur, width=10)
blur_button.pack(side=tk.LEFT, padx=5, pady=5)

# Button row 2
row2_frame = tk.Frame(bottom_panel)
row2_frame.pack(side=tk.TOP)

emboss_button = tk.Button(row2_frame, text="Emboss", command=emboss, width=10)
emboss_button.pack(side=tk.LEFT, padx=5,pady=5)

crop_button = tk.Button(row2_frame, text="Crop", command=crop, width=10)
crop_button.pack(side=tk.LEFT, padx=5,pady=5)

resize_button = tk.Button(row2_frame, text="Resize", command=resize, width=10)
resize_button.pack(side=tk.LEFT, padx=5,pady=5)

# Button row 3
row3_frame = tk.Frame(bottom_panel)
row3_frame.pack(side=tk.TOP)

edge_enhance_button = tk.Button(row3_frame, text="Edge Enhance", command=edge_enhance, width=16)
edge_enhance_button.pack(side=tk.LEFT, padx=5,pady=5)

btn_change_img = tk.Button(row3_frame,text="Change Image",command=change_img, width=16)
btn_change_img.pack(side=tk.LEFT, padx=5,pady=5)

# Button row 4
row4_frame = tk.Frame(bottom_panel)
row4_frame.pack(side=tk.TOP)

save_button = tk.Button(row4_frame, text="✓",command=save, width=10)
save_button.pack(side=tk.LEFT, padx=5,pady=5)

reset_button = tk.Button(row4_frame, text="Reset", command=reset, width=10)
reset_button.pack(side=tk.LEFT, padx=5,pady=5)

btn_close = tk.Button(row4_frame,text="X",command=close, width=10)
btn_close.pack(side=tk.LEFT, padx=5,pady=5)

root.mainloop()
