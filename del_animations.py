import os

project_path = ""
unused_animations = set()


def read_unused_animations(path):
    global unused_animations
    for line in open(path):
        line = line.strip()
        unused_animations.add(line)


def delete_animations():
    global unused_animations
    size = 0
    for filename in unused_animations:
        filename = filename.strip()
        # print filename
        size = size + os.path.getsize(filename)
        os.remove(filename)

    print "delete animations size=" + str(size / 1024) + "K"
    return size

