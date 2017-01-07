"""Utilities"""

import shutil


class Copier:
    """Copy with preset source and destination path"""

    def __init__(self, source_path, destination_path):
        self.src_path = source_path
        self.dest_path = destination_path

    def copy(self, fname):
        """Copy file with preset source and destination path"""
        shutil.copyfile(self.src_path + '/' + fname,
                        self.dest_path + '/' + fname)

    def copytree(self, dirname):
        """Copy directory tree with preset source and destination path"""
        shutil.copytree(self.src_path + '/' + dirname,
                        self.dest_path + '/' + dirname)


def pathsanitycheck(path, figurepath, installpath, installimgpath):
    """Check absolute and realtive paths"""
    for thispath in [path, figurepath, installpath]:
        if thispath[0] != "/":
            raise Exception(
                "Config file contains realtive paths where absolute paths must be provided.")
    for thispath in [installimgpath]:
        if thispath[0] == "/":
            raise Exception(
                "Config file contains absolute paths where relative paths must be provided.")
