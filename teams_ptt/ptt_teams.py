from pynput.keyboard import Key, Listener
from playsound import playsound
import subprocess
import os

#pactl list source-outputs

id = 0

def get_id():
	result = subprocess.run(['pactl', 'list', 'source-outputs'], stdout=subprocess.PIPE)
	out = result.stdout.decode('utf-8')
	sepa = out.split("\n")
	indices = [i for i, s in enumerate(sepa) if 'WEBRTC VoiceEngine' in s]
	id = int(sepa[indices[0]-17].split()[2][1:])

	return id

def on_press(key):
	k = '{0}'.format(key)
	if(k == 'Key.shift_r'):
		os.system("pactl set-source-output-mute "+str(get_id())+" no")
		playsound('ptt-activate.mp3')
		#print("ON")

def on_release(key):
	k = '{0}'.format(key)
	if(k == 'Key.shift_r'):
		os.system("pactl set-source-output-mute "+str(get_id())+" yes")
		playsound('ptt-deactivate.mp3')
		#print("RELEASED")
	if key == Key.esc:
		# Stop listener
		return False

os.system("pactl set-source-output-mute "+str(get_id())+" yes")

# Collect events until released
with Listener(
		on_press=on_press,
		on_release=on_release) as listener:
	print("Started")
	listener.join()