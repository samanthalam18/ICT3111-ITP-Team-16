import cv2
import os
import numpy as np
import shutil
import random


def get_image_path(directory):
    images = []
    for image in os.listdir(directory):
        file_path = os.path.join(directory, image)
        if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
            images.append(file_path)
    return images


def combine_image_paths(dir1, dir2):
    images1 = get_image_path(dir1)
    images2 = get_image_path(dir2)
    combined_images = images1 + images2

    return combined_images


def combine_image_dir(data, directory):
    copy_count = 0
    for combined_images in data:
        filename = os.path.basename(combined_images)
        destination = os.path.join(directory, filename)
        shutil.copy(combined_images, destination)
        copy_count += 1
        print(copy_count)


def get_ratio(data, ratio):
    unique_data = list(set(data))
    random.shuffle(unique_data)
    split_point = int(ratio * len(unique_data))
    training = unique_data[:split_point]
    testing = unique_data[split_point:]

    return training, testing


def move_images(ratio_set, source_dir, destination_dir):
    copy_count = 0
    for image in ratio_set:
        filename = os.path.basename(image)
        destination = os.path.join(destination_dir, filename)
        shutil.copy(os.path.join(source_dir, filename), destination)
        copy_count += 1
        print(copy_count, '/', len(ratio_set))
    print("Done", destination_dir)


def get_file_count(directory):
    return len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])


def add_grainy_noise(source_dir, destination_dir):
    copy_count = 0
    for image in os.listdir(source_dir):
        img_path = os.path.join(source_dir, image)
        img = cv2.imread(img_path)

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if 'Normal' in image:
            mask = cv2.inRange(img_gray, 60, 255)
        elif 'Cyst' in image:
            mask = cv2.inRange(img_gray, 20, 255)
        else:
            mask = cv2.inRange(img_gray, 0, 255)

        noise = np.random.randint(0, 150, img_gray.shape, dtype=np.uint8)
        noise_masked = cv2.bitwise_and(noise, mask)

        grainy_image = cv2.add(img_gray, noise_masked)
        grainy_image = cv2.cvtColor(grainy_image, cv2.COLOR_GRAY2BGR)

        # Convert the gray areas of the image to white
        grainy_image[np.where((grainy_image == [128]).all(axis=2))] = [255, 255, 255]

        output_path = os.path.join(destination_dir, image)
        cv2.imwrite(output_path, grainy_image)

        copy_count += 1
        print(copy_count, '/', len(os.listdir(source_dir)))

    print("Done", destination_dir)


def down_size_grainy(source_dir, destination_dir, width, height):
    for image in os.listdir(source_dir):
        img_path = os.path.join(source_dir, image)
        img = cv2.imread(img_path)

        # Reduce the image resolution
        width, height = img.shape[1], img.shape[0]
        resized_img = cv2.resize(img, (width // 4, height // 4), interpolation=cv2.INTER_LINEAR)

        output_path = os.path.join(destination_dir, image)
        cv2.imwrite(output_path, resized_img)

    print("Done", destination_dir)


def down_sample_image(img, scale_factor):
    width = int(img.shape[1] * scale_factor)
    height = int(img.shape[0] * scale_factor)
    dim = (width, height)
    resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized_img


def lower_resolution(source_dir, destination_dir, scale_factor):
    copy_count = 0
    for image in os.listdir(source_dir):
        img_path = os.path.join(source_dir, image)
        img = cv2.imread(img_path)

        downscaled_img = down_sample_image(img, scale_factor)

        output_path = os.path.join(destination_dir, image)
        cv2.imwrite(output_path, downscaled_img)

        copy_count += 1
        print(copy_count, '/', len(os.listdir(source_dir)))

    print("Done", destination_dir)


