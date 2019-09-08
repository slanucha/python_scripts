import os
import glob
import cv2
import xml.etree.ElementTree as ET


def get_path_filename_and_ext(filepath):
    path, filename = os.path.split(filepath)
    filename, ext = os.path.splitext(filename)
    return path, filename, ext


def add_suffix(filepath, suffix):
    """Function adding suffix to the given filepath"""
    path, filename, ext = get_path_filename_and_ext(filepath)
    new_filename = filename + suffix + ext
    new_path = os.path.join(path, new_filename)
    return new_path


def flip_XML(path, filename, suffix):
    """
    For given path, filename and suffix, a new xml file is created.
    Each x coordinate is transformed usinf this formula: x = width - x.
    Filename and path are also updated
    """
    tree = ET.parse(os.path.join(path, filename) + '.xml')
    root = tree.getroot()
    tag_filename = root.find('filename')
    tag_path = root.find('path')

    tag_filename.text = filename + suffix + '.jpg'
    tag_path.text = add_suffix(tag_path.text, suffix)

    width = int(root.find('size').find('width').text)

    for xmin in root.iter('xmin'):
        xmin.text = str(width - int(xmin.text))

    for xmax in root.iter('xmax'):
        xmax.text = str(width - int(xmax.text))

    tree.write(os.path.join(path, filename) + suffix + '.xml')


def flip_IMG(path, filename, ext, suffix):
    image = cv2.imread(os.path.join(path, filename) + ext)
    image = cv2.flip(image, 1)
    cv2.imwrite(os.path.join(path, filename) + suffix + ext, image)


if __name__ == '__main__':
    path = './'
    suffix = '_flipped'
    for f in glob.glob(path + '*.jpg'):
        path, filename, ext = get_path_filename_and_ext(f)
        flip_IMG(path, filename, ext, suffix)
        flip_XML(path, filename, suffix)
