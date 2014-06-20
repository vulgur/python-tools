import os
import time
import del_animations
import del_drawables
import del_layouts
import del_strings
import del_styles
import del_dat


# read project path
def get_project_path(path):
    global project_path
    for line in open(path):
        line = line.strip()
        return line


def add_to_list(s, l):
    sorted_list = list(s)
    sorted_list.sort()
    for e in sorted_list:
        l.append(e)


def write_to_log(filename, logs):
    if os.path.isdir(output_folder):
        pass
    else:
        os.mkdir(output_folder)
    filename = output_folder + os.sep + filename
    output = open(filename, 'w')
    for x in logs:
        output.write(x + '\n')
    output.close()


size = 0
total_size = 0
deleted = set()
total_deleted = []
project_path = get_project_path("project_path.txt")
res_folder = os.path.join(project_path, "res")
output_folder = "outputs"

layout_out_path = os.path.join("outputs", "unused_layouts.txt")
del_layouts.read_unused_layouts(layout_out_path)
(size, deleted) = del_layouts.delete_layouts()
total_size += size
total_deleted.append('--------------- layouts ' + str(total_size / 1024) + "K")
add_to_list(deleted, total_deleted)

style_out_path = os.path.join("outputs", "unused_styles.txt")
del_styles.read_unused_styles(style_out_path)
(size, deleted) = del_styles.delete_xml_styles(res_folder)
total_size += size
total_deleted.append('--------------- styles ' + str(total_size / 1024) + "K")
add_to_list(deleted, total_deleted)

animation_out_path = os.path.join("outputs", "unused_animations.txt")
del_animations.read_unused_animations(animation_out_path)
(size, deleted) = del_animations.delete_animations()
total_size += size
total_deleted.append('--------------- animations ' + str(total_size / 1024) + "K")
add_to_list(deleted, total_deleted)

drawable_out_path = os.path.join("outputs", "unused_drawables.txt")
del_drawables.read_unused_styles(drawable_out_path)
(size, deleted) = del_drawables.delete_pics()
total_size += size
total_deleted.append('--------------- drawables ' + str(total_size / 1024) + "K")
add_to_list(deleted, total_deleted)

string_out_path = os.path.join("outputs", "unused_strings.txt")
del_strings.read_unused_strings(string_out_path)
(size, deleted) = del_strings.delete_xml_strings(res_folder)
total_size += size
total_deleted.append('--------------- strings ' + str(total_size / 1024) + "K")
add_to_list(deleted, total_deleted)

dat_file = os.path.join(project_path, "assets", "kfmt.dat")
dat_out_path = os.path.join("outputs", "unused_tables.txt")
del_dat.read_unused_tables(dat_out_path)
(size, deleted) = del_dat.delete_tables(dat_file)
total_size += size
total_deleted.append('--------------- tables ' + str(total_size / 1024) + "K")
add_to_list(deleted, total_deleted)

print "total cleanup size=" + str(total_size / 1024) + "K"
total_deleted.append('---------------')
total_deleted.append("total cleanup size=" + str(total_size / 1024) + "K")

cleanup_filename = "cleanup" + time.strftime("%Y-%m-%d-%H%M%S", time.localtime())
write_to_log(cleanup_filename, total_deleted)