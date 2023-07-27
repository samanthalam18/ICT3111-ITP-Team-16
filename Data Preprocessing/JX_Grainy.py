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


def combine_image_paths(*directories):
    combined_images = []
    for directory in directories:
        images = get_image_path(directory)
        combined_images.extend(images)

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
    print("Done moving", destination_dir)


def get_file_count(directory):
    return len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])


# def add_grainy_noise(source_dir, destination_dir):
#     copy_count = 0
#     for image in os.listdir(source_dir):
#         img_path = os.path.join(source_dir, image)
#         img = cv2.imread(img_path)
#
#         img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
#         # if 'Normal' in image:
#         #     mask = cv2.inRange(img_gray, 60, 255)
#         # elif 'Cyst' in image:
#         #     mask = cv2.inRange(img_gray, 20, 255)
#         # elif 'Stone' in image:
#         #     mask = cv2.inRange(img_gray, 20, 255)
#         # else:
#         #     mask = cv2.inRange(img_gray, 0, 255)
#
#         average_gray_level = img_gray.mean()
#
#         if average_gray_level > 60:
#             lower_threshold = 60
#         else:
#             lower_threshold = 20
#
#         # Create the mask based on the threshold
#         mask = cv2.inRange(img_gray, lower_threshold, 255)
#
#         noise = np.random.randint(0, 150, img_gray.shape, dtype=np.uint8)
#         noise_masked = cv2.bitwise_and(noise, mask)
#
#         grainy_image = cv2.add(img_gray, noise_masked)
#         grainy_image = cv2.cvtColor(grainy_image, cv2.COLOR_GRAY2BGR)
#
#         # Convert the gray areas of the image to white
#         grainy_image[np.where((grainy_image == [128]).all(axis=2))] = [255, 255, 255]
#
#         output_path = os.path.join(destination_dir, image)
#         cv2.imwrite(output_path, grainy_image)
#
#         copy_count += 1
#         print(copy_count, '/', len(os.listdir(source_dir)))
#
#     print("Done grainy", destination_dir)

def add_grainy_noise(source_dir, destination_dir):
    copy_count = 0
    for image in os.listdir(source_dir):
        img_path = os.path.join(source_dir, image)
        img = cv2.imread(img_path)

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        average_gray_level = np.mean(img_gray)

        if average_gray_level > 40:
            lower_threshold = 100
        else:
            lower_threshold = 20

        # Create the mask based on the threshold
        mask = cv2.inRange(img_gray, lower_threshold, 255)

        noise = np.random.randint(0, 150, img_gray.shape, dtype=np.uint8)
        noise_masked = cv2.bitwise_and(noise, mask)

        grainy_image = cv2.add(img_gray, noise_masked)

        # Convert the gray areas of the image to white
        grainy_image[np.where(grainy_image == 128)] = 255

        output_path = os.path.join(destination_dir, image)
        cv2.imwrite(output_path, grainy_image)

        copy_count += 1
        print(copy_count, '/', len(os.listdir(source_dir)))

    print("Done grainy", destination_dir)


