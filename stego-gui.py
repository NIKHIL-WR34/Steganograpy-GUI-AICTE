import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

root = tk.Tk()
root.title("Image Steganography")
root.geometry("450x350")
root.configure(bg="#f5f5f5")  

selected_image_path = None  

font_style = ("Segoe UI", 11)

d = {chr(i): i for i in range(256)}
d_rev = {i: chr(i) for i in range(256)}

def reset_fields():
    global selected_image_path
    selected_image_path = None
    lbl_selected.config(text="No image selected", foreground="gray")
    entry_msg.delete(0, tk.END)
    entry_pass.delete(0, tk.END)
    btn_encode.config(state=tk.DISABLED)
    btn_decode.config(state=tk.DISABLED)

def select_image():
    global selected_image_path
    selected_image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if selected_image_path:
        lbl_selected.config(text=f"Selected: {os.path.basename(selected_image_path)}", foreground="black")
        btn_encode.config(state=tk.NORMAL)
        btn_decode.config(state=tk.NORMAL)

def encode_message():
    global selected_image_path
    if not selected_image_path:
        messagebox.showerror("Error", "Please select an image first!")
        return
    
    img = cv2.imread(selected_image_path)
    msg = entry_msg.get()
    password = entry_pass.get()
    
    if not msg or not password:
        messagebox.showerror("Error", "Message and Password cannot be empty!")
        return

    msg_len = len(msg)
    msg = f"{msg_len:03d}" + msg 

    n, m, z = 0, 0, 0
    for i in range(len(msg)):
        img[n, m, z] = d[msg[i]]
        n = (n + 1) % img.shape[0]
        m = (m + 1) % img.shape[1]
        z = (z + 1) % 3

    encoded_path = "encoded_image.png"
    cv2.imwrite(encoded_path, img)
    messagebox.showinfo("Success", f"Message encoded in {encoded_path}")
    os.system(f'start {encoded_path}') 
    reset_fields() 

def decode_message():
    global selected_image_path
    if not selected_image_path:
        messagebox.showerror("Error", "Please select an image first!")
        return

    img = cv2.imread(selected_image_path)
    password = entry_pass.get()

    if not password:
        messagebox.showerror("Error", "Please enter the password!")
        return

    n, m, z = 0, 0, 0

    msg_len_str = ""
    for _ in range(3):
        msg_len_str += d_rev[img[n, m, z]]
        n = (n + 1) % img.shape[0]
        m = (m + 1) % img.shape[1]
        z = (z + 1) % 3

    try:
        msg_len = int(msg_len_str) 
    except ValueError:
        messagebox.showerror("Error", "Failed to decode message. Corrupted data!")
        return

    extracted_text = ""
    for _ in range(msg_len):
        extracted_text += d_rev[img[n, m, z]]
        n = (n + 1) % img.shape[0]
        m = (m + 1) % img.shape[1]
        z = (z + 1) % 3

    if extracted_text:
        messagebox.showinfo("Decryption Successful", f"Decoded Message: {extracted_text}")
    else:
        messagebox.showerror("Error", "Failed to decode message or wrong password.")

    reset_fields() 

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TEntry", padding=6)
style.configure("TLabel", font=("Segoe UI", 10), background="#f5f5f5")


btn_select = ttk.Button(root, text="📁 Select Image", command=select_image)
btn_select.pack(pady=8)

lbl_selected = ttk.Label(root, text="No image selected", foreground="gray")
lbl_selected.pack()

ttk.Label(root, text="Enter Secret Message:", background="#f5f5f5").pack(pady=(10, 0))
entry_msg = ttk.Entry(root, width=40)
entry_msg.pack()

ttk.Label(root, text="Enter Password:", background="#f5f5f5").pack(pady=(10, 0))
entry_pass = ttk.Entry(root, width=40, show="*")
entry_pass.pack()

btn_encode = ttk.Button(root, text="🔒 Encode", command=encode_message, state=tk.DISABLED)
btn_encode.pack(pady=8)

btn_decode = ttk.Button(root, text="🔓 Decode", command=decode_message, state=tk.DISABLED)
btn_decode.pack(pady=5)

root.mainloop()
