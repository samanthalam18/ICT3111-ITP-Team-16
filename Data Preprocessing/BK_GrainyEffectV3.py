from PIL import Image, ImageDraw, ImageEnhance, ImageTk
import random
import tkinter as tk
from tkinter import filedialog
import os
import numpy as np



class GraininessEffectApp:

    def __init__(self, master):
        self.master = master
        self.master.title("Graininess Effect App")

        self.image = None
        self.modified_image = None
        self.graininess_level = tk.IntVar(value=50)
        self.brightness_level = tk.DoubleVar(value=1.0)

        # UI controls
        self.control_frame = tk.Frame(self.master)
        self.control_frame.pack(expand=True, fill="both")
        tk.Label(self.control_frame, text="Graininess Level:").grid(row=0, column=0, padx=5, pady=5)
        tk.Scale(self.control_frame, variable=self.graininess_level, from_=0, to=100, orient=tk.HORIZONTAL, length=200).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(self.control_frame, text="Brightness Level:").grid(row=0, column=2, padx=5, pady=5)
        tk.Scale(self.control_frame, variable=self.brightness_level, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=200).grid(row=0, column=3, padx=5, pady=5)
        tk.Button(self.control_frame, text="Load Image", command=self.load_image).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.control_frame, text="Apply Graininess Effect", command=self.apply_graininess_effect).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.control_frame, text="Save Image", command=self.save_image).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(self.control_frame, text="Apply to All", command=self.apply_graininess_effect_to_all).grid(row=1, column=3, padx=5, pady=5)

        # image displays
        self.image_frame = tk.Frame(self.master)
        self.image_frame.pack(expand=True, fill="both")

        # Create a new frame inside the image frame
        self.image_display_frame = tk.Frame(self.image_frame)
        self.image_display_frame.pack(expand=True, fill="both")

        self.original_image_label = tk.Label(self.image_display_frame)
        self.original_image_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.modified_image_label = tk.Label(self.image_display_frame)
        self.modified_image_label.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # configure grid layout
        self.control_frame.grid_rowconfigure(2, weight=1)
        self.control_frame.grid_columnconfigure([0, 1, 2, 3], weight=1)
        self.image_frame.grid_rowconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(0, weight=1)

    def create_labels(self):
        # Create image labels
        self.before_label = tk.Label(self.image_display_frame, text="Before", font=('Helvetica', 14))
        self.before_label.grid(row=0, column=0, padx=5, pady=5, sticky="n")

        self.after_label = tk.Label(self.image_display_frame, text="After", font=('Helvetica', 14))
        self.after_label.grid(row=0, column=1, padx=5, pady=5, sticky="n")

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", ("*.jpg", "*.jpeg", "*.png"))])
        if path:
            self.image = Image.open(path).convert("L")  # Convert to grayscale
            self.modified_image = self.image.copy()
            self.display_images(self.image, self.image)
            self.graininess_level.set(50)
            self.brightness_level.set(1.0)
            self.create_labels()

    def apply_graininess_effect(self):
        if self.image:
            draw = ImageDraw.Draw(self.modified_image)
            width, height = self.image.size
            graininess_level = self.graininess_level.get()
            brightness_level = self.brightness_level.get()

            # Convert image to NumPy array
            image_array = np.array(self.image)

            # Downsample image by a quarter
            downsampled_image_array = image_array[::2, ::2]

            box_width = 400
            box_height = 350
            box_left = (width // 2 - box_width) // 2
            box_top = (height // 2 - box_height) // 2 - 50  # move higher
            box_right = box_left + box_width
            box_bottom = box_top + box_height

            for i in range(width // 2):
                for j in range(height // 2):
                    if box_left <= i < box_right and box_top <= j < box_bottom:
                        pixel_value = downsampled_image_array[j, i]
                        delta = int(pixel_value * graininess_level / 100)
                        new_pixel_value = random.randint(pixel_value - delta, pixel_value + delta)
                        new_pixel_value = max(0, min(255, new_pixel_value))
                        draw.point((i * 2, j * 2), new_pixel_value)
                        draw.point((i * 2 + 1, j * 2), new_pixel_value)
                        draw.point((i * 2, j * 2 + 1), new_pixel_value)
                        draw.point((i * 2 + 1, j * 2 + 1), new_pixel_value)

            # Adjust brightness of the modified image
            brightness = ImageEnhance.Brightness(self.modified_image)
            self.modified_image = brightness.enhance(brightness_level)

            self.display_images(self.image, self.modified_image)

    def apply_graininess_effect_to_all(self):
        # folder_path = filedialog.askdirectory()
        # save_path = filedialog.askdirectory()
        folder_path = r"C:\Users\Bing Kang\Desktop\KIDNEY DATASET\BK_Contrast\Test_HQ"
        save_path = r"C:\Users\Bing Kang\Desktop\KIDNEY DATASET\BK_Contrast\Test_LQ"
        graininess_level = self.graininess_level.get()
        brightness_level = self.brightness_level.get()

        if folder_path and save_path:
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            for filename in os.listdir(folder_path):
                if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
                    image_path = os.path.join(folder_path, filename)
                    image = Image.open(image_path).convert("L")
                    modified_image = image.copy()
                    draw = ImageDraw.Draw(modified_image)
                    width, height = image.size

                    # Downsample image by a quarter
                    downsampled_image = image.resize((width // 2, height // 2))

                    box_width = 400
                    box_height = 350
                    box_left = (width // 2 - box_width) // 2
                    box_top = (height // 2 - box_height) // 2 - 50  # move higher
                    box_right = box_left + box_width
                    box_bottom = box_top + box_height

                    downsampled_image_array = np.array(downsampled_image)

                    for i in range(width // 2):
                        for j in range(height // 2):
                            if box_left <= i < box_right and box_top <= j < box_bottom:
                                pixel_value = downsampled_image_array[j, i]
                                delta = int(pixel_value * graininess_level / 100)
                                new_pixel_value = random.randint(pixel_value - delta, pixel_value + delta)
                                new_pixel_value = max(0, min(255, new_pixel_value))
                                draw.point((i * 2, j * 2), new_pixel_value)
                                draw.point((i * 2 + 1, j * 2), new_pixel_value)
                                draw.point((i * 2, j * 2 + 1), new_pixel_value)
                                draw.point((i * 2 + 1, j * 2 + 1), new_pixel_value)

                    # Adjust brightness of the modified image
                    brightness = ImageEnhance.Brightness(modified_image)
                    modified_image = brightness.enhance(brightness_level)

                    save_filename = os.path.splitext(filename)[0] + "_Grainy.jpg"
                    save_filepath = os.path.join(save_path, save_filename)
                    modified_image.save(save_filepath)

            tk.messagebox.showinfo("Success", "Graininess effect applied to all images.")

    def save_image(self):
        if self.modified_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg")])
            if save_path:
                self.modified_image.save(save_path)
                tk.messagebox.showinfo("Success", "Image saved successfully.")

    def display_images(self, original, modified):
        original.thumbnail((400, 400))
        modified.thumbnail((400, 400))

        original_photo = ImageTk.PhotoImage(original)
        self.original_image_label.configure(image=original_photo)
        self.original_image_label.image = original_photo

        modified_photo = ImageTk.PhotoImage(modified)
        self.modified_image_label.configure(image=modified_photo)
        self.modified_image_label.image = modified_photo


if __name__ == "__main__":
    root = tk.Tk()
    app = GraininessEffectApp(root)
    root.mainloop()
