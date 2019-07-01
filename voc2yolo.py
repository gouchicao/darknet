import argparse
import os
import pickle
import xml.etree.ElementTree as ET

from os import listdir, getcwd
from os.path import join
from tqdm import tqdm


classes = []


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(voc_label_file, yolo_label_dir):
    with open(voc_label_file, "r") as in_file:
        xmlname = os.path.basename(voc_label_file)
        txtname = os.path.splitext(xmlname)[0]+'.txt'
        txtfile = os.path.join(yolo_label_dir, txtname)
        with open(txtfile, "w+") as out_file:
            tree=ET.parse(in_file)
            root = tree.getroot()
            size = root.find('size')
            w = int(size.find('width').text)
            h = int(size.find('height').text)
            out_file.truncate()
            for obj in root.iter('object'):
                difficult = obj.find('difficult').text
                cls = obj.find('name').text
                if cls not in classes or int(difficult)==1:
                    continue
                cls_id = classes.index(cls)
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
                bb = convert((w,h), b)
                out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--voc_label_dir', type=str, help='pascal voc format label directory.')
    parser.add_argument('-y', '--yolo_label_dir', type=str, help='save yolo format label directory.')
    parser.add_argument('-c', '--class_name_file', type=str, help='class name file.')
    
    args = parser.parse_args()

    if args.voc_label_dir:
        if not os.path.exists(args.yolo_label_dir):
            os.makedirs(args.yolo_label_dir)

    if args.class_name_file and os.path.exists(args.class_name_file):
        with open(args.class_name_file) as f:
            classes = f.read().splitlines()

    if args.voc_label_dir:
        voc_label_files = os.listdir(args.voc_label_dir)
        for voc_label_file in tqdm(voc_label_files):
            voc_label_file_path = os.path.join(args.voc_label_dir, voc_label_file)
            if '.xml' in voc_label_file or '.XML' in voc_label_file:
                convert_annotation(voc_label_file_path, args.yolo_label_dir)
            else:
                print('{} not xml file.'.format(voc_label_file_path))
