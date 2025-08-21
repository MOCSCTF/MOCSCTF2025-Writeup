import zipfile
from binascii import crc32

flag = ''
_zipfile = zipfile.ZipFile('./flag.zip')
for i in range(41):
    _crc = _zipfile.getinfo('flag/{}.txt'.format(str(i))).CRC
    for j in range(32,127):
        if(crc32(chr(j).encode()) == _crc):
           flag += chr(j)
           print(flag)
           break 

# MOCSCTF{9fc0b9fd2d3f666c8e3631dce9fe2d4d}