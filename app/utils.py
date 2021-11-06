from random import choice
from os import listdir
from os.path import isfile, join


def random_choice_image(path):
    file_list = []
    pi = path.find("img")

    for file in listdir(path):
        if isfile(join(path, file)):
            file_list.append(file)
    return f"{path[pi:]}/{choice(file_list)}"