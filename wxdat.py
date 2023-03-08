import os
import sys


def get_files(path, full_path=True, suffix=""):
    files = []
    if os.path.isfile(path) and path.endswith(suffix):
        files.append(path if full_path else os.path.basename(path))
    elif os.path.isdir(path):
        file_list = os.listdir(path)
        for i in range(len(file_list)):
            files.extend(get_files(os.path.join(path, file_list[i]), full_path, suffix))
    return files


def check_dat(dat):
    """
    根据dat文件头, 识别图片类型
    """
    magic = {
        ".png": (0x89, 0x50, 0x4e),
        ".gif": (0x47, 0x49, 0x46),
        ".jpeg": (0xff, 0xd8, 0xff)
    }
    with open(dat, "rb") as file:
        line = file.readline()
        for k, v in magic.items():
            res = []
            for i in range(0, 3):
                res.append(line[i]^v[i])
            if res[0] == res[1] == res[2]:
                return res[0], k


def decode_dat(dat_file, out_dir):
    key, ext = check_dat(dat_file)
    with open(dat_file, "rb") as dat:
        out_file = os.path.join(out_dir, os.path.basename(dat_file)) + ext
        with open(out_file, "wb") as out:
            for d in dat.read():
                out.write(bytes([d^key]))


def main(dat_dir, img_dir):
    print("[+] start...")
    dat_files = get_files(dat_dir, suffix="dat")
    total = len(dat_files)
    print("[+] total {} dat files".format(total))
    i = 0
    for dat in dat_files:
        try:
            decode_dat(dat, img_dir)
            i += 1
            progress =int((i/total)*100)
            print("\r[+] decode {} files, progress {}%\r".format(i, progress), end="")
        except Exception as e:
            print("[-] decode {} error: {}".format(dat, e))
    print("\n[+] done")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:\n\t{} <dat_dir> <out_dir>".format(sys.argv[0]))
        sys.exit(0)
    else:
        dat_dir = sys.argv[1]
        out_dir = sys.argv[2]
        main(dat_dir, out_dir)