def down_size_grainy(source_dir, destination_dir, width, height):
    for image in os.listdir(source_dir):
        img_path = os.path.join(source_dir, image)
        img = cv2.imread(img_path)

        # Reduce the image resolution
        width, height = img.shape[1], img.shape[0]
        resized_img = cv2.resize(img, (width // 4, height // 4), interpolation=cv2.INTER_LINEAR)

        output_path = os.path.join(destination_dir, image)
        cv2.imwrite(output_path, resized_img)

    print("Done downsize", destination_dir)


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

    print("Done low res", destination_dir)


def image_avg_height(source_dir):
    total_height = 0
    image_count = 0

    for image in os.listdir(source_dir):
        img_path = os.path.join(source_dir, image)
        if os.path.isfile(img_path):
            try:
                img = cv2.imread(img_path)
                if img is not None:
                    height = img.shape[0]
                    # print(img_path, height)
                    total_height += height
                    image_count += 1
            except Exception as e:
                print(f"Error image: {img_path}")
                print(f"Error message: {str(e)}")

    if image_count > 0:
        avg_height = total_height / image_count
        print("Average Height:", avg_height)
        return avg_height
    else:
        print("Error")
        return None


def filter_unwanted_images(source_dir, destination_dir, avg_height):
    for image in os.listdir(source_dir):
        img_path = os.path.join(source_dir, image)
        img = cv2.imread(img_path)

        if img is not None:
            height = img.shape[0]

            if height < avg_height:
                filename = os.path.basename(image)
                destination = os.path.join(destination_dir, filename)
                os.rename(img_path, destination)
            # else:
            #     print("Done")
        else:
            print(f"Error: {img_path}")

    print("Done", destination_dir)


def contrast_images(source_dir, destination_dir, contrast, brightness):
    for image in os.listdir(source_dir):
        img_path = os.path.join(source_dir, image)
        img = cv2.imread(img_path)

        adjusted_image = cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)

        output_path = os.path.join(destination_dir, 'contrast ' + image)
        cv2.imwrite(output_path, adjusted_image)

    print("Done contrast", destination_dir)


normal_dir = 'data/Normal'
cyst_dir = 'data/Cyst'
stone_dir = 'data/Stone'
combined_dir = 'data/NewCombined'
filtered_dir = 'data/Filtered'  # unwanted
processed_dir = 'data/Final_Filtered'

training_dir = 'data/Jiaxin/train_HR_Jiaxin'
testing_dir = 'data/Jiaxin/test_HR_Jiaxin'

train_G_dir = 'data/Jiaxin/train_G_Jiaxin'
test_G_dir = 'data/Jiaxin/test_G_Jiaxin'

train_LR_dir = 'data/Jiaxin/train_LR_Jiaxin'
test_LR_dir = 'data/Jiaxin/test_LR_Jiaxin'

train_G_contrast_dir = 'data/Jiaxin/train_G_contrast_dir'
test_G_contrast_dir = 'data/Jiaxin/test_G_contrast_dir'

for folder in [combined_dir, filtered_dir, processed_dir, training_dir, testing_dir, train_G_dir, test_G_dir,
               train_LR_dir, test_LR_dir, train_G_contrast_dir, test_G_contrast_dir]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# # To combine and count all the images, did not include the normal one
# print('Combining Images')
# dataset = function.combine_image_paths(cyst_dir, stone_dir)
# print(len(dataset))
#
# function.combine_image_dir(dataset, combined_dir)
# print("Combine Done")
#
# # To remove all the bone images
# print('Filtering Images')
# avg_height_all = function.image_avg_height(combined_dir)
# if avg_height_all is not None:
#     function.filter_unwanted_images(combined_dir, filtered_dir, avg_height_all)
#
# print('Second Filter')
# avg_height_final = function.image_avg_height(filtered_dir)
# if avg_height_final is not None:
#     function.filter_unwanted_images(filtered_dir, processed_dir, avg_height_final)
#
# # To randomly split and move images into training, testing set
# print('Splitting Images')
# training_set, testing_set = function.get_ratio(function.get_image_path(processed_dir), ratio=0.8)
#
# function.move_images(training_set, processed_dir, training_dir)
# function.move_images(testing_set, processed_dir, testing_dir)

# To count how many images in each
print(function.get_file_count(filtered_dir))
print(function.get_file_count(training_dir))
print(function.get_file_count(testing_dir))

# To add noise and downscale the images
print('Adding Grainy Effect')
function.add_grainy_noise(training_dir, train_G_dir)
function.add_grainy_noise(testing_dir, test_G_dir)
print('Adding Low Res Effect')
function.lower_resolution(test_G_dir, test_LR_dir, 0.5)
function.lower_resolution(train_G_dir, train_LR_dir, 0.5)

# To check if there is any missing images
print(function.get_file_count(training_dir), function.get_file_count(testing_dir))
print(function.get_file_count(train_G_dir), function.get_file_count(test_G_dir))
print(function.get_file_count(train_LR_dir), function.get_file_count(test_LR_dir))

# To remove all the bone images
print('Adding Contrast')
function.contrast_images(train_G_dir, train_G_contrast_dir, 1.4, 0)
function.contrast_images(test_G_dir, test_G_contrast_dir, 1.4, 0)
