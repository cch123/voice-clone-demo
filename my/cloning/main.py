import pyaudio
import wave

# 配置录音参数
chunk = 1024  # 块大小
sample_format = pyaudio.paInt16  # 采样位数
channels = 1  # 声道数
sample_rate = 16000  # 采样率

# 初始化 PyAudio
p = pyaudio.PyAudio()

# 开始录音
print('开始录音...')
stream = p.open(format=sample_format,
                channels=channels,
                rate=sample_rate,
                frames_per_buffer=chunk,
                input=True)

frames = []

# 录音持续时间（秒）
recording_time = 10

for i in range(0, int(sample_rate / chunk * recording_time)):
    data = stream.read(chunk)
    frames.append(data)

# 停止录音
print('录音结束.')
stream.stop_stream()
stream.close()
p.terminate()

# 保存录音文件
wf = wave.open('audio.wav', 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(sample_rate)
wf.writeframes(b''.join(frames))
wf.close()
