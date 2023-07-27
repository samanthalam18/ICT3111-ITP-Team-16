import cv2
import numpy as np
import os
from sklearn.model_selection import train_test_split
import shutil


def add_grainy_effect(input_dir, noised_dir):
    # Create the Grainy Cyst directories if they don't exist
    os.makedirs(noised_dir, exist_ok=True)

    # Loop through all the image files in the directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.jpg'):  # Check if the file is a JPEG image
            # Load the image
            img = cv2.imread(os.path.join(input_dir, filename))

            # Convert the image to grayscale
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Generate random Gaussian noise
            mean = 0
            stddev = 80  # Adjust the noise intensity as desired
            noise = np.zeros(gray_img.shape, np.uint8)
            cv2.randn(noise, mean, stddev)

            # Threshold the grayscale image to obtain a binary mask
            _, threshold_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY)

            # Apply the binary mask to the noise image
            noisy_lines = cv2.bitwise_and(noise, threshold_img)

            # Add the noisy lines to the original image
            noisy_img = cv2.add(gray_img, noisy_lines)

            # Apply histogram equalization to the grayscale image
            equalized_img = cv2.equalizeHist(noisy_img)

            # Apply a threshold to darken the bright regions while preserving the black regions
            _, thresholded_img = cv2.threshold(equalized_img, 200, 200, cv2.THRESH_TRUNC)

            # Convert the thresholded image back to BGR
            thresholded_img = cv2.cvtColor(thresholded_img, cv2.COLOR_GRAY2BGR)

            # Save the Grainy Cyst images into the output folder
            output_filename = os.path.splitext(filename)[0] + '_With_Grain.jpg'
            output_path = os.path.join(noised_dir, output_filename)
            cv2.imwrite(output_path, thresholded_img)

    print("Grainy Effect on Cyst Images Done")


def combine_folders(source_dirs, destination_dir):
    # Create the destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)

    for source_dir in source_dirs:
        # Move files from the source directory to the destination directory
        for filename in os.listdir(source_dir):
            src_path = os.path.join(source_dir, filename)
            dst_path = os.path.join(destination_dir, filename)
            shutil.move(src_path, dst_path)

    # Delete the source directories and their contents here
    for source_dir in source_dirs:
        try:
            shutil.rmtree(source_dir)
            print(f"Deleted {source_dir}")
        except OSError as e:
            print(f"Failed to remove {source_dir}. The directory is not empty.")
            print(f"Error message: {e}")

    print("Combine Grainy Cyst and Normal Images into 1 Folder Done")


def split_and_move_images(input_dir, training_dir, testing_dir):
    # Create the Training and Testing directories if they don't exist
    os.makedirs(training_dir, exist_ok=True)
    os.makedirs(testing_dir, exist_ok=True)

    # Get the list of image filenames in the directory
    image_files = [filename for filename in os.listdir(input_dir) if filename.endswith('.jpg')]

    # Split the images into training (80%) and testing (20%) sets
    train_files, test_files = train_test_split(image_files, test_size=0.2, random_state=42)

    # Move the training images to the training directory
    for filename in train_files:
        src_path = os.path.join(input_dir, filename)
        dst_path = os.path.join(training_dir, filename)
        shutil.copyfile(src_path, dst_path)

    print("High Res Training Folder Done")

    # Move the testing images to the testing directory
    for filename in test_files:
        src_path = os.path.join(input_dir, filename)
        dst_path = os.path.join(testing_dir, filename)
        shutil.copyfile(src_path, dst_path)

    print("High Res Testing Folder Done")


def downsample_images(input_dir, output_dir, scale_factor=0.25, resampling_method=cv2.INTER_LINEAR):
    # Create the Downsampled directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over the image files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.jpg'):  # Check if the file is a JPEG image
            # Load the image
            img = cv2.imread(os.path.join(input_dir, filename))

            # Get the original width and height
            height, width = img.shape[:2]

            # Calculate the new width and height for downsampling
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)

            # Resize the image to the new dimensions using the specified resampling method
            downsampled_img = cv2.resize(img, (new_width, new_height), interpolation=resampling_method)

            # Save the downsampled image in the output directory
            output_path = os.path.join(output_dir, filename)
            cv2.imwrite(output_path, downsampled_img)

    if 'train' in output_dir.lower():
        print("Low Res Training Folder Done")
    elif 'test' in output_dir.lower():
        print("Low Res Testing Folder Done")


if __name__ == "__main__":
    # Set the directory where the Original Cyst images are located at
    cyst_dir = 'C:/Users/saman/Downloads/Cyst/'
    # Create a new directory to save the Grainy Cyst images
    grainy_dir = 'C:/Users/saman/Downloads/Grainy Cyst/'
    add_grainy_effect(cyst_dir, grainy_dir)

    # Set the directories where the Grainy Cyst and Normal folders are located at
    grainy_cyst_dir = 'C:/Users/saman/Downloads/Grainy Cyst/'
    normal_dir = 'C:/Users/saman/Downloads/Normal/'
    # Create a new directory to combine both folders
    combined_dir = 'C:/Users/saman/Downloads/CT Scans/'
    combine_folders([grainy_cyst_dir, normal_dir], combined_dir)

    # Set the directory where the Normal and Cyst images are located at
    img_dir = 'C:/Users/saman/Downloads/CT Scans'
    # Set the directory for the High Resolution Training and Testing images
    train_dir = 'C:/Users/saman/Downloads/train_HR'
    test_dir = 'C:/Users/saman/Downloads/test_HR'
    split_and_move_images(img_dir, train_dir, test_dir)

    # Set the directory where the High Resolution Training and Testing images are located at
    trainHR_dir = 'C:/Users/saman/Downloads/train_HR'
    testHR_dir = 'C:/Users/saman/Downloads/test_HR'
    # Set the directory for the Downsampled images
    downsampled_train_dir = 'C:/Users/saman/Downloads/train_LR_Samantha'
    downsampled_test_dir = 'C:/Users/saman/Downloads/test_LR_Samantha'
    downsample_images(trainHR_dir, downsampled_train_dir)
    downsample_images(testHR_dir, downsampled_test_dir)
