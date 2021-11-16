import pyttsx3
import time
def speak(text):
	engine = pyttsx3.init()
	# voices = engine.getProperty('voices')   // 可以设置音色的 0 男，1女，2,3隐藏角色，具体情况打印voices便知
	# engine.setProperty('voice', voices[0].id)
	engine.say(text)
	engine.runAndWait()
	engine.stop()

if __name__ == "__main__":
	for i in range(10):
		speak(f"第{i}步，干什么")
		time.sleep(1)
