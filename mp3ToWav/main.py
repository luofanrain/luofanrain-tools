from pydub import AudioSegment
import wave
import io
 
if __name__ == "__main__":
    # 先从本地获取 mp3 的 bytestring 作为数据样本
    filename = "b.mp3"
    fp=open(filename, 'rb')
    data=fp.read()
    fp.close()
    # 读取
    aud=io.BytesIO(data)
    sound=AudioSegment.from_file(aud, format='mp3')
    raw_data = sound._data
    
    # 写入到文件
    l=len(raw_data)
    f = wave.open(filename + ".wav",'wb')
    f.setnchannels(1)
    f.setsampwidth(2)
    setframerate(8000)
    f.setnframes(l)
    f.writeframes(raw_data)
    f.close()