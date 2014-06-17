import os
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


size = 0
project_path = get_project_path("project_path.txt")
res_folder = os.path.join(project_path, "res")

layout_out_path = os.path.join("outputs", "unused_layouts.txt")
del_layouts.read_unused_layouts(layout_out_path)
size += del_layouts.delete_layouts()

style_out_path = os.path.join("outputs", "unused_styles.txt")
del_styles.read_unused_styles(style_out_path)
size += del_styles.delete_xml_styles(res_folder)

animation_out_path = os.path.join("outputs", "unused_animations.txt")
del_animations.read_unused_animations(animation_out_path)
size += del_animations.delete_animations()

drawable_out_path = os.path.join("outputs", "unused_drawables.txt")
del_drawables.read_unused_styles(drawable_out_path)
size += del_drawables.delete_pics()

string_out_path = os.path.join("outputs", "unused_strings.txt")
del_strings.read_unused_strings(string_out_path)
size += del_strings.delete_xml_strings(res_folder)

dat_file = os.path.join(project_path, "assets", "kfmt.dat")
dat_out_path = os.path.join("outputs", "unused_tables.txt")
del_dat.read_unused_tables(dat_out_path)
size += del_dat.delete_tables(dat_file)

print "total cleanup size=" + str(size / 1024) + "K"