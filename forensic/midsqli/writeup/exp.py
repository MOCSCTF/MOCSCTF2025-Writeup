from urllib.parse import unquote
import re

flag = ['' for i in range(50)]
with open('out.txt') as f:
    c = unquote(f.read())
    pattern = '(\d+\.\d+)\s+.+,(\d+),1\)\)>(\d+)\),1\)\)-- '
    _re = re.findall(pattern,c)
    for i in range(0,len(_re),1):
        reqtime,_index,_ascii = _re[i]
        restime = _re[i+1][0]
        interv = float(restime) - float(reqtime)
        if(interv > 0.5):
            flag[int(_index)] = chr(int(_ascii) + 1)
            print(''.join(flag))
        else:
            flag[int(_index)] = chr(int(_ascii))
            print(''.join(flag))

# MOCSCTF{3fa9238670ef3eb99462b9593c3aaa85}