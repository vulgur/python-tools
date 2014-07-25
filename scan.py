import os
import re

# ----- global containers
java_activities = set()
xml_activities = set()
base_activities = set(['Activity', 'FragmentActivity'])
child_activities = set()
others = set()

used_layouts = set()
unused_layouts = set()
all_drawables_dict = {}
all_drawables = set()
used_drawables = set()
used_strings = set()
used_styles = set()
xml_styles = set()
kmob_layouts = set()
kmob_drawables = set()
kmob_strings = set()

all_ids = set()

layout_objs = set()

used_animations = set()

used_tables = set()
all_tables = set()
cm_reports = set()
exclusions = set()

drawable_dict = {}
layout_dict = {}
style_dict = {}
string_dict = {}
animation_dict = {}
# ----- kmob
isKmob = False

output_folder = 'outputs'

# ------ class


class Layout:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.drawables = set()
        self.layouts = set()
        self.strings = set()
        self.styles = set()
        self.animations = set()
        self.ref = 0

    def addDrawable(self, d):
        self.drawables.add(d)

    def addLayout(self, d):
        self.layouts.add(d)

    def addString(self, d):
        self.strings.add(d)

    def addStyle(self, d):
        self.styles.add(d)

    def addAnimation(self, d):
        self.animations.add(d)

    def addRef(self):
        self.ref += 1

    def removeRef(self):
        self.ref -= 1


class Drawable:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.ref = 0
        self.drawables = set()

    def addRef(self):
        self.ref += 1

    def removeRef(self):
        self.ref -= 1


class String:
    def __init__(self, name):
        self.name = name
        self.ref = 0

    def addRef(self):
        self.ref += 1

    def removeRef(self):
        self.ref -= 1


class Style:
    def __init__(self, name):
        self.name = name
        self.ref = 0
        self.parent = ""
        self.styles = set()
        self.drawables = set()
        self.animations = set()

    def addRef(self):
        self.ref += 1

    def removeRef(self):
        self.ref -= 1


class Animation:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.ref = 0
        self.drawables = set()

    def addRef(self):
        self.ref += 1

    def removeRef(self):
        self.ref -= 1


# ------ functions


def get_filename(path):
    """
    return a filename from a path
    :param path:an absolute path for a file
    :return:
    """
    filename = os.path.basename(path)
    return filename.split('.')[0]


# read project path
def get_project_path(path):
    for line in open(path):
        line = line.strip()
        return line


# read exclusions
def get_exclusion_set(path):
    e = set()
    for line in open(path):
        line = line.strip()
        e.add(line)
    return e


# read all needed kmob resources
def read_kmob_drawables(path):
    global kmob_drawables
    for line in open(path):
        line = line.strip()
        kmob_drawables.add(line)


def read_kmob_layouts(path):
    global kmob_layouts
    for line in open(path):
        line = line.strip()
        kmob_layouts.add(line)


def read_kmob_strings(path):
    global kmob_strings
    for line in open(path):
        line = line.strip()
        kmob_strings.add(line)


