# writeup説明

ida反編譯main函數如下，很明顯sub_14BC生成密鑰，sub_1315加密，unk_4060是比較的值

~~~c++
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  _QWORD v4[2]; // [rsp+0h] [rbp-60h] BYREF
  char s[56]; // [rsp+10h] [rbp-50h] BYREF
  char *v6; // [rsp+48h] [rbp-18h]
  size_t v7; // [rsp+50h] [rbp-10h]
  int i; // [rsp+5Ch] [rbp-4h]

  if ( fgets(s, 41, stdin) )
  {
    v7 = strcspn(s, "\n");
    if ( v7 == 40 )
    {
      v4[0] = 0LL;
      v4[1] = 0LL;
      sub_14BC(v4);
      for ( i = 0; i <= 4; ++i )
      {
        v6 = &s[8 * i];
        sub_1315(v6, v4);
      }
      if ( !memcmp(s, &unk_4060, 0x28uLL) )
        puts("Flag correct!");
      else
        puts("Wrong.");
      return 0LL;
    }
    else
    {
      return 1LL;
    }
  }
  else
  {
    perror("fgets");
    return 1LL;
  }
}
~~~

查看sub_14BC，可以發現對main后1056字節做了MD5加密

~~~c++
int *__fastcall sub_14BC(__int64 a1)
{
  int *result; // rax
  _BYTE v2[96]; // [rsp+10h] [rbp-80h] BYREF
  _BYTE v3[16]; // [rsp+70h] [rbp-20h] BYREF
  __int64 (__fastcall *v4)(int, char **, char **); // [rsp+80h] [rbp-10h]
  int i; // [rsp+8Ch] [rbp-4h]

  v4 = main;
  MD5_Init(v2);
  MD5_Update(v2, v4, 1056LL);
  result = (int *)MD5_Final(v3, v2);
  for ( i = 0; i <= 3; ++i )
  {
    result = (int *)(4LL * i + a1);
    *result = ((unsigned __int8)v3[4 * i + 2] << 16) | ((unsigned __int8)v3[4 * i + 1] << 8) | (unsigned __int8)v3[4 * i] | ((unsigned __int8)v3[4 * i + 3] << 24);
  }
  return result;
}
~~~

返回加密後的16字節作爲key傳入sub_1315，sub_1315如下

~~~c++
__int64 __fastcall sub_1315(unsigned int *a1, __int64 a2)
{
  unsigned int v2; // eax
  unsigned int v3; // ebx
  unsigned int v4; // r12d
  unsigned int v5; // eax
  unsigned int v6; // eax
  unsigned int v7; // eax
  unsigned int v8; // eax
  unsigned int v9; // eax
  unsigned int v10; // eax
  unsigned int v11; // eax
  unsigned int v12; // ebx
  unsigned int v13; // r12d
  unsigned int v14; // eax
  unsigned int v15; // eax
  unsigned int v16; // eax
  unsigned int v17; // eax
  unsigned int v18; // eax
  __int64 result; // rax
  int i; // [rsp+10h] [rbp-20h]
  unsigned int v21; // [rsp+14h] [rbp-1Ch]
  unsigned int v22; // [rsp+18h] [rbp-18h]
  unsigned int v23; // [rsp+1Ch] [rbp-14h]

  v23 = *a1;
  v22 = a1[1];
  v21 = 0;
  for ( i = 0; i <= 31; ++i )
  {
    v2 = sub_12D3(v21, 3LL);
    v3 = sub_12BF(v21, *(unsigned int *)(4LL * v2 + a2));
    v4 = sub_12FD(v22, 5LL);
    v5 = sub_12E5(v22, 3LL);
    v6 = sub_12AD(v5, v4);
    v7 = sub_12BF(v6, v22);
    v8 = sub_12AD(v7, v3);
    v9 = sub_12AD(v8, v22);
    v23 = sub_12BF(v23, v9);
    v21 = sub_12BF(v21, 892350514LL);
    v10 = sub_12FD(v21, 11LL);
    v11 = sub_12D3(v10, 3LL);
    v12 = sub_12BF(v21, *(unsigned int *)(4LL * v11 + a2));
    v13 = sub_12FD(v23, 5LL);
    v14 = sub_12E5(v23, 3LL);
    v15 = sub_12AD(v14, v13);
    v16 = sub_12BF(v15, v23);
    v17 = sub_12AD(v16, v12);
    v18 = sub_12AD(v17, v23);
    v22 = sub_12BF(v18, v22);
  }
  *a1 = v23;
  result = v22;
  a1[1] = v22;
  return result;
}
~~~

