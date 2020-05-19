import os
import sys

from os.path import join as join


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    return join(join(join(get_path(), "static"), "res"), relative_path)


def config_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    return join(join("static", "config"), relative_path)


def get_path():
    base_path = getattr(sys, '_MEIPASS',
                        get_this_file_path())
    return base_path


def get_this_file_path():
    return os.path.dirname(os.path.split(os.path.abspath(__file__))[0])
