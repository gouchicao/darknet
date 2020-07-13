import os
import os.path
import random
import argparse


IMAGE_FILE_EXTNAMES = ('.jpg', '.jpeg', '.png')
LABEL_FILE_EXTNAMES = ('.txt')


def get_files_with_extnames(dir, extnames=()):
    files = []
    for file in os.listdir(dir):
        if not extnames:
            files.append(file)
        elif file.lower().endswith(extnames):
            files.append(file)

    return files


def filter_unlabeled_images(image_files, label_files):
    """
    通过标注文件反向推理可能存在的图像文件，查看图像文件是否存在。
    """
    files = []
    for label_file in label_files:
        filename, _ = os.path.splitext(label_file)
        
        may_exist_image_files = []
        for image_file_extname in IMAGE_FILE_EXTNAMES:
            may_exist_image_files.append((filename + image_file_extname).lower())

        for image_file in image_files:
            if image_file.lower() in may_exist_image_files:
                files.append(image_file)
                break

    return files


def WriteFilePath(file, file_content):
    print('Save image file path. Filename: %s' % file)
    with open(file, 'w') as f:
        for filename in file_content:
            filename = 'images/' + filename
            f.write(filename + '\n')
            print(filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--images_dir', type=str, default='project/images', help='images directory.')
    parser.add_argument('-l', '--labels_dir', type=str, default='project/labels', help='labels directory.')
    parser.add_argument('-r', '--split_radio', type=float, default=0.7, help='dataset split radio(train/valid).')
    parser.add_argument('-t', '--train_path_file', type=str, default='project/cfg/train.txt', help='save train image path file.')
    parser.add_argument('-v', '--valid_path_file', type=str, default='project/cfg/valid.txt', help='save valid image path file.')
    args = parser.parse_args()

    image_files = get_files_with_extnames(args.images_dir, IMAGE_FILE_EXTNAMES)
    label_files = get_files_with_extnames(args.labels_dir, LABEL_FILE_EXTNAMES)
    
    image_files = filter_unlabeled_images(image_files, label_files)

    random.shuffle(image_files)

    image_num = len(image_files)
    train_len = int(image_num * args.split_radio)

    train_image_files = image_files[:train_len]
    valid_image_files = image_files[train_len:]

    WriteFilePath(args.train_path_file, train_image_files)
    WriteFilePath(args.valid_path_file, valid_image_files)