# read all layouts file in the folder 'layout'
def read_layouts(res_folder_path):
    global used_layouts
    global used_strings
    global used_styles
    global layout_objs

    global layout_dict
    global drawable_dict
    global animation_dict
    global style_dict
    global all_ids

    p = re.compile('@layout/(\w*)')
    p_string = re.compile('@string/(\w*)')
    p_style = re.compile('@style/([\w|\.]+)')
    p_drawable = re.compile('@drawable/(\w*)')
    p_anim = re.compile('@anim/(\w*)')
    p_id = re.compile('@\+?id/(\w*)')
    is_comment = False

    # scan xml filename
    for folder in os.listdir(res_folder_path):
        if folder.startswith('layout'):
            for f in os.listdir(os.path.join(res_folder_path, folder)):
                if os.path.isdir(os.path.join(res_folder_path, folder, f)):
                    pass
                else:
                    filename = f.split('.')
                    pre = filename[0]
                    ext = filename[1]
                    if ext.lower() == 'xml':
                        layout_dict[pre] = Layout(pre, res_folder_path + os.sep + folder + os.sep + f)

    # scan xml contents
    for folder in os.listdir(res_folder_path):
        if folder.startswith('layout'):
            for f in os.listdir(res_folder_path + os.sep + folder):
                if os.path.isdir(res_folder_path + os.sep + folder + os.sep + f):
                    pass
                else:
                    filename = f.split('.')
                    pre = filename[0]
                    ext = filename[1]
                    if ext.lower() == 'xml':
                        # init a Layout Object
                        if layout_dict.get(pre):
                            layout_obj = layout_dict[pre]
                        else:
                            continue
                        for line in open(res_folder_path + os.sep + folder + os.sep + f):
                            line = line.strip()
                            if line.startswith('<!--'):
                                is_comment = True
                            if line.endswith('-->'):
                                is_comment = False
                                continue
                            if is_comment:
                                continue
                            # match the drawables
                            d = p_drawable.search(line)
                            if d:
                                drawable = d.group(1)
                                layout_obj.addDrawable(drawable)

                                if drawable_dict.get(drawable):
                                    drawable_dict[drawable].addRef()
                                else:
                                    drawable_dict[drawable] = Drawable(drawable)
                                    drawable_dict[drawable].addRef()
                            # match the style
                            t = p_style.search(line)
                            if t:
                                style = t.group(1)
                                layout_obj.addStyle(style)
                                if style_dict.get(style):
                                    style_dict[style].addRef()
                                else:
                                    style_dict[style] = Style(style)
                                    style_dict[style].addRef()
                            # match the string
                            s = p_string.search(line)
                            if s:
                                string = s.group(1)
                                layout_obj.addString(string)

                                if string_dict.get(string):
                                    string_dict[string].addRef()
                                else:
                                    string_dict[string] = String(string)
                                    string_dict[string].addRef()
                            # match the anim
                            a = p_anim.search(line)
                            if a:
                                anim = a.group(1)
                                layout_obj.addAnimation(anim)

                                if animation_dict.get(anim):
                                    animation_dict[anim].addRef()
                                else:
                                    animation_dict[anim] = Animation(anim)
                                    animation_dict[anim].addRef()
                            # match the layout
                            m = p.search(line)
                            if m:
                                layout = m.group(1)
                                # layout inside another layout
                                layout_obj.addLayout(layout)
                                # layout ref puls one
                                if layout_dict.get(layout):
                                    layout_dict[layout].addRef()
                                else:
                                    layout_dict[layout] = Layout(layout)
                                    layout_dict[layout].addRef()
                                    # match the id
                                    # m_id = p_id.search(line)
                                    # if m_id:
                                    # item_id = m_id.group(1)
                                    # if item_id in all_ids:
                                    # used_layouts.add(layout_obj.name)


def read_android_manifest(xml):
    # print manifest
    global xml_activities
    global used_styles
    p1 = re.compile('android:name=".*"')
    p2 = re.compile('<activity\s+android:name=".*"')
    p_style = re.compile('@style/([\w|\.]+)')
    is_comment = False
    is_activity = False
    for line in open(xml):
        line = line.strip()

        if line.startswith('<!--'):
            is_comment = True
        if line.endswith('-->'):
            is_comment = False
            continue
        if is_comment:
            continue
        # match the style
        s = p_style.search(line)
        if s:
            style = s.group(1)
            used_styles.add(style)
        if line.startswith('<activity'):
            is_activity = True
            m = p2.match(line)
            if m:
                activity = get_activity_name(line)
                xml_activities.add(activity)
                is_activity = False
                continue
        if is_activity:
            m = p1.match(line)
            if m:
                activity = get_activity_name(line)
                xml_activities.add(activity)
                is_activity = False
                continue


def read_all_java(src_path):
    for f in os.listdir(src_path):
        if os.path.isdir(os.path.join(src_path, f)):
            read_all_java(os.path.join(src_path, f))
        else:
            filename = f.split('.')
            if len(filename) > 1:
                name = filename[0]
                ext = filename[1]
                if ext.lower() == 'java':
                    read_class(os.path.join(src_path, f))
                else:
                    pass
            else:
                pass


