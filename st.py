#!/usr/bin/env python3
import base64
import hashlib
import inspect
import json
import os
import random
import re
import sys
import urllib.parse


def get_files(path, full_path=True, suffix=""):
    files = []
    if os.path.isfile(path) and path.endswith(suffix):
        files.append(path if full_path else os.path.basename(path))
    elif os.path.isdir(path):
        for i in os.listdir(path):
            files.extend(get_files(os.path.join(path, i), full_path, suffix))
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

    def unicode2s(self):
        """
        unicode 转 string
        """
        return self.input.encode().decode("unicode_escape")

    def s2unicode(self):
        """
        string 转 unicode
        """
        return self.input.encode("unicode_escape").decode()

    def url2s(self):
        """
        url 转 string
        """
        return urllib.parse.unquote(self.input)

    def s2url(self):
        """
        string 转 url
        """
        return urllib.parse.quote(self.input)

    def hex2s(self):
        """
        hex 转 string
        """
        if self.input.startswith("0x"):
            self.input = self.input[2:]
        return bytes.fromhex(self.input).decode()

    def s2hex(self):
        """
        string 转 hex
        """
        return "0x" + self.input.encode().hex()

    def bin2s(self):
        """
        binary 转 string
        """
        self.input = self.input.replace(" ", "")
        return bytearray(
            int(self.input[i : i + 8], 2) for i in range(0, len(self.input), 8)
        ).decode()

    def s2bin(self):
        """
        string 转 binary
        """
        return " ".join(format(byte, "08b") for byte in self.input.encode())

    def b642s(self):
        """
        base64  转 string
        """
        return base64.b64decode(self.input.encode()).decode()

    def s2b64(self):
        """
        string 转 base64
        """
        return base64.b64encode(self.input.encode()).decode()

    def len(self):
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

    def rs(self):
        """
        string 倒序
        """
        return self.input[::-1]

    def rands(self):
        """
        随机字符串
        """
        pwd = ""
        char = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        for i in range(int(self.input)):
            pwd += random.choice(char)
        return pwd

    def jsonf(self):
        """
        json 格式化
        """
        obj = json.loads(self.input)
        return json.dumps(obj, sort_keys=True, indent=4, separators=(",", ":"))

    def refind(self):
        """
        正则提取
        """
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

    def dedup2(self):
        """
        双列去重
        """
        new_file = sys.argv.pop(-1)
        if not os.path.exists(new_file):
            col = new_file.splitlines()
        else:
            with open(new_file) as f:
                col = f.read().splitlines()
        return "\n".join(
            [i for i in [line for line in self.input.splitlines()] if i not in col]
        )

    def col(self):
        """
        按列取值 -> st.py col [sep] [num] file.txt
        """
        n = int(sys.argv.pop(-1))
        sep = sys.argv[2] or " "
        return "\n".join(
            i.split(sep)[n] for i in [line for line in self.input.splitlines()]
        )


def print_usage():
    print(f"Usage:\n\t{sys.argv[0]} [function] [string|path|length|regex]")
    print("\nAvailable functions:\n")
    st = StrTool()
    functions = [
        (name, inspect.getdoc(getattr(st, name)))
        for name in dir(st)
        if callable(getattr(st, name))
    ]
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
        funcs = sys.argv[1]
        # print("functions: {}".format(" -> ".join(funcs.split("|"))))
        for func in funcs.split("|"):
            result = getattr(st, func)()
            st._set_input(str(result))  # function chains input
        print(result)
    except Exception as err:
        print(f"\nError: {err}\n")
        print_usage()
