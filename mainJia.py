import os
import functionJia

normal_dir = 'data/Normal'
cyst_dir = 'data/Cyst'
combined_dir = 'data/Combined'
training_dir = 'data/jiaxin/train_HR_Jiaxin'
testing_dir = 'data/jiaxin/test_HR_Jiaxin'
train_G_dir = 'data/jiaxin/train_G_Jiaxin'
test_G_dir = 'data/jiaxin/test_G_Jiaxin'
train_LR_dir = 'data/jiaxin/train_LR_Jiaxin'
test_LR_dir = 'data/jiaxin/test_LR_Jiaxin'

for folder in [combined_dir, training_dir, testing_dir, train_G_dir, test_G_dir, train_LR_dir, test_LR_dir]:
    if not os.path.exists(folder):
        os.makedirs(folder)

dataset = functionJia.combine_image_paths(normal_dir, cyst_dir)
print(len(dataset))

# function.combine_image_dir(dataset, combined_dir)
# print("Combine Done")
#
# training_set, testing_set = function.get_ratio(dataset, ratio=0.8)
#
# function.move_images(training_set, combined_dir, training_dir)
# function.move_images(testing_set, combined_dir, testing_dir)

print(functionJia.get_file_count(normal_dir))
print(functionJia.get_file_count(cyst_dir))
print(functionJia.get_file_count(combined_dir))
print(functionJia.get_file_count(training_dir))
print(functionJia.get_file_count(testing_dir))

functionJia.add_grainy_noise(training_dir, train_G_dir)
functionJia.add_grainy_noise(testing_dir, test_G_dir)
functionJia.lower_resolution(test_G_dir, test_LR_dir, 0.5)
functionJia.lower_resolution(train_G_dir, train_LR_dir, 0.5)

print(functionJia.get_file_count(training_dir), functionJia.get_file_count(testing_dir))
print(functionJia.get_file_count(train_G_dir), functionJia.get_file_count(test_G_dir))
print(functionJia.get_file_count(train_LR_dir), functionJia.get_file_count(test_LR_dir))