def read_class(f):
    global child_activities
    global base_activities
    global used_layouts
    global others
    global used_drawables
    global used_strings
    global used_styles
    global used_animations
    global cm_reports
    global all_ids
    package = ""
    p_java = re.compile('.*class\s+.*\s+extends\s+.*')
    p_layout = re.compile('R\.layout\.(\w*)')
    p_drawable = re.compile('R\.drawable\.(\w*)')
    p_string = re.compile('R\.string\.(\w*)')
    p_string_android = re.compile('android\.R\.string\.(\w*)')
    p_style = re.compile('R\.style\.(\w*)')
    p_style_android = re.compile('android\.R\.style\.(\w*)')
    p_id = re.compile('R\.id\.(\w*)')

    p_report = re.compile('KInfocClientAssist\.getInstance\(\)\.reportData')
    p_force_report = re.compile('KInfocClientAssist\.getInstance\(\)\.forceReportData')
    p_report_param = re.compile('KInfocClientAssist\.getInstance\(\)\.reportData\(\"(\w*)\".*')
    p_force_report_param = re.compile('KInfocClientAssist\.getInstance\(\)\.forceReportData\(\"(\w*)\".*')
    p_table = re.compile('\"(\w*)\"')

    p_anim = re.compile('R\.anim\.(\w*)')

    is_comment = False
    filename = os.path.basename(f)
    report_class = filename.split('.')[0]
    if report_class.startswith('cm_'):
        cm_reports.add(report_class)
    for line in open(f):
        line = line.strip()
        if line.startswith("//"):
            continue
        if line.startswith("/**") > 0 or line.startswith("/*") > 0:
            is_comment = True
        if line.find("*/") >= 0:
            is_comment = False
            continue
        if is_comment:
            continue
            # if line.startswith("package"):
            # package = getPackageName(line)
            # filename = get_filename(f)

        # # match the id
        # ids = p_id.findall(line)
        # if ids:
        # for item in ids:
        # all_ids.add(item)
        # match the db table name
        m_table = p_table.search(line)
        if m_table:
            table = m_table.group(1)
            if table.startswith('cm_'):
                used_tables.add(table)
        # match the layout
        m_layout = p_layout.search(line)
        if m_layout:
            layout = m_layout.group(1)
            used_layouts.add(layout)
        # match the string
        m_android_string = p_string_android.findall(line)
        if m_android_string:
            pass
        else:
            m_string = p_string.findall(line)
            if m_string:
                for string in m_string:
                    used_strings.add(string)
        # match the drawable
        m_drawable = p_drawable.findall(line)
        if m_drawable:
            for drawable in m_drawable:
                used_drawables.add(drawable)
        # match the styles
        m_android_style = p_style_android.findall(line)
        if m_android_style:
            pass
        else:
            m_style = p_style.findall(line)
            if m_style:
                for style in m_style:
                    used_styles.add(style)
        # match the animations
        m_anim = p_anim.findall(line)
        if m_anim:
            for anim in m_anim:
                used_animations.add(anim)
        # match the extends
        m_java = p_java.match(line)
        if m_java:
            keywords = line.split()
            for i in range(len(keywords)):
                if keywords[i].lower() == 'extends':
                    break
            # child = str(package)+"."+keywords[i-1]
            child = keywords[i - 1]
            base = keywords[i + 1]

            if base.endswith('{'):
                base = base[0:len(base) - 1]
            if base in base_activities:
                child_activities.add(child)
                # scanOthers(child)
            if base in child_activities:
                base_activities.add(base)
                child_activities.add(child)
                scan_others(base)
            else:
                others.add((child, base))


def scan_others(activity):
    global others
    removes = set()
    for clz in others:
        if clz[1] == activity:
            child_activities.add(clz[0])
            removes.add(clz)
    others = others - removes


def get_package_name(line):
    line = line.strip()
    pattern = re.compile('package\s+.*;')
    m = pattern.match(line)
    if m:
        start = line.find('package', 0) + len('package')
        end = line.rfind(';', 0)
        return line[start + 1:end]


def get_activity_name(string):
    start = string.find("\"", 0)
    end = string.rfind("\"", 0)
    package = string[start + 1:end]
    components = package.split('.')
    activity = components[-1]
    return activity


def write_output(filename, set_name):
    if os.path.isdir(output_folder):
        pass
    else:
        os.mkdir(output_folder)
    filename = output_folder + os.sep + filename
    result = list(set_name)
    result.sort()
    output = open(filename, 'w')
    for x in result:
        output.write(x + '\n')
    output.close()


def clean_others():
    global others
    removes = set()
    for x in others:
        child = x[0]
        base = x[1]
        if child.endswith('Activity') or base.endswith('Activity'):
            child_activities.add(child)
            base_activities.add(base)
            removes.add(x)
    others = others - removes


