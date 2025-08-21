# -*- coding: utf-8 -*-
import random
import numpy as np
import wave
import random

binary_str = '1000110110110011000011100111011111101000001000101110000111100101110100110100011011001101001110111011001111110011010000011000111100001110111001001111110100010000011010001100101110000111100100100000111010111100110101110000101010001101101001110111011001010101100101011101100001110111101111111110011001111111010110111110111001110111111101001011111111010011010000110011101111101101011110101111000011001011110010101111110010001100101100000011100100110001110111011001110101110101001011001011101101110010111011011100010110010111100100101110'

def insert_random_questions(s, density=0.1):
    chars = list(s)
    insert_count = int(len(s) * density)  # 插入的总数量
    for _ in range(insert_count):
        pos = random.randint(0, len(chars))
        count = random.randint(1, 3)  # 每次插入1~3个
        chars[pos:pos] = ['?'] * count
    return ''.join(chars)

result = insert_random_questions(binary_str, density=0.5)
print('混淆后的二进制flag：'+result)


data = result # 经过混淆的二进制字符串
sample_rate = 44100  # 采样率
output_file = 'mystery_sound.wav'

bit_durations = 0.7 # 每段波形对应的持续时间
audio_data = []

for bit in data:
    if bit == '1':
        freq = random.randint(20001,22000)
        print('频率为：', freq,' 对应的字符为：1')
    elif bit == '0':
        freq = random.randint(1,18)
        print('频率为：', freq,' 对应的字符为：0')
    elif bit == '?':
        freq = random.randint(25,19500)
        print('频率为：', freq,' 对应的字符为：?')
    duration = bit_durations
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    samples = 0.5 * np.sin(2 * np.pi * freq * t)
    audio_data.extend(samples)

audio_data = np.array(audio_data)
audio_data_int = np.int16(audio_data * 32767)

# 写入wav音频
with wave.open(output_file, 'w') as wav_file:
    wav_file.setnchannels(1) # 单声道
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(audio_data_int.tobytes())

print(f"文件已生成： {output_file}")
