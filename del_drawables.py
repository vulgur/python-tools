import os

project_path = ""
unused_pics = set()


def read_unused_styles(path):
    global unused_pics
    for line in open(path):
        line = line.strip()
        if not line == '':
            unused_pics.add(line)


def delete_pics():
    global unused_pics
    size = 0
    if len(unused_pics) == 0:
        print 'no drawables to be deleted'
    else:
        for filename in unused_pics:
            # path = project_path + os.sep + filename
            # print filename
            size += os.path.getsize(filename)
            os.remove(filename)
        print "deleted drawables size=" + str(size / 1024) + "K"
    return size, unused_pics