def read_all_animation_file(res_path):
    global animation_dict
    for folder in os.listdir(res_path):
        if os.path.isdir(os.path.join(res_path, folder)) and folder.startswith('anim'):
            path = os.path.join(res_path, folder)
            for f in os.listdir(path):
                if os.path.isdir(os.path.join(path, f)):
                    pass
                else:
                    filename = f.split('.')
                    pre = filename[0]
                    animation_dict[pre] = Animation(pre, os.path.join(path, f))


def read_all_drawable_file(res_path):
    global drawable_dict
    for folder in os.listdir(res_path):
        if os.path.isdir(os.path.join(res_path, folder)) and folder.startswith('drawable'):
            path = os.path.join(res_path, folder)
            for f in os.listdir(path):
                if os.path.isdir(os.path.join(path, f)):
                    pass
                else:
                    filename = f.split('.')
                    pre = filename[0]
                    drawable_dict[pre] = Drawable(pre, os.path.join(path, f))


# read all nested drawable in xml except layouts and styles
def read_nested_drawables(res_folder_path):
    global used_drawables
    global drawable_dict
    global animation_dict
    pattern = re.compile('@drawable/(\w*)')
    for folder in os.listdir(res_folder_path):
        if folder.startswith('layout'):
            continue
        for f in os.listdir(os.path.join(res_folder_path, folder)):
            if os.path.isdir(os.path.join(res_folder_path, folder, f)):
                pass
            elif f == 'styles.xml':
                pass
            else:
                filename = f.split('.')
                if len(filename) == 2:
                    pre = filename[0]
                    ext = filename[1]
                    if ext.lower() == 'xml':
                        is_comment = False
                        for line in open(os.path.join(res_folder_path, folder, f)):
                            line = line.strip()
                            if line.startswith('<!--'):
                                is_comment = True
                            # comment inside the line
                            elif line.find('<!--') > 0:
                                if line.endswith('-->'):
                                    is_comment = False
                            if is_comment and line.endswith('-->'):
                                is_comment = False
                                continue
                            if is_comment:
                                continue
                            m_drawables = pattern.search(line)
                            if m_drawables:
                                d = m_drawables.group(1)
                                if drawable_dict.get(pre):
                                    outer = drawable_dict[pre]
                                    if d in outer.drawables:
                                        pass
                                    else:
                                        outer.drawables.add(d)
                                        if drawable_dict.get(d):
                                            drawable_dict[d].addRef()
                                elif animation_dict.get(pre):
                                    anim = animation_dict[pre]
                                    anim.drawables.add(d)
                                    if drawable_dict.get(d):
                                        drawable_dict[d].addRef()


def read_all_strings(res_path):
    global string_dict
    pattern = re.compile('<string name="(\w*)"')
    for folder in os.listdir(res_path):
        if folder.startswith('values'):
            for f in os.listdir(os.path.join(res_path, folder)):
                filename = f.split('.')
                if len(filename) == 2:
                    pre = filename[0]
                    ext = filename[1]
                    if pre.startswith('strings'):
                        for line in open(os.path.join(res_path, folder, f)):
                            m = pattern.search(line)
                            if m:
                                name = m.group(1)
                                # exclude widget and preference
                                if name.lower().startswith('widget') or name.lower().startswith("pref"):
                                    continue
                                else:
                                    string_dict[name] = String(name)


