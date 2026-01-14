



from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image, ImageEnhance, ImageFilter
from tkinter import filedialog
import os
from ttkbootstrap import Style

# Displaying Image
def display_image(img):
    disp_image = ImageTk.PhotoImage(img)
    panel.configure(image=disp_image)
    panel.image = disp_image

# Brightness Slider
def brightness_callback(brightness_pos):
    brightness_pos = float(brightness_pos)
    global output_image
    enhancer = ImageEnhance.Brightness(img)
    output_image = enhancer.enhance(brightness_pos)
    display_image(output_image)

# Contrast Slider
def contrast_callback(contrast_pos):
    contrast_pos = float(contrast_pos)
    global output_image
    enhancer = ImageEnhance.Contrast(img)
    output_image = enhancer.enhance(contrast_pos)
    display_image(output_image)

# Sharpness Slider
def sharpen_callback(sharpness_pos):
    sharpness_pos = float(sharpness_pos)
    global output_image
    enhancer = ImageEnhance.Sharpness(img)
    output_image = enhancer.enhance(sharpness_pos)
    display_image(output_image)

# Color Slider
def color_callback(color_pos):
    color_pos = float(color_pos)
    global output_image
    enhancer = ImageEnhance.Color(img)
    output_image = enhancer.enhance(color_pos)
    display_image(output_image)

# Rotate
def rotate():
    global img
    img = img.rotate(90)
    display_image(img)

# Flip
def flip():
    global img
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    display_image(img)

# Blur
def blur():
    global img
    img = img.filter(ImageFilter.BLUR)
    display_image(img)

# Emboss
def emboss():
    global img
    img = img.filter(ImageFilter.EMBOSS)
    display_image(img)

# Edge Enhance
def edge_enhance():
    global img
    img = img.filter(ImageFilter.FIND_EDGES)
    display_image(img)

# Resize
def resize():
    global img
    img = img.resize((200, 300))
    display_image(img)

# Crop
def crop():
    global img
    img = img.crop((100, 100, 400, 400))
    display_image(img)

# Reset Function
def reset():
    mains.destroy()
    os.popen("img_editor.py")

# Open images from file explorer
def change_img():
    global img
    imgname = filedialog.askopenfilename(title="Change Image")
    if imgname:
        img = Image.open(imgname)
        img = img.resize((480,360))
        display_image(img)

# Save edited images
def save():
    global img
    savefile = filedialog.asksaveasfile(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if savefile:
        output_image.save(savefile, "PNG")

# Close window
def close():
    mains.destroy()

mains = Tk()
mains.title("Image Editor")
mains.resizable(width=False, height=False)

style = Style(theme="vapor")
style.configure("TButton", font=("Helvetica", 12))
style.configure("Horizontal.TScale", padding=10, thickness=30)

# Default image in editor
img = Image.open("abc.jpg")
img = img.resize((480, 360))

# Creating panel to display image
panel = Label(mains)
panel.grid(row=0, column=0, rowspan=10, padx=(10,200), pady=(50,130))
display_image(img)

# Necessary editing buttons and sliders

# Brightness Slider
brightness_slider = ttk.Scale(mains,from_=0,to=2,orient=HORIZONTAL,command=brightness_callback,style="Horizontal.TScale")
brightness_slider.set(1)
brightness_slider.place(x=550, y=50)

# Contrast Slider
contrast_slider = ttk.Scale(mains,from_=0,to=2,orient=HORIZONTAL,command=contrast_callback,style="Horizontal.TScale")
contrast_slider.set(1)
contrast_slider.place(x=550, y=100)

# Sharpness Slider
sharpness_label = ttk.Label(mains, text="Contrast", style='info.TLabel')
sharpness_slider = ttk.Scale(mains, from_=0,to=2,orient=HORIZONTAL,command=sharpen_callback,style="Horizontal.TScale")
sharpness_slider.set(1)
sharpness_slider.place(x=550, y=150)

# Color Slider
color_slider = ttk.Scale(mains,from_=0,to=2,orient=HORIZONTAL,command=color_callback,style="Horizontal.TScale")
color_slider.set(1)
color_slider.place(x=550, y=200)

# Close button
btn_close = ttk.Button(mains,text="X",command=close,style="danger.Outline.TButton")
btn_close.place(x=620, y=420)

# Save button
btn_save = ttk.Button(mains,text="✓",command=save,style="success.Outline.TButton")
btn_save.place(x=540, y=420)

# Reset all button
reset_button = ttk.Button(mains,text="Reset",width= 15, command=reset,style="primary.TButton")
reset_button.place(x=10, y=420)

# Change image button
btn_change_img = ttk.Button(mains,text="Change Image",width=15,command=change_img,style="secondary.TButton")
btn_change_img.place(x=172, y=420)

# Edge Enhance button
btn_edge_enhance = ttk.Button(mains,text="EdgeEnhance",width=15,command=edge_enhance,style="primary.TButton")
btn_edge_enhance.place(x=334, y=420)

# Rotate button
btn_rotate = ttk.Button(mains,text="Rotate",width=15,command=rotate,style="secondary.TButton")
btn_rotate.place(x=10, y=460)

# Flip button
btn_flip = ttk.Button(mains,text="Flip",width=15,command=flip,style="primary.TButton")
btn_flip.place(x=172, y=460)

# Resize button
btn_resize = ttk.Button(mains,text="Resize",width=15,command=resize,style="secondary.TButton")
btn_resize.place(x=334, y=460)

# Crop button
btn_crop = ttk.Button(mains,text="Crop",width=15,command=crop,style="primary.TButton")
btn_crop.place(x=10, y=500)

# Blur button
btn_blur = ttk.Button(mains,text="Blur",width=15,command=blur,style="secondary.TButton")
btn_blur.place(x=172, y=500)

# Emboss button
btn_emboss = ttk.Button(mains,text="Emboss",width=15,command=emboss,style="TButton")
btn_emboss.place(x=334, y=500)

mains.mainloop()
