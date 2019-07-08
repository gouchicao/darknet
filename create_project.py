import os
import sys
# import os.path
import shutil
import random


class Project(object):
    """目录结构
    创建前：
        project/
        ├── cfg
        │   └── voc.names
        ├── images
        │   ├── ...
        │   └── ...
        ├── labels
        │   ├── ...
        │   └── ...
        └── test
            ├── ...
            └── ...

    创建后：
        project/
        ├── backup
        ├── cfg
        │   ├── train.txt
        │   ├── valid.txt
        │   ├── voc.data
        │   ├── voc.names
        │   └── yolov3.cfg
        ├── images
        │   ├── ...
        │   └── ...
        ├── labels
        │   ├── ...
        │   └── ...
        ├── predict
        └── test
            ├── ...
            └── ...
    """

    def __init__(self, project_dir='project'):
        self.project_dir = project_dir
        self.dataset_images_dir = os.path.join(project_dir, 'images')
        self.dataset_labels_dir = os.path.join(project_dir, 'labels')
        self.model_config_dir = os.path.join(project_dir, 'cfg')
        self.model_data_labels_dir = os.path.join(project_dir, 'data/labels')
        self.model_test_dir = os.path.join(project_dir, 'test')
        self.model_predict_dir = os.path.join(project_dir, 'predict')
        self.model_backup_dir = os.path.join(project_dir, 'backup')

        self.model_config_train_file = os.path.join(self.model_config_dir, 'train.txt')
        self.model_config_valid_file = os.path.join(self.model_config_dir, 'valid.txt')
        self.model_config_data_file = os.path.join(self.model_config_dir, 'voc.data')
        self.model_config_name_file = os.path.join(self.model_config_dir, 'voc.names')
        self.model_config_network_file = os.path.join(self.model_config_dir, 'yolov3.cfg')

        self.dataset_split_radio = 0.2


    def create(self):
        self._copy_model_data_labels()
        self._create_model_config_files()
        self._create_model_predict_directory()
        self._create_model_backup_directory()

    def _copy_model_data_labels(self):
        """拷贝data/labels到project/data/labels
        """
        data_dir = os.path.split(self.model_data_labels_dir)[0]
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        if not os.path.exists(self.model_data_labels_dir):
            shutil.copytree('data/labels', self.model_data_labels_dir)

    def _create_model_config_files(self):
        """依次按顺序创建
            cfg
            ├── voc.names
            ├── voc.data
            ├── yolov3.cfg
            ├── train.txt
            └── valid.txt
        """
        if not os.path.exists(self.model_config_dir):
            os.makedirs(self.model_config_dir)
        
        class_num = self._get_model_class_num()
        self._create_model_config_data_file(class_num)

        self._copy_model_config_network_file()

        image_files = self._get_dataset_images()
        random.shuffle(image_files)

        train_len = int(len(image_files) * (1-self.dataset_split_radio))

        train_image_files = image_files[:train_len]
        valid_image_files = image_files[train_len:]

        self._create_model_config_train_file(train_image_files)
        self._create_model_config_valid_file(valid_image_files)

    def _get_model_class_num(self):
        self._assert_file_exists(self.model_config_name_file)

        with open(self.model_config_name_file) as f:
            lines = f.read().splitlines()

        # 移除无效的class name
        class_num = 0
        for class_name in lines:
            if len(class_name.strip()) > 0:
                class_num += 1

        return class_num

    def _assert_file_exists(self, file_path):
        if not os.path.exists(file_path):
            print('file: {} not exist.'.format(file_path))
            sys.exit()

    def _create_model_config_data_file(self, class_num):
        """
        classes= 1
        train  = cfg/train.txt
        valid  = cfg/valid.txt
        names = cfg/voc.names
        backup = backup
        """
        if not os.path.exists(self.model_config_data_file):
            with open(self.model_config_data_file, 'w+') as f:
                f.write('classes = {}\n'.format(class_num))
                f.write('train  = cfg/train.txt\n')
                f.write('valid  = cfg/valid.txt\n')
                f.write('names = cfg/voc.names\n')
                f.write('backup = backup\n')


    def _copy_model_config_network_file(self):
        if not os.path.exists(self.model_config_network_file):
            shutil.copy('cfg/yolov3.cfg', self.model_config_network_file)

    def _get_dataset_images(self):
        self._assert_file_exists(self.dataset_images_dir)
        self._assert_file_exists(self.dataset_labels_dir)

        image_exts = ('jpg', 'png', 'jpeg', 'bmp', 'tif')

        parent_dir = os.path.basename(self.dataset_images_dir)
        image_files = []
        for filepath in os.listdir(self.dataset_images_dir):
            if filepath.lower().endswith(image_exts):
                image_files.append(os.path.join(parent_dir, filepath))
        
        return image_files

    def _create_model_config_train_file(self, image_files):
        self._write(self.model_config_train_file, image_files)

    def _create_model_config_valid_file(self, image_files):
        self._write(self.model_config_valid_file, image_files)

    def _write(self, file_path, lines):
        with open(file_path, 'w') as f:
            for line in lines:
                f.write(line + '\n')
        

    def _create_model_predict_directory(self):
        if not os.path.exists(self.model_predict_dir):
            os.makedirs(self.model_predict_dir)

    def _create_model_backup_directory(self):
        if not os.path.exists(self.model_backup_dir):
            os.makedirs(self.model_backup_dir)

if __name__ == "__main__":
    project = Project()
    project.create()
