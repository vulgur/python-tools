import os

project_path = ""
unused_layouts = set()


def read_unused_layouts(path):
    global unused_layouts
    for line in open(path):
        line = line.strip()
        if not line == '':
            unused_layouts.add(line)


def delete_layouts():
    global unused_layouts
    size = 0
    if len(unused_layouts) == 0:
        print 'no layouts to be deleted'
    else:
        for filename in unused_layouts:
            filename = filename.strip()
            # print filename
            size = size + os.path.getsize(filename)
            os.remove(filename)

        print "deleted layouts size=" + str(size / 1024) + "K"
    return size, unused_layouts


