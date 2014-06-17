import os

project_path = ""
unused_pics = set()


def read_unused_styles(path):
    global unused_pics
    for line in open(path):
        line = line.strip()
        unused_pics.add(line)


def delete_pics():
    size = 0
    for filename in unused_pics:
        # path = project_path + os.sep + filename
        print filename
        size = size + os.path.getsize(filename)
        os.remove(filename)
    print "delete drawables size=" + str(size / 1024) + "K"


# read project path
def read_project_path(path):
    global project_path
    for line in open(path):
        line = line.strip()
        project_path = line


read_project_path("project_path.txt")
out_path = os.path.join("outputs", "unused_drawables.txt")
read_unused_styles(out_path)
delete_pics()