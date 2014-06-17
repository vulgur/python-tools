import os
import re

project_path = ""
# project_path = "D:\workplace\Kmob"

unused_styles = set()


def read_unused_styles(path):
    global unused_styles
    for line in open(path):
        line = line.strip()
        unused_styles.add(line)


def delete_xml_styles(res_folder_path):
    global unused_styles
    pattern = re.compile('<style name="([\w|\.]+)"')
    size = 0
    for folder in os.listdir(res_folder_path):
        if folder.startswith('values'):
            for f in os.listdir(res_folder_path + os.sep + folder):
                if f.startswith('style') or f.startswith('kmob_style'):

                    infile = res_folder_path + os.sep + folder + os.sep + f
                    outfile = res_folder_path + os.sep + folder + os.sep + "temp"
                    infp = open(infile, 'rb')
                    outfp = open(outfile, 'wb')
                    before = os.path.getsize(infile)
                    is_in_style = False
                    for line in infp:
                        if is_in_style and line.strip().endswith('</style>'):
                            is_in_style = False
                            continue
                        if is_in_style:
                            continue
                        else:
                            m = pattern.search(line)
                            if m:
                                name = m.group(1)

                                if name in unused_styles:

                                    if not line.strip().endswith('</style>'):
                                        is_in_style = True
                                    else:
                                        is_in_style = False
                                else:
                                    outfp.write(line)

                            else:
                                outfp.write(line)

                    infp.close()
                    outfp.close()
                    after = os.path.getsize(outfile)
                    os.remove(infile)
                    os.rename(outfile, infile)
                    size = size + (before - after)
    print "delete styles size=" + str(size / 1024) + "K"
    return size