一個個函數分析可知，每個函數都是一種運算，ida在函數名上按下n可以修改命名以幫助我們更好地分析加密算法，分析後的結果如下

~~~c++
__int64 __fastcall sub_1315(unsigned int *a1, __int64 a2)
{
  unsigned int v2; // eax
  unsigned int v3; // ebx
  unsigned int v4; // r12d
  unsigned int v5; // eax
  unsigned int v6; // eax
  unsigned int v7; // eax
  unsigned int v8; // eax
  unsigned int v9; // eax
  unsigned int v10; // eax
  unsigned int v11; // eax
  unsigned int v12; // ebx
  unsigned int v13; // r12d
  unsigned int v14; // eax
  unsigned int v15; // eax
  unsigned int v16; // eax
  unsigned int v17; // eax
  unsigned int v18; // eax
  __int64 result; // rax
  int i; // [rsp+10h] [rbp-20h]
  unsigned int v21; // [rsp+14h] [rbp-1Ch]
  unsigned int v22; // [rsp+18h] [rbp-18h]
  unsigned int v23; // [rsp+1Ch] [rbp-14h]

  v23 = *a1;
  v22 = a1[1];
  v21 = 0;
  for ( i = 0; i <= 31; ++i )
  {
    v2 = and(v21, 3);
    v3 = add(v21, *(_DWORD *)(4LL * v2 + a2));
    v4 = shr(v22, 5);
    v5 = shl(v22, 3);
    v6 = xor(v5, v4);
    v7 = add(v6, v22);
    v8 = xor(v7, v3);
    v9 = xor(v8, v22);
    v23 = add(v23, v9);
    v21 = add(v21, 0x35303032);
    v10 = shr(v21, 11);
    v11 = and(v10, 3);
    v12 = add(v21, *(_DWORD *)(4LL * v11 + a2));
    v13 = shr(v23, 5);
    v14 = shl(v23, 3);
    v15 = xor(v14, v13);
    v16 = add(v15, v23);
    v17 = xor(v16, v12);
    v18 = xor(v17, v23);
    v22 = add(v18, v22);
  }
  *a1 = v23;
  result = v22;
  a1[1] = v22;
  return result;
}
~~~

算法符合[XTEA加密](https://en.wikipedia.org/wiki/XTEA)特徵，但是魔改了三個地方

1. 左移操作由標准的4改爲3
2. DELTA值由標准的0x9E3779B9改爲了0x35303032（正好是“2025”）
3. 額外多亦或了v0和v1

只需要寫出解密算法即可，但是可以發現MD5實現了文件校驗，如果我們直接動態調試到sub_1315獲取v4（key）值，拿到的是不正確的key（原因是IDA等調試器是通過插入0xCC實現斷點，此時改變了要校驗的1056字節）。這種做法本質上是一種反調試手段。

正確做法是動態調試到MD5_Update前，**取消所有斷點**，F8執行萬MD5_Update和MD5_Final，然後回到main在sub_1315前下斷點，F9停下后v4就是正確的key值，提取16字節出來為4個DWORD大小

python解密脚本如下

~~~python
from ctypes import c_uint32


def xtea_decrypt(r, v, key):
    v0, v1 = c_uint32(v[0]), c_uint32(v[1])
    delta = 0x35303032
    total = c_uint32(delta * r)
    for i in range(r):
        v1.value -= (((v0.value << 3) ^ (v0.value >> 5)) + v0.value) ^ (total.value + key[(total.value >> 11) & 3]) ^ v0.value
        total.value -= delta
        v0.value -= (((v1.value << 3) ^ (v1.value >> 5)) + v1.value) ^ (total.value + key[total.value & 3]) ^ v1.value
    return v0.value, v1.value


if __name__ == "__main__":
    k = [0x7F7C4FBB, 0xEE5F99E6, 0x1013E69C, 0x1D70DF86]
    v = [0xF0B835D9, 0xFA32D131, 0x4A09FE50, 0xE975B582, 0xA5EB9492, 0xD21013E8, 0x9E8BBC0D, 0x8C7D9D82, 0xB00FC859, 0xF379F0FB]
    for i in range(0, len(v), 2):
        v[i:i+2] = xtea_decrypt(32, v[i:i+2], k)
    v = "".join([int.to_bytes(v[i], byteorder='little', length=4).decode() for i in range(len(v))])
    print(v)

# flag: MOCSCTF{Th1s_1s_4n_Easy_x73a_ENcryp7I0n}
~~~

flag是`MOCSCTF{Th1s_1s_4n_Easy_x73a_ENcryp7I0n}`
