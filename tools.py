import os
import re

# ----- global containers
java_activities = set()
xml_activities = set()
base_activities = set(['Activity', 'FragmentActivity'])
child_activities = set()
others = set()
xml_layouts = set()
used_layouts = set()
unused_layouts = set()
all_drawables_dict = {}
all_drawables = set()
used_drawables = set()
used_strings = set()
xml_strings = set()
used_styles = set()
xml_styles = set()
kmob_layouts = set()
kmob_drawables = set()
kmob_strings = set()

all_layouts = set()
all_ids = set()

layout_objs = set()
drawable_objs = set()
string_objs = set()
style_objs = set()

used_animations = set()

used_tables = set()
all_tables = set()
cm_reports = set()

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
        # d.addRef()

    def addLayout(self, d):
        self.layouts.add(d)
        # d.addRef()

    def addString(self, d):
        self.strings.add(d)
        # d.addRef()

    def addStyle(self, d):
        self.styles.add(d)
        # d.addRef()
    def addAnimation(self, d):
        self.animations.add(d)

    def addRef(self):
        self.ref = self.ref + 1

    def removeRef(self):
        self.ref = self.ref - 1


class Drawable:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.ref = 0
        self.drawables = set()

    def addRef(self):
        self.ref = self.ref + 1

    def removeRef(self):
        self.ref = self.ref - 1


class String:
    def __init__(self, name):
        self.name = name
        self.ref = 0

    def addRef(self):
        self.ref = self.ref + 1

    def removeRef(self):
        self.ref = self.ref - 1


