import wave
import numpy as np
from scipy.fft import fft, fftfreq

filename = 'mystery_sound.wav'
sum = ''
with wave.open(filename, 'rb') as wf:
    sample_rate = wf.getframerate()
    num_frames = wf.getnframes()
    audio_data = np.frombuffer(wf.readframes(num_frames), dtype=np.int16)


duration_per_segment = 0.7 # 每段1秒
samples_per_segment = int(sample_rate * duration_per_segment)

# 分段分析
num_segments = len(audio_data) // samples_per_segment

for i in range(num_segments):
    segment = audio_data[i * samples_per_segment : (i + 1) * samples_per_segment]

    # 执行FFT
    fft_result = np.abs(fft(segment))
    freqs = fftfreq(len(segment), d=1/sample_rate)

    # 取正频率部分
    positive_freqs = freqs[:len(freqs)//2]
    positive_magnitudes = fft_result[:len(fft_result)//2]

    # 找到最大频率成分
    peak_freq = positive_freqs[np.argmax(positive_magnitudes)]

    if peak_freq < 20:
        sum = sum+'0'
        print(f'第{i + 1}段: 主频率 = {peak_freq:.2f} Hz → bit = 0')
    elif peak_freq > 20000:
        sum = sum+'1'
        print(f'第{i + 1}段: 主频率 = {peak_freq:.2f} Hz → bit = 1')
    else:
        print(f'第{i + 1}段: 主频率 = {peak_freq:.2f} Hz → bit = ?')


print(sum)
print(len(sum))