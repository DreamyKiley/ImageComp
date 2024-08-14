import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageOps
import webbrowser
import requests
from io import BytesIO
import tempfile
import os

def download_and_convert_icon(url, output_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGBA")  # Ensure the image is in RGBA mode
        
        # Convert to .ico format
        img.save(output_path, format="ICO")
        print("Icon downloaded and converted successfully.")
    except Exception as e:
        print(f"Failed to download or convert icon: {e}")

def compress_image(input_path, output_path, quality):
    try:
        # Open the image file
        img = Image.open(input_path)
        
        # Convert RGBA to RGB (JPEG doesn't support RGBA)
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        img = ImageOps.exif_transpose(img)  # Handle image rotation based on EXIF data

        # Determine the file format and save accordingly
        file_extension = os.path.splitext(output_path)[1].lower()
        
        if file_extension == '.jpg':
            img.save(output_path, "JPEG", quality=quality, optimize=True)
        elif file_extension == '.webp':
            img.save(output_path, "WEBP", quality=quality)
        else:
            raise ValueError("Unsupported file format")
        
        messagebox.showinfo("Success", "Image compressed and saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to compress image: {e}")

def browse_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.webp")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def browse_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("WebP files", "*.webp")])
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)

def compress_from_entries():
    input_path = input_entry.get()
    output_path = output_entry.get()
    if not input_path or not output_path:
        messagebox.showerror("Error", "Please provide both input and output file paths.")
        return
    compress_image(input_path, output_path, quality=95)

def show_credits():
    credits_window = tk.Toplevel(root)
    credits_window.title("Credits")
    credits_window.geometry("300x200")
    credits_window.config(bg="#f0f0f0")  # Light grey background

    # Set the application icon for the credits window
    credits_window.iconbitmap(icon_path)  # Path to the downloaded icon file

    # Title Label
    title_label = tk.Label(credits_window, text="Credits", font=("Arial", 16, "bold"), bg="#f0f0f0")
    title_label.pack(pady=10)

    # Credits Text
    text = tk.Text(credits_window, wrap=tk.WORD, height=6, width=40, font=("Arial", 12), bg="#f0f0f0", bd=0, padx=10, pady=10)
    text.pack(pady=10)

    url = "https://allmylinks.com/dreamykiley"
    additional_text = "Thank you for using ImageComp!"  # Customizable additional text

    text.insert(tk.END, "ImageComp\n\nCredit: Kiley W.\nVisit: ")
    text.insert(tk.END, url, ('url',))
    text.tag_config('url', foreground='blue', underline=True)
    text.bind("<Button-1>", lambda e: webbrowser.open(url))

    text.insert(tk.END, f"\n\n{additional_text}")

    text.config(state=tk.DISABLED)

    # Close Button
    close_button = tk.Button(credits_window, text="Close", command=credits_window.destroy, font=("Arial", 12), bg="#6c757d", fg="white")
    close_button.pack(pady=10)

def create_gui():
    global root, input_entry, output_entry, temp_dir, icon_path

    # Create a temporary directory for the icon
    temp_dir = tempfile.TemporaryDirectory()

    # Download and convert icon
    icon_url = "https://avatars.githubusercontent.com/u/86751611?v=4"
    icon_path = os.path.join(temp_dir.name, "github_icon.ico")
    download_and_convert_icon(icon_url, icon_path)
    
    root = tk.Tk()
    root.title("Image Compressor")
    root.geometry("400x450")  # Increased height from 250 to 300
    root.config(bg="#f0f0f0")  # Light grey background

    # Set the application icon
    root.iconbitmap(icon_path)  # Path to the downloaded icon file

    # Title Label
    title_label = tk.Label(root, text="Image Compressor", font=("Arial", 16, "bold"), bg="#f0f0f0")
    title_label.pack(pady=10)

    # Input file entry and button
    tk.Label(root, text="Input File:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
    input_entry = tk.Entry(root, width=50, font=("Arial", 12))
    input_entry.pack(pady=5, padx=10)
    tk.Button(root, text="Browse...", command=browse_input_file, font=("Arial", 12), bg="#007bff", fg="white").pack(pady=5)

    # Output file entry and button
    tk.Label(root, text="Output File:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
    output_entry = tk.Entry(root, width=50, font=("Arial", 12))
    output_entry.pack(pady=5, padx=10)
    tk.Button(root, text="Browse...", command=browse_output_file, font=("Arial", 12), bg="#007bff", fg="white").pack(pady=5)

    # Compress button
    tk.Button(root, text="Compress Image", command=compress_from_entries, font=("Arial", 12, "bold"), bg="#28a745", fg="white").pack(pady=15)

    # Credits button
    credits_button = tk.Button(root, text="Credits", command=show_credits, font=("Arial", 12), bg="#6c757d", fg="white")
    credits_button.pack(pady=10)

    # Ensure the temp directory is cleaned up on exit
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()


def on_closing():
    # Cleanup the temporary directory
    temp_dir.cleanup()
    root.destroy()

if __name__ == "__main__":
    create_gui()
