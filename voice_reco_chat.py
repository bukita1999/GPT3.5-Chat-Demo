import speech_recognition as sr
import openai
import sounddevice as sd
import numpy as np
import pyttsx3

# 初始化GPT-3.5 API客户端
openai.api_key = "xxx"

# 初始化语音识别器
recognizer = sr.Recognizer()

# 初始化TTS引擎
engine = pyttsx3.init()

# 定义提示音函数
def play_sound(start=True):
    frequency = 440  # 频率（赫兹）
    duration = 0.5  # 持续时间（秒）
    samplerate = 44100  # 采样率
    t = np.linspace(0, duration, int(samplerate * duration))
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    if not start:
        wave = 0.5 * np.sin(2 * np.pi * (frequency // 2) * t)
    sd.play(wave, samplerate)
    sd.wait()

while True:
    # 使用麦克风捕获音频
    with sr.Microphone() as source:
        print("语音识别中...")
        play_sound(start=True)  # 开始录音提示音
        audio_data = recognizer.listen(source)
        play_sound(start=False)  # 结束录音提示音

        try:
            # 使用Google语音识别
            text = recognizer.recognize_google(audio_data, language='zh-CN')
            print(f"你说的是：{text}")

            print("GPT-3.5思考中...")
            # 使用GPT-3.5 API进行回答
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # 确保模型名称正确
                messages=[
                    {"role": "system", "content": 
                        "你是一名万能的帮手，我希望你对我的任何回答用一句简短的话来回答。由于我是语音输入，有时候会被截断话语，请你考虑到这样的情况猜测我可能想讲的全部内容。"},
                    {"role": "user", "content": text}
                ]
            )
            answer = response['choices'][0]['message']['content'].strip()
            
            print(f"GPT-3.5的回答：{answer}")

            # 使用TTS读出GPT-3.5的回答
            engine.say(answer)
            engine.runAndWait()

            # 等待用户输入以继续
            user_input = input("输入'y'以继续，其他键退出：")
            if user_input.lower() != 'y':
                break
            
        except sr.UnknownValueError:
            print("无法识别音频")
        except sr.RequestError as e:
            print(f"语音识别请求失败; {e}")
