#!/usr/bin/env python3
import base64
import hashlib
import inspect
import os
import sys
import urllib.parse


def get_files(path, full_path=True, suffix=""):
    files = []
    if os.path.isfile(path) and path.endswith(suffix):
        files.append(path if full_path else os.path.basename(path))
    elif os.path.isdir(path):
        for i in os.listdir(path):
            files.extend(
                get_files(os.path.join(path, i), full_path, suffix))
    return files


class StrTool:
    def __init__(self):
        self.input = ""

    def _set_input(self, input):
        if os.path.exists(input):
            files = get_files(input)
            for file in files:
                with open(file) as f:
                    self.input += f.read()
        else:
            self.input = str(input)

    def unicode2str(self):
        """
        unicode 转 string
        """
        return self.input.encode().decode("unicode_escape")

    def str2unicode(self):
        """
        string 转 unicode
        """
        return self.input.encode("unicode_escape").decode()

    def url2str(self):
        """
        url 转 string
        """
        return urllib.parse.unquote(self.input)

    def str2url(self):
        """
        string 转 url
        """
        return urllib.parse.quote(self.input)

    def hex2str(self):
        """
        hex 转 string
        """
        if self.input.startswith("0x"):
            self.input = self.input[2:]
        return bytes.fromhex(self.input).decode()

    def str2hex(self):
        """
        string 转 hex
        """
        return "0x"+self.input.encode().hex()

    def bin2str(self):
        """
        binary 转 string
        """
        self.input = self.input.replace(" ", "")
        return bytearray(int(self.input[i:i+8], 2) for i in range(0, len(self.input), 8)).decode()

    def str2bin(self):
        """
        string 转 binary
        """
        return " ".join(format(byte, '08b') for byte in self.input.encode())

    def base642str(self):
        """
        base64  转 string
        """
        return base64.b64decode(self.input.encode()).decode()

    def str2base64(self):
        """
        string 转 base64
        """
        return base64.b64encode(self.input.encode()).decode()

    def length(self):
        """
        计算string长度
        """
        return len(self.input)

    def md5(self):
        """
        string 转 md5
        """
        return hashlib.md5(self.input.encode()).hexdigest()

    def sha1(self):
        """
        string 转 sha1
        """
        return hashlib.sha1(self.input.encode()).hexdigest()

    def sha256(self):
        """
        string 转 sha256
        """
        return hashlib.sha256(self.input.encode()).hexdigest()

    def sha512(self):
        """
        string 转 sha512
        """
        return hashlib.sha512(self.input.encode()).hexdigest()

    def reverse(self):
        """
        string 倒序
        """
        return self.input[::-1]

    def randomstr(self):
        """
        随机字符串
        """
        import random
        pwd = ""
        char = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        for i in range(int(self.input)):
            pwd += random.choice(char)
        return pwd

    def jsonify(self):
        """
        json 格式化
        """
        import json
        obj = json.loads(self.input)
        return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ':'))

    def refind(self):
        """
        正则提取
        """
        import re
        regex = sys.argv[2]
        items = re.findall(regex, self.input)
        if len(items) > 1:
            return "\n".join(items)
        elif len(items) == 1:
            return items[0]
        else:
            return "not found"

    def dedup(self):
        """
        多行去重
        """
        return "\n".join(set(self.input.splitlines()))

    def column(self):
        """
        按列取值
        """
        sep = sys.argv[2]
        n = int(sys.argv[3])
        return "\n".join(i.split(sep)[n] for i in [line for line in self.input.splitlines()])


def print_usage():
    print(f"Usage:\n\t{sys.argv[0]} [function] [string|path|length|regex]")
    print("\nAvailable functions:\n")
    st = StrTool()
    functions = [(name, inspect.getdoc(getattr(st, name)))
                 for name in dir(st) if callable(getattr(st, name))]
    for f, doc in functions:
        if not f.startswith("_"):
            print(f"\t{f:15}{doc}")
    print()


if __name__ == "__main__":
    st = StrTool()
    if not sys.stdin.isatty():
        st._set_input(sys.stdin.read().strip())
    else:
        if len(sys.argv) < 3:
            print_usage()
            sys.exit(0)
        input = sys.argv.pop(-1)
        st._set_input(input)
    try:
        f = sys.argv[1]
        result = ""
        # print("functions: {}".format(" -> ".join(f.split("|"))))
        for n in f.split("|"):
            result = getattr(st, n)()
            st._set_input(str(result))  # function chains input
        print(result)
    except Exception as err:
        print(f"\nError: {err}\n")
        print_usage()
