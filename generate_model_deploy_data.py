import argparse
import os
import shutil

import pickle
import xml.etree.ElementTree as ET

from os import listdir, getcwd
from os.path import join
from tqdm import tqdm


MODEL_CONFIG_FILE = 'cfg/voc.data'
MODEL_CLASS_NAME_FILE = 'cfg/voc.names'
MODEL_NETWORK_FILE = 'cfg/yolov3.cfg'
MODEL_WEIGHT_FILE = 'backup/yolov3_final.weights'

MODEL_DEPLOY_DATA_DIR = 'model'


def generate_model_deploy_data(project_dir):
    model_deploy_data_dir = os.path.join(project_dir, MODEL_DEPLOY_DATA_DIR)

    if os.path.exists(model_deploy_data_dir):
        shutil.rmtree(model_deploy_data_dir)
    os.mkdir(model_deploy_data_dir)

    model_config_file = os.path.join(project_dir, MODEL_CONFIG_FILE)
    model_class_name_file = os.path.join(project_dir, MODEL_CLASS_NAME_FILE)
    model_network_file = os.path.join(project_dir, MODEL_NETWORK_FILE)
    model_weight_file = os.path.join(project_dir, MODEL_WEIGHT_FILE)

    copyfile(model_weight_file, model_deploy_data_dir)
    copyfile(model_network_file, model_deploy_data_dir)
    copyfile(model_class_name_file, model_deploy_data_dir)

    class_num = get_class_num(model_config_file)
    model_deploy_config_file = os.path.join(model_deploy_data_dir, os.path.basename(model_config_file))
    with open(model_deploy_config_file, 'w+') as f:
        f.write('classes = {}\n'.format(class_num))
        f.write('names = {}/{}\n'.format(MODEL_DEPLOY_DATA_DIR, os.path.basename(MODEL_CLASS_NAME_FILE)))
    

def copyfile(src_file, dst_dir):
    if not os.path.exists(src_file):
        print('{} file not exist.'.format(src_file))
        return

    shutil.copyfile(src_file, os.path.join(dst_dir, os.path.basename(src_file)))


def get_class_num(model_config_file):
    lines = []
    with open(model_config_file) as f:
        lines = f.read().splitlines()

    classes_key = 'classes'
    for line in lines:
        if classes_key in line:
            return int(line.split('=')[-1])

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--project_dir', type=str, help='project directory.')
    
    args = parser.parse_args()

    project_dir = args.project_dir
    if not project_dir:
        project_dir = os.getcwd()

    generate_model_deploy_data(project_dir)
