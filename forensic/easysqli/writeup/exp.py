from urllib.parse import unquote
import re

with open('./access.log') as f:
    c = unquote(f.read())
    # _re = re.findall('.*flag.*',c)
    pattern = 'flag ORDER BY flag LIMIT 0,1\),(\d+),1\)\)!=(\d+),'
    _re = re.findall(pattern,c)
    flag = ['' for i in range(42)]
    for i,a in _re:
        flag[int(i)] = chr(int(a))
        print(''.join(flag))

# MOCSCTF{cb2c8d87721dcbbd0a8f8c3ebaecaf78}