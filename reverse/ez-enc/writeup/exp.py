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