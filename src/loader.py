import pygame
from pygame.locals import *
import os
import sys


def load_image(filename, colorkey=None):
    current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))  # スクリプトのディレクトリ
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))  # スクリプトの親ディレクトリ
    """画像をロードして画像と矩形を返す"""
    filename = os.path.join("img", filename)
    filename = os.path.join(parent_dir, filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        print ("Cannot load image:", filename)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(filename):
    current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))  # スクリプトのディレクトリ
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))  # スクリプトの親ディレクトリ
    filename = os.path.join("sound", filename)
    filename = os.path.join(parent_dir, filename)
    return pygame.mixer.Sound(filename)

def play_sound(filename, repeat=None):
    current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))  # スクリプトのディレクトリ
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))  # スクリプトの親ディレクトリ
    filename = os.path.join("sound", filename)
    filename = os.path.join(parent_dir, filename)
    pygame.mixer.music.load(filename)
    if repeat is not None:
        if repeat is -1:
            pygame.mixer.music.play(-1)

def load_font(fontname, size):
    current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))  # スクリプトのディレクトリ
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))  # スクリプトの親ディレクトリ
    fontname = os.path.join("font", fontname)
    fontname = os.path.join(parent_dir, fontname)
    return pygame.font.Font(fontname, size)