def read_all_styles(res_path):
    global xml_styles
    global unused_layouts
    global style_dict
    global drawable_dict
    global animation_dict

    pattern = re.compile('<style name="([\w|\.]+)"')
    p_item = re.compile('<item.*@style/([\w|\.]+)')
    p_parent = re.compile('<style name="([\w|\.]+)"\s+parent="(.+?)"')
    p_drawable = re.compile('@drawable/(\w+)')
    p_end = re.compile('</style>')
    p_anim = re.compile('@anim/(\w+)')

    # read all styles in styles.xml into dict
    for folder in os.listdir(res_path):
        if folder.startswith('values'):
            for f in os.listdir(os.path.join(res_path, folder)):
                filename = f.split('.')
                if len(filename) == 2:
                    pre = filename[0]
                    ext = filename[1]
                    if pre.startswith('style'):
                        for line in open(os.path.join(res_path, folder, f)):
                            m_style = pattern.search(line)
                            if m_style:
                                name = m_style.group(1)
                                style_dict[name] = Style(name)

    # read all nested or included styles in xml
    for folder in os.listdir(res_path):
        if folder.startswith('values'):
            for f in os.listdir(os.path.join(res_path, folder)):
                filename = f.split('.')
                if len(filename) == 2:
                    pre = filename[0]
                    ext = filename[1]
                    if pre.startswith('style') or pre.startswith('theme'):
                        style_obj = None
                        for line in open(os.path.join(res_path, folder, f)):
                            line = line.strip()
                            m_style = pattern.search(line)
                            if m_style:
                                name = m_style.group(1)
                                if style_dict.get(name):
                                    style_obj = style_dict[name]
                                    if name.find(".") > -1:
                                        fullname = name.split(".")
                                        parent = fullname[0]
                                        if style_dict.get(parent):
                                            style_dict[parent].addRef()
                                        else:
                                            style_obj.parent = parent
                                            style_dict[parent] = Style(parent)
                                            style_dict[parent].addRef()

                            # match the parent style
                            m_parent = p_parent.search(line)
                            if m_parent:
                                p1 = m_parent.group(0)
                                child = m_parent.group(1)
                                parent = m_parent.group(2)
                                if parent.find("/") > -1:
                                    parent_name = parent.split("/")[1]
                                else:
                                    parent_name = parent

                                if style_obj:
                                    style_obj.parent = parent_name
                                else:
                                    style_obj = Style(child)
                                    style_obj.parent = parent_name
                                    style_dict[child] = style_obj
                                # add ref of parent
                                if style_dict.get(parent_name):
                                    style_dict[parent_name].addRef()
                                else:
                                    style_dict[parent_name] = Style(parent_name)
                                    style_dict[parent_name].addRef()
                            # match the style item
                            m_style_item = p_item.search(line)
                            if m_style_item:
                                item = m_style_item.group(1)
                                if style_obj:
                                    if style_dict.get(item):
                                        item_obj = style_dict[item]
                                        item_obj.addRef()
                                        style_obj.styles.add(item)
                                else:
                                    if style_dict.get(item):
                                        style_dict[item].addRef()

                            # match the drawable item
                            m_drawable_item = p_drawable.search(line)
                            if m_drawable_item:
                                drawable = m_drawable_item.group(1)
                                if style_obj:
                                    if drawable in style_obj.drawables:
                                        pass
                                    else:
                                        style_obj.drawables.add(drawable)
                                        if drawable_dict.get(drawable):
                                            drawable_dict[drawable].addRef()

                            # match the anim item
                            m_anim = p_anim.search(line)
                            if m_anim:
                                anim = m_anim.group(1)
                                if style_obj:
                                    if anim in style_obj.animations:
                                        pass
                                    else:
                                        style_obj.animations.add(anim)
                                        if animation_dict.get(anim):
                                            animation_dict[anim].addRef()

                            m_end = p_end.search(line)
                            if m_end:
                                style_obj = None


def read_kfmt_file(path):
    global all_tables
    p_num = re.compile('.+\d+$')
    for line in open(path):
        table_name = line.split(':')[0]
        m = p_num.search(table_name)
        if m:
            # skip all table ends with numbers
            pass
        else:
            # skip 'cm_public'
            if not table_name.startswith('cm_public'):
                all_tables.add(table_name)


def reduce_drawable_refs(drawable):
    """
    reduce refs of sub drawables
    :param drawable:
    """
    global drawable_dict
    # reduce sub drawable refs
    for d in drawable.drawables:

        if drawable_dict.get(d):
            drawable_dict[d].removeRef()
            reduce_drawable_refs(drawable_dict[d])


# recursively reduce style ref
def reduce_style_refs(style):
    global style_dict
    global drawable_dict
    global animation_dict

    # reduce parent style refs
    if style.parent:
        if style_dict.get(style.parent):
            reduce_style_refs(style_dict[style.parent])
    # reduce sub style refs
    for s in style.styles:
        if style_dict.get(s):
            item = style_dict[s]
            item.removeRef()
            reduce_style_refs(item)
    # reduce sub drawable refs
    for d in style.drawables:
        if drawable_dict.get(d):
            item = drawable_dict[d]
            item.removeRef()
            reduce_drawable_refs(item)
    # reduce sub animation refs
    for a in style.animations:
        if animation_dict.get(a):
            anim = animation_dict[a]
            anim.removeRef()
            reduce_animation_ref(anim)


