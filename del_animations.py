import os

project_path = ""
unused_animations = set()


def read_unused_animations(path):
    global unused_animations
    for line in open(path):
        line = line.strip()
        if not line == '':
            unused_animations.add(line)


def delete_animations():
    global unused_animations
    size = 0
    if len(unused_animations) == 0:
        print 'no animations to be deleted'
    else:
        for filename in unused_animations:
            filename = filename.strip()
            # print filename
            size = size + os.path.getsize(filename)
            os.remove(filename)
        print "deleted animations size=" + str(size / 1024) + "K"
    return size, unused_animations

