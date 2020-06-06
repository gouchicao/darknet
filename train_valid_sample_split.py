import os
import os.path
import random


image_file_extnames = ('.jpg', '.jpeg', '.png')
label_file_extname = '.txt'

image_files = []
label_files = []

root_path = 'model-zoo/platen-switch/'
images_dir = 'model-zoo/platen-switch/images'
labels_dir = 'model-zoo/platen-switch/labels'

for filepath in os.listdir(images_dir):
    if filepath.lower().endswith(image_file_extnames):
        image_files.append(filepath)
        
for filepath in os.listdir(labels_dir):
    if filepath.lower().endswith(label_file_extname):
        label_files.append(filepath)

image_files_with_label = []
for label_file in label_files:
    filename, extname = os.path.splitext(label_file)
    
    may_exist_image_files = []
    for image_file_extname in image_file_extnames:
        may_exist_image_files.append((filename + image_file_extname).lower())

    for image_file in image_files:
        if image_file.lower() in may_exist_image_files:
            image_files_with_label.append(image_file)
            break

random.shuffle(image_files_with_label)

len = len(image_files_with_label)
split_radio = 0.2
train_len = int(len * (1-split_radio))

train_image_files = image_files_with_label[:train_len]
valid_image_files = image_files_with_label[train_len:]

train_txt_path = os.path.join(root_path, 'cfg/train.txt')
valid_txt_path = os.path.join(root_path, 'cfg/valid.txt')
print(train_txt_path)
print(valid_txt_path)

print('train image files\n')
with open(train_txt_path, 'w') as f:
    for filename in train_image_files:
        filename = 'images/' + filename
        f.write(filename + '\n')
        print(filename)

print('\n\n')

print('valid image files\n')
with open(valid_txt_path, 'w') as f:
    for filename in valid_image_files:
        filename = 'images/' + filename
        f.write(filename + '\n')
        print(filename)
