from zipfile import ZipFile
with ZipFile("project mad1.zip", 'r') as zip:
    zip.extractall("Unzipped")

import checksumdir
hash = checksumdir.dirhash("Unzipped")
print(hash)