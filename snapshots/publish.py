import os
import shutil

from distutils.dir_util import copy_tree


def publish(src, dst):
    _clear(dst)
    copy_tree(src, dst)


def _clear(dst):
    for the_file in os.listdir(dst):
        file_path = os.path.join(folder, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
