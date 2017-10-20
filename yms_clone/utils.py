import os


def thumb_gen(filename):
    base, ext = os.path.splitext(filename)
    return os.path.join(base + '_thumb' + ext)