# recursively reduce layout ref
def reduce_layout_refs(layout):
    global style_dict
    global drawable_dict
    global layout_dict
    global string_dict
    global drawable_dict
    global animation_dict

    # reduce sub layout refs
    for l in layout.layouts:
        if layout_dict.get(l):
            item = layout_dict[l]
            item.removeRef()
            reduce_layout_refs(item)
    # reduce sub style refs
    for s in layout.styles:
        if style_dict.get(s):
            item = style_dict[s]
            item.removeRef()
            reduce_style_refs(item)
    # reduce sub drawable refs
    for d in layout.drawables:
        if drawable_dict.get(d):
            item = drawable_dict[d]
            item.removeRef()
            reduce_drawable_refs(item)
    # reduce sub string refs
    for t in layout.strings:
        if string_dict.get(t):
            item = string_dict[t]
            item.removeRef()
    # reduce sub animations refs
    for a in layout.animations:
        if animation_dict.get(a):
            item = animation_dict[a]
            item.removeRef()
            reduce_animation_ref(item)


def reduce_animation_ref(anim):
    global animation_dict
    global drawable_dict

    for d in anim.drawables:
        if drawable_dict.get(d):
            element = drawable_dict[d]
            element.removeRef()
            reduce_drawable_refs(element)


def set_drawable_used(obj):
    global used_drawables
    global drawable_dict

    used_drawables.add(obj.name)
    for d in obj.drawables:
        if drawable_dict.get(d):
            element = drawable_dict[d]
            set_drawable_used(element)


def set_style_used(obj):
    global used_styles
    global used_strings
    global style_dict
    global drawable_dict
    global string_dict
    global animation_dict

    used_styles.add(obj.name)
    if obj.parent:
        if style_dict.get(obj.parent):
            set_style_used(style_dict[obj.parent])
    for element in obj.styles:
        if style_dict.get(element):
            set_style_used(style_dict[element])
    for element in obj.drawables:
        if drawable_dict.get(element):
            set_drawable_used(drawable_dict[element])
    for element in obj.animations:
        if animation_dict.get(element):
            set_animation_used(animation_dict[element])


def set_layout_used(obj):
    global used_layouts
    global used_styles
    global used_strings
    global layout_dict
    global style_dict
    global drawable_dict
    global string_dict

    used_layouts.add(obj.name)
    for element in obj.layouts:
        if layout_dict.get(element):
            set_layout_used(layout_dict[element])
    for element in obj.styles:
        if style_dict.get(element):
            set_style_used(style_dict[element])
    for element in obj.drawables:
        if drawable_dict.get(element):
            set_drawable_used(drawable_dict[element])
    for element in obj.strings:
        used_strings.add(element)
    for element in obj.animations:
        if animation_dict.get(element):
            set_animation_used(animation_dict[element])


def set_animation_used(obj):
    global used_animations
    global drawable_dict

    used_animations.add(obj.name)
    for element in obj.drawables:
        if drawable_dict.get(element):
            set_drawable_used(drawable_dict[element])


def get_underscore_name(name):
    if name.find(".") > -1:
        return name.replace(".", "_")
    else:
        return name


def get_unused_drawables(outputname):
    global exclusions
    global used_drawables
    global drawable_dict
    zero_refs = set()
    # calculate the refs
    for key in drawable_dict:
        drawable = drawable_dict[key]
        if key in used_drawables:
            set_drawable_used(drawable)
        else:
            filename = drawable.path
            if drawable.ref <= 0:
                reduce_drawable_refs(drawable)
    # add exclusions to used set
    for pre in exclusions:
        for key in drawable_dict:
            item = drawable_dict[key]
            name = item.name
            if name.startswith(pre):
                # print 'drawables >>>>>>>>>>>>>>', name
                used_drawables.add(name)

    # add unused drawables to set
    for key in drawable_dict:
        item = drawable_dict[key]
        name = item.name

        if name in used_drawables:
            pass
        else:
            filename = item.path
            if item.ref <= 0:
                zero_refs.add(filename)

    write_output(outputname, zero_refs)
    print "unused drawables:", len(zero_refs)


