# To install openCv: pip install opencv-python
import cv2
import os
import numpy as np

input_data = 'data/highQualityData'
grainy_data = 'data/grainy/jiaxin'
# preprocessed_data = 'data/preprocessed_data'

for folder in [input_data, grainy_data]:
    if not os.path.exists(folder):
        os.makedirs(folder)

for image in os.listdir(input_data):

    img_path = os.path.join(input_data, image)
    img = cv2.imread(img_path)

    # Convert the image to grayscale
    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Binary mask for gray areas
    mask = cv2.inRange(img, 20, 150)

    # Random noise
    noise = np.random.randint(0, 150, img.shape, dtype=np.uint8)

    # Apply mask to restrict noise addition to gray areas
    noise_masked = cv2.bitwise_and(noise, mask)

    # Add noise
    grainy_image = cv2.add(img, noise_masked)

    grainy_image = cv2.cvtColor(grainy_image, cv2.COLOR_GRAY2BGR)

    output_path = os.path.join(grainy_data, image)
    cv2.imwrite(output_path, grainy_image)

print("Done")

