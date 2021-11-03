# coding: utf-8
# author: myc
# 
# Match all files in the specified directory and print the content that meets the regular rules.


import re
import os
import sys
import argparse


def get_files(path, isabs=True):
    files = []
    if os.path.isfile(path):
        if isabs:
            files.append(path)
        else:
            files.append(os.path.basename(path))
    elif os.path.isdir(path):
        file_list = os.listdir(path)
        for i in range(len(file_list)):
            _path = os.path.join(path, file_list[i])
            files.extend(get_files(_path, isabs))
    return files


def read_file(filepath, mode='r'):
    if not os.path.isfile(filepath):
        return ""
    file = open(filepath, mode)
    content = file.read()
    file.close()
    return content


def match_response(regex, content):
    items = re.findall(regex, content)
    if items:
        for item in items:
            print(" ".join(item))


def main(path, regex):
    files = get_files(path)
    for file in files:
        content = read_file(file)
        match_response(regex, content)


if __name__ == '__main__':
    usage = "{} -p path -r regex".format(sys.argv[0])
    parser = argparse.ArgumentParser(prog="Match Multifile", usage=usage)
    parser.add_argument("-p", dest="path", help="file directory")
    parser.add_argument("-r", dest="regex", default="", help="regular expression")
    args = parser.parse_args()
    if not args.path:
        print("Please specify the path")
        sys.exit()
    main(args.path, args.regex)