def get_unused_layouts(outputname):
    global used_layouts
    global layout_dict

    zero_refs = set()
    all_list = []
    # add all layouts into a list and sort them
    for key in layout_dict:
        all_list.append(layout_dict[key])
    sorted_list = sorted(all_list, key=lambda x: len(x.layouts), reverse=True)
    # calculate the refs
    for layout in sorted_list:
        name = layout.name
        if name in used_layouts:
            set_layout_used(layout)
        else:
            if layout.ref <= 0:
                reduce_layout_refs(layout)

    # add exclusions to used set
    for pre in exclusions:
        for key in layout_dict:
            item = layout_dict[key]
            name = item.name
            if name.startswith(pre):
                # print 'layouts >>>>>>>>>>>>>>', name
                used_layouts.add(name)

    # add unused layouts to set
    for key in layout_dict:
        obj = layout_dict[key]
        name = obj.name
        if name in used_layouts:
            pass
        else:
            if layout_dict[key].ref <= 0:
                filename = layout_dict[key].path
                zero_refs.add(filename)

    write_output(outputname, zero_refs)
    print "unused layouts:", len(zero_refs)


def get_unused_styles(outputname):
    global used_styles
    global style_dict
    zero_refs = set()
    # add all styles into a list and sort them by the count of sub styles
    all_list = []
    for key in style_dict:
        all_list.append(style_dict[key])
    sorted_list = sorted(all_list, key=lambda x: len(x.styles), reverse=True)
    # calculate the refs
    for style in sorted_list:
        name = style.name
        tmp_name = get_underscore_name(name)
        if tmp_name in used_styles:
            set_style_used(style)
        else:
            if style.ref <= 0:
                reduce_style_refs(style)

    # add exclusions to used set
    for pre in exclusions:
        for key in style_dict:
            item = style_dict[key]
            name = item.name
            if name.startswith(pre):
                # print 'styles >>>>>>>>>>>>>>', name
                used_styles.add(name)
    # add unused styles to set
    for key in style_dict:
        name = style_dict[key].name
        if name in used_styles:
            pass
        else:
            if style_dict[key].ref <= 0:
                zero_refs.add(name)

    write_output(outputname, zero_refs)
    print "unused styles:", len(zero_refs)


def get_unused_strings(outputname):
    global used_strings
    global string_dict
    global exclusions
    zero_refs = set()

    # add exclusions to used set
    for pre in exclusions:
        for key in string_dict:
            item = string_dict[key]
            name = item.name
            if name.startswith(pre):
                print 'strings >>>>>>>>>>>>>>', name
                used_strings.add(name)

    for key in string_dict:
        if key in used_strings:
            pass
        else:
            name = string_dict[key].name
            if string_dict[key].ref <= 0:
                zero_refs.add(name)

    write_output(outputname, zero_refs)
    print "unused strings:", len(zero_refs)


def get_unused_animations(outputname):
    global used_animations
    global animation_dict
    global exclusions
    zero_refs = set()

    for key in animation_dict:
        anim = animation_dict[key]
        if anim.name in used_animations:
            set_animation_used(anim)
        else:
            if anim.ref <= 0:
                reduce_animation_ref(anim)

    # add exclusions to used set
    for pre in exclusions:
        for key in animation_dict:
            item = animation_dict[key]
            name = item.name
            if name.startswith(pre):
                # print 'anim >>>>>>>>>>>>>>', name
                used_animations.add(name)

    for key in animation_dict:
        anim = animation_dict[key]
        if anim.name in used_animations:
            pass
        else:
            if anim.ref <= 0:
                zero_refs.add(anim.path)

    write_output(outputname, zero_refs)
    print "unused animations:", len(zero_refs)


def read_used_tables(path):
    global used_tables
    for line in open(path):
        line = line.strip()
        used_tables.add(line)

# ------------- run the tool
project_path = get_project_path("project_path.txt")
exclusions = get_exclusion_set("exclusions.txt")
# ----- paths
src_folder = os.path.join(project_path, "src")
layout_folder = os.path.join(project_path, "res", "layout")
res_folder = os.path.join(project_path, "res")
manifest = os.path.join(project_path, "AndroidManifest.xml")


# --- read all things
read_android_manifest(manifest)
read_all_java(src_folder)
read_all_animation_file(res_folder)
read_all_drawable_file(res_folder)
read_nested_drawables(res_folder)
read_all_styles(res_folder)
read_all_strings(res_folder)
read_layouts(res_folder)

get_unused_layouts("unused_layouts.txt")
get_unused_styles("unused_styles.txt")
get_unused_animations("unused_animations.txt")
get_unused_strings("unused_strings.txt")
get_unused_drawables("unused_drawables.txt")