class Style:
    def __init__(self, name):
        self.name = name
        self.ref = 0
        self.parent = ""
        self.styles = set()
        self.drawables = set()
        self.animations = set()

    def addRef(self):
        self.ref = self.ref + 1

    def removeRef(self):
        self.ref = self.ref - 1


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
    return a filename frm a path
    :param path:
    :return:
    """
    filename = os.path.basename(path)
    return filename.split('.')[0]


# read project path
def readProjectPath(path):
    global project_path
    for line in open(path):
        line = line.strip()
        project_path = line


# read all needed kmob resources
def readKmobDrawables(path):
    global kmob_drawables
    for line in open(path):
        line = line.strip()
        kmob_drawables.add(line)


def readKmobLayouts(path):
    global kmob_layouts
    for line in open(path):
        line = line.strip()
        kmob_layouts.add(line)


def readKmobStrings(path):
    global kmob_strings
    for line in open(path):
        line = line.strip()
        kmob_strings.add(line)


# read all layouts file in the folder 'layout'
def readLayouts(res_folder):
    global xml_layouts
    global used_layouts
    global used_strings
    global used_styles
    global all_layouts
    global layout_objs
    global drawable_objs
    global string_objs
    global style_objs

    global layout_dict
    global drawable_dict
    global animation_dict
    global style_dict
    global all_ids
    white_layout = set()
    white_layout2 = set()

    p = re.compile('@layout/(\w*)')
    p_string = re.compile('@string/(\w*)')
    p_style = re.compile('@style/([\w|\.]+)')
    p_drawable = re.compile('@drawable/(\w*)')
    p_anim = re.compile('@anim/(\w*)')
    p_id = re.compile('@\+?id/(\w*)')
    is_comment = False

    # scan xml filename
    for folder in os.listdir(res_folder):
        if folder.startswith('layout'):
            for f in os.listdir(res_folder + os.sep + folder):
                if os.path.isdir(res_folder + os.sep + folder + os.sep + f):
                    pass
                else:
                    filename = f.split('.')
                    pre = filename[0]
                    ext = filename[1]
                    if ext.lower() == 'xml':
                        # exclude widget
                        xml_layouts.add(pre)
                        all_layouts.add(res_folder + os.sep + folder + os.sep + f)
                        layout_dict[pre] = Layout(pre, res_folder + os.sep + folder + os.sep + f)

    # scan xml contents
    for folder in os.listdir(res_folder):
        if folder.startswith('layout'):
            for f in os.listdir(res_folder + os.sep + folder):
                if os.path.isdir(res_folder + os.sep + folder + os.sep + f):
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
                        for line in open(res_folder + os.sep + folder + os.sep + f):
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
                            #     item_id = m_id.group(1)
                            #     if item_id in all_ids:
                            #         used_layouts.add(layout_obj.name)


def readXML(xml):
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
            is_comment = True;
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
                activity = getActivityName(line)
                xml_activities.add(activity)
                is_activity = False
                continue
        if is_activity:
            m = p1.match(line)
            if m:
                activity = getActivityName(line)
                xml_activities.add(activity)
                is_activity = False
                continue


def readJava(src):
    for f in os.listdir(src):
        if os.path.isdir(src + os.sep + f):
            readJava(src + os.sep + f)
        else:
            filename = f.split('.')
            if len(filename) > 1:

                name = filename[0]
                ext = filename[1]
                if ext.lower() == 'java':
                    readClass(src + os.sep + f)
                else:
                    pass
            else:
                pass


def readClass(f):
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
    reportname = filename.split('.')[0]
    if reportname.startswith('cm_'):
        cm_reports.add(reportname)
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
        #     for item in ids:
        #         all_ids.add(item)
        # match the db table name
        tableline = p_table.search(line)
        if tableline:
            table = tableline.group(1)
            if table.startswith('cm_'):
                used_tables.add(table)
        # match the layout
        l = p_layout.search(line)
        if l:
            layout = l.group(1)
            used_layouts.add(layout)
        # match the string
        s1 = p_string_android.findall(line)
        if s1:
            pass
        else:
            s = p_string.findall(line)
            if s:
                for string in s:
                    used_strings.add(string)
        # match the drawable
        d = p_drawable.findall(line)
        if d:
            for drawable in d:
                used_drawables.add(drawable)
        # match the styles
        t1 = p_style_android.findall(line)
        if t1:
            pass
        else:
            t = p_style.findall(line)
            if t:
                for style in t:
                    used_styles.add(style)
        # match the animations
        a = p_anim.findall(line)
        if a:
            for anim in a:
                used_animations.add(anim)
        # match the extends
        m = p_java.match(line)
        if m:
            keywords = line.split()
            for i in range(len(keywords)):
                if keywords[i].lower() == 'extends':
                    break
            #child = str(package)+"."+keywords[i-1]
            child = keywords[i - 1]
            base = keywords[i + 1]

            if base.endswith('{'):
                base = base[0:len(base) - 1]
            if base in base_activities:
                child_activities.add(child)
                #scanOthers(child)
            if base in child_activities:
                base_activities.add(base)
                child_activities.add(child)
                scanOthers(base)
            else:
                others.add((child, base))


def scanOthers(activity):
    global others
    removes = set()
    for clz in others:
        if clz[1] == activity:
            child_activities.add(clz[0])
            removes.add(clz)
    others = others - removes


def getPackageName(line):
    line = line.strip()
    pattern = re.compile('package\s+.*;')
    m = pattern.match(line)
    if m:
        start = line.find('package', 0) + len('package')
        end = line.rfind(';', 0)
        return line[start + 1:end]


def getActivityName(string):
    start = string.find("\"", 0)
    end = string.rfind("\"", 0)
    package = string[start + 1:end]
    components = package.split('.')
    activity = components[-1]
    return activity


def write_output(filename, setname):
    if os.path.isdir(output_folder):
        pass
    else:
        os.mkdir(output_folder)
    filename = output_folder + os.sep + filename
    result = list(setname)
    result.sort()
    output = open(filename, 'w')
    for x in result:
        output.write(x + '\n')
    output.close()


def cleanOthers():
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

def readAllAnimationFile(resFolder):
    global animation_dict
    for folder in os.listdir(resFolder):
        if os.path.isdir(resFolder + os.sep + folder) and folder.startswith('anim'):
            path = resFolder + os.sep + folder
            for f in os.listdir(path):
                if os.path.isdir(path + os.sep + f):
                    pass
                else:
                    filename = f.split('.')
                    pre = filename[0]
                    animation_dict[pre] = Animation(pre, path + os.sep + f)

def readAllDrawableFile(resFolder):
    global drawable_dict
    for folder in os.listdir(resFolder):
        if os.path.isdir(resFolder + os.sep + folder) and folder.startswith('drawable'):
            path = resFolder + os.sep + folder
            for f in os.listdir(path):
                if os.path.isdir(path + os.sep + f):
                    pass
                else:
                    filename = f.split('.')
                    pre = filename[0]
                    drawable_dict[pre] = Drawable(pre, path + os.sep + f)


# read all nested drawable in xml except layouts and styles
def readNestedDrawables(res_folder_path):
    global used_drawables
    global drawable_dict
    global animation_dict
    for folder in os.listdir(res_folder_path):
        if folder.startswith('layout'):
            continue
        for f in os.listdir(res_folder_path + os.sep + folder):
            if os.path.isdir(res_folder_path + os.sep + folder + os.sep + f):
                pass
            elif f == 'styles.xml':
                pass
            else:
                filename = f.split('.')
                if len(filename) == 2:
                    pre = filename[0]
                    ext = filename[1]
                    if ext.lower() == 'xml':
                        p = re.compile('@drawable/(\w*)')
                        isComment = False
                        for line in open(res_folder_path + os.sep + folder + os.sep + f):
                            line = line.strip()
                            if line.startswith('<!--'):
                                isComment = True;
                            # comment inside the line
                            elif line.find('<!--') > 0:
                                if line.endswith('-->'):
                                    isComment = False
                            if isComment and line.endswith('-->'):
                                isComment = False
                                continue
                            if isComment:
                                continue
                            s = p.search(line)
                            if s:
                                d = s.group(1)
                                if drawable_dict.get(pre):
                                    outter = drawable_dict[pre]
                                    if d in outter.drawables:
                                        pass
                                    else:
                                        outter.drawables.add(d)
                                        if drawable_dict.get(d):
                                            drawable_dict[d].addRef()
                                elif animation_dict.get(pre):
                                    anim = animation_dict[pre]
                                    anim.drawables.add(d)
                                    if drawable_dict.get(d):
                                        drawable_dict[d].addRef()
                                    # used_drawables.add(d)


def readAllStrings(res_folder):
    global xml_strings

    global string_dict
    pattern = re.compile('<string name="(\w*)"')
    for folder in os.listdir(res_folder):
        if folder.startswith('values'):
            for f in os.listdir(res_folder + os.sep + folder):
                filename = f.split('.')
                if len(filename) == 2:
                    pre = filename[0]
                    ext = filename[1]
                    if pre.startswith('strings'):
                        for line in open(os.path.join(res_folder, folder, f)):
                            m = pattern.search(line)
                            if m:
                                name = m.group(1);
                                # exclude widget and preference
                                if name.lower().startswith('widget') or name.lower().startswith("pref"):
                                    continue
                                else:
                                    xml_strings.add(name)
                                    string_dict[name] = String(name)


def readAllStyles(res_folder):
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
    # nested styles
    items = set()

    # read all styles in styles.xml into dict
    for folder in os.listdir(res_folder):
        if folder.startswith('values'):
            for f in os.listdir(res_folder + os.sep + folder):
                filename = f.split('.')
                if len(filename) == 2:
                    pre = filename[0]
                    ext = filename[1]
                    if pre.startswith('style'):
                        for line in open(os.path.join(res_folder, folder, f)):
                            m = pattern.search(line)
                            if m:
                                name = m.group(1)
                                style_dict[name] = Style(name)

    # read all nested or included styles in xml
    for folder in os.listdir(res_folder):
        if folder.startswith('values'):
            for f in os.listdir(res_folder + os.sep + folder):
                filename = f.split('.')
                if len(filename) == 2:
                    pre = filename[0]
                    ext = filename[1]
                    if pre.startswith('style') or pre.startswith('theme'):
                        style_obj = None
                        for line in open(os.path.join(res_folder, folder, f)):
                            line = line.strip()
                            m = pattern.search(line)
                            if m:
                                name = m.group(1)
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
                            p = p_parent.search(line)
                            if p:
                                p1 = p.group(0)
                                child = p.group(1)
                                parent = p.group(2)
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
                            t = p_item.search(line)
                            if t:
                                item = t.group(1)
                                if style_obj:
                                    if style_dict.get(item):
                                        item_obj = style_dict[item]
                                        item_obj.addRef()
                                        style_obj.styles.add(item)
                                else:
                                    if style_dict.get(item):
                                        style_dict[item].addRef()

                            # match the drawable item
                            d = p_drawable.search(line)
                            if d:
                                drawable = d.group(1)
                                if style_obj:
                                    if drawable in style_obj.drawables:
                                        pass
                                    else:
                                        style_obj.drawables.add(drawable)
                                        if drawable_dict.get(drawable):
                                            drawable_dict[drawable].addRef()

                            # match the anim item
                            a = p_anim.search(line)
                            if a:
                                anim = a.group(1)
                                if style_obj:
                                    if anim in style_obj.animations:
                                        pass
                                    else:
                                        style_obj.animations.add(anim)
                                        if animation_dict.get(anim):
                                            animation_dict[anim].addRef()

                            e = p_end.search(line)
                            if e:
                                style_obj = None


def readKfmt(path):
    global all_tables
    p_num = re.compile('.+\d+$')
    for line in open(path):
        tablename = line.split(':')[0]
        m = p_num.search(tablename)
        if m:
            # skip all table ends with numbers
            pass
        else:
            # skip 'cm_public'
            if not tablename.startswith('cm_public'):
                all_tables.add(tablename)


def reduceDrawableRef(drawable):
    """
    reduce refs of sub drawables
    :param drawable:
    """
    global drawable_dict
    # reduce sub drawable refs
    for d in drawable.drawables:

        if drawable_dict.get(d):
            drawable_dict[d].removeRef()
            reduceDrawableRef(drawable_dict[d])


# recursively reduce style ref
def reduceStyleRef(style):
    global style_dict
    global drawable_dict
    global animation_dict

    # reduce parent style refs
    if style.parent:
        if style_dict.get(style.parent):
            reduceStyleRef(style_dict[style.parent])
    # reduce sub style refs
    for s in style.styles:
        if style_dict.get(s):
            item = style_dict[s]
            item.removeRef()
            reduceStyleRef(item)
    # reduce sub drawable refs
    for d in style.drawables:
        if drawable_dict.get(d):
            item = drawable_dict[d]
            item.removeRef()
            reduceDrawableRef(item)
    # reduce sub animation refs
    for a in style.animations:
        if animation_dict.get(a):
            anim = animation_dict[a]
            anim.removeRef()
            reduceAnimationRef(anim)


# recursively reduce layout ref
def reduceLayoutRef(layout):
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
            reduceLayoutRef(item)
    # reduce sub style refs
    for s in layout.styles:
        if style_dict.get(s):
            item = style_dict[s]
            item.removeRef()
            reduceStyleRef(item)
    # reduce sub drawable refs
    for d in layout.drawables:
        if drawable_dict.get(d):
            item = drawable_dict[d]
            item.removeRef()
            reduceDrawableRef(item)
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
            reduceAnimationRef(item)

def reduceAnimationRef(anim):
    global animation_dict
    global drawable_dict

    for d in anim.drawables:
        if drawable_dict.get(d):
            element = drawable_dict[d]
            element.removeRef()
            reduceDrawableRef(element)

def setDrawableUsed(obj):
    global used_drawables
    global drawable_dict

    used_drawables.add(obj.name)
    for d in obj.drawables:
        if drawable_dict.get(d):
            element = drawable_dict[d]
            setDrawableUsed(element)


def setStyleUsed(obj):
    global used_styles
    global used_strings
    global style_dict
    global drawable_dict
    global string_dict
    global animation_dict

    used_styles.add(obj.name)
    if obj.parent:
        if style_dict.get(obj.parent):
            setStyleUsed(style_dict[obj.parent])
    for element in obj.styles:
        if style_dict.get(element):
            setStyleUsed(style_dict[element])
    for element in obj.drawables:
        if drawable_dict.get(element):
            setDrawableUsed(drawable_dict[element])
    for element in obj.animations:
        if animation_dict.get(element):
            setAnimationUsed(animation_dict[element])


def setLayoutUsed(obj):
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
            setLayoutUsed(layout_dict[element])
    for element in obj.styles:
        if style_dict.get(element):
            setStyleUsed(style_dict[element])
    for element in obj.drawables:
        if drawable_dict.get(element):
            setDrawableUsed(drawable_dict[element])
    for element in obj.strings:
        used_strings.add(element)
    for element in obj.animations:
        if animation_dict.get(element):
            setAnimationUsed(animation_dict[element])


def setAnimationUsed(obj):
    global used_animations
    global drawable_dict

    used_animations.add(obj.name)
    for element in obj.drawables:
        if drawable_dict.get(element):
            setDrawableUsed(drawable_dict[element])

# ------------- run the tool
readProjectPath("project_path.txt")

# ----- paths
src_folder = project_path + os.sep + "src"
layout_folder = project_path + os.sep + "res" + os.sep + "layout"
res_folder = project_path + os.sep + "res"

# readKmobLayouts("kmob_layouts.txt")
# readKmobStrings("kmob_strings.txt")
# readKmobDrawables("kmob_drawables.txt")

manifest = project_path + os.sep + "AndroidManifest.xml"
# --- read all things
readXML(manifest)
readJava(src_folder)
readAllAnimationFile(res_folder)
readAllDrawableFile(res_folder)
readNestedDrawables(res_folder)
readAllStyles(res_folder)
readAllStrings(res_folder)
readLayouts(res_folder)

# unused kfmt table
data = os.path.join(project_path, "assets", "kfmt.dat")
readKfmt(data)
write_output("used_tables.txt", used_tables)

unused_tables = all_tables - used_tables
write_output("unused_tables.txt", unused_tables)

# animations
# print "all animations:", len(animation_dict)
# print "used animations:", len(used_animations)
unused_animations = set(animation_dict) - used_animations
# write_output("used_animations.txt", used_animations)


def getUnderscoreName(name):
    if name.find(".") > -1:
        return name.replace(".", "_")
    else:
        return name


def getUnusedDrawables(used_set, all_dict, outputname):
    zero_refs = set()
    xml_drawables = set()
    drawable_set = set()
    pattern = re.compile('@drawable/(\w*)')
    # read drawables in drawable xml
    for key in all_dict:
        drawable = all_dict[key]
        if key in used_set:
            setDrawableUsed(drawable)
        else:
            filename = drawable.path
            if filename.find('gowidget') > -1 or filename.find('shadow_size_n') > -1:
                continue
            if drawable.ref <= 0:
                reduceDrawableRef(drawable)

    for key in all_dict:
        item = all_dict[key]
        name = item.name

        if name in used_set:
            pass
        else:
            filename = item.path
            if name.find('widget') > -1 or name.find('shadow_size_n') > -1:
                continue
            if item.ref <= 0:
                zero_refs.add(filename)

    write_output(outputname, zero_refs)
    print "unused drawables:", len(zero_refs)


def getUnusedLayouts(used_set, all_dict, outputname):
    global drawable_dict
    global style_dict
    global string_dict

    zero_refs = set()
    all_list = []
    for key in all_dict:
        all_list.append(all_dict[key])
    sorted_list = sorted(all_list, key=lambda x: len(x.layouts), reverse=True)

    for layout in sorted_list:
        name = layout.name
        if name in used_set or name.find('widget') > -1:
            setLayoutUsed(layout)
        else:
            if layout.ref <= 0:
                reduceLayoutRef(layout)

    for key in all_dict:
        obj = all_dict[key]
        name = obj.name
        if name in used_set or name.find('widget') > -1:
            pass
        else:
            if all_dict[key].ref <= 0:
                filename = all_dict[key].path
                zero_refs.add(filename)

    write_output(outputname, zero_refs)
    print "unused layouts:", len(zero_refs)


def getUnusedStyles(used_set, all_dict, outputname):
    global drawable_dict
    global style_dict
    zero_refs = set()

    all_list = []
    for key in all_dict:
        all_list.append(all_dict[key])
    sorted_list = sorted(all_list, key=lambda x: len(x.styles), reverse=True)

    for style in sorted_list:
        name = style.name
        tmp_name = getUnderscoreName(name)
        if tmp_name in used_set:
            setStyleUsed(style)
        else:
            if tmp_name.find('gowidget') > -1:
                continue
            if style.ref <= 0:
                reduceStyleRef(style)

    for key in all_dict:
        name = all_dict[key].name
        if name in used_set or name.find('widget') > -1:
            pass
        else:
            if all_dict[key].ref <= 0:
                zero_refs.add(name)

    write_output(outputname, zero_refs)
    print "unused styles:", len(zero_refs)


def getUnusedStrings(used_set, all_dict, outputname):
    zero_refs = set()

    for key in all_dict:
        if key in used_set:
            pass
        else:
            name = all_dict[key].name
            if all_dict[key].ref <= 0:
                zero_refs.add(name)

    write_output(outputname, zero_refs)
    print "unused strings:", len(zero_refs)

def getUnusedAnimations(used_set, all_dict, outputname):
    zero_refs = set()

    for key in all_dict:
        anim = all_dict[key]
        if anim.name in used_set:
            setAnimationUsed(anim)
        else:
            if anim.ref <= 0:
                reduceAnimationRef(anim)

    for key in all_dict:
        anim = all_dict[key]
        if anim.name in used_set:
            pass
        else:
            if anim.ref <= 0:
                zero_refs.add(anim.path)

    write_output(outputname, zero_refs)
    print "unused animations:", len(zero_refs)

getUnusedLayouts(used_layouts, layout_dict, "zero_refs_layouts.txt")
getUnusedStyles(used_styles, style_dict, "zero_refs_styles.txt")
getUnusedAnimations(used_animations, animation_dict, "zero_refs_animations.txt")
getUnusedStrings(used_strings, string_dict, "zero_refs_strings.txt")
getUnusedDrawables(used_drawables, drawable_dict, "zero_refs_drawables.txt")