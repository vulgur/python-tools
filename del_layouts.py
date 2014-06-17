import os

project_path = ""
unused_layouts = set()


def read_unused_layouts(path):
    global unused_layouts
    for line in open(path):
        line = line.strip()
        unused_layouts.add(line)


def delete_layouts():
    size = 0
    for filename in unused_layouts:
        filename = filename.strip()
        print filename
        size = size + os.path.getsize(filename)
        os.remove(filename)

    print "delete layouts size=" + str(size / 1024) + "K"


# read project path
def read_project_path(path):
    global project_path
    for line in open(path):
        line = line.strip()
        project_path = line


read_project_path("project_path.txt")
out_path = os.path.join("outputs", "unused_layouts.txt")
read_unused_layouts(out_path)
delete_layouts()