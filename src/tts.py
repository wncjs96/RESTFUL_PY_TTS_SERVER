from gtts import gTTS 
from time import sleep

import os 
import random
import sys
import threading
import re
import pathlib
import pygame
import mutagen.mp3
#import pyglet

# Avoid globals, all variables defined on the class lvl in python are considered static.
#global switch
#switch = 1

class ST1:
	#player = pyglet.media.Player()
	switch = 0
	mode = -1
	rand = 0

instance = ST1()

def clear():
	tts = gTTS(text="temp", lang=language, slow=False)
	tts.save("JunkFile")
	pygame.mixer.music.load("JunkFile")
	pygame.mixer.music.play(0)
	pygame.mixer.music.stop()
	clearfiles()
	instance.rand = 0

def clearfiles():
	curr = str(pathlib.Path().absolute())
	
	# w/o extension
	#regex = re.compile('temp(\d)*')
	# w/ extension
	
	regex = re.compile('temp(\d)*\.(.)*')
	
	if instance.switch == 0:
		for root,dirs,files in os.walk(curr):
			for file in files:
				#print(file)
				if regex.match(file):
					#print(file)
					os.unlink(file)


def playsound(filename):
	lock.acquire()
	instance.switch = instance.switch + 1
	#filename = 'CantinaBand60.wav'

	#player = pyglet.media.Player()
	#src = pyglet.media.load(filename)
	#player.queue(src)
	#player.play()	
	#print("duration : "+str(src.duration))
	#sleep(src.duration)
	#player.delete()
	#pyglet.app.exit
	#player = None
	#instance.switch = 0
	#if (instance.mode == 1) :
	#	print("mode 1 activated")
	#	pygame.mixer.init(44000)	
	#elif (instance.mode == 2) :
	#	print("mode 2 activated")
	#	pygame.mixer.init(24000)
	#elif (instance.mode == 3) :
	#	print("mode 3 activated")
	#	pygame.mixer.init(32000)
	
	pygame.mixer.music.load(filename)
	pygame.mixer.music.play(0)
	#pygame.mixer.music.stop()
	instance.switch = instance.switch - 1
	lock.release()

clearfiles()
#random.seed(a=None, version=2)
#rand = random.randint(0, 50000)
instance.rand = 0

random.seed(a=None, version=2)
rand2 = random.randint(0, 20)


# The text that you want to convert to audio 
language = 'ko'
#curr = str(pathlib.Path().absolute())
#print("curr : "+ curr)

lock = threading.Lock()

print(instance.switch)

#mytext = '간장공장공장장은긴공장장안깐꽁깎지'
#tts = gTTS(text=mytext, lang=language, slow=False) 
#filename = 'temp' + str(rand) + '.mp3'
#tts.save(filename) 
#playsound(filename)

song_file = "welcome.mp3"
#song_file = "Positive_Win_Game_Sound_4.mp3"
mp3 = mutagen.mp3.MP3(song_file)

#pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init(mp3.info.sample_rate)
#pygame.mixer.init(44100)
print(mp3.info.sample_rate)
#pygame.mixer.quit()


while 1:
	mytext = sys.stdin.readline()
	if mytext == "\n" :
		continue
	
	if mytext == "exit\n" or mytext == "ff\n" :
		print("exit enabled")
		exit()

	if mytext == "mode 1\n" :
		print("mode 1 activated")
		#pygame.mixer.quit()
		sleep(1)
		#pygame.mixer.pre_init(frequency=44100)
		#pygame.mixer.init(44100)
		instance.mode = 1
		continue	

	if mytext == "mode 2\n" :
		print("mode 2 activated")
		#pygame.mixer.quit()
		sleep(1)
		#pygame.mixer.pre_init(frequency=32000)
		#pygame.mixer.init(32000)
		instance.mode = 2	
		continue

	if mytext == "mode 3\n" :
		print("mode 3 activated")
		#pygame.mixer.quit()
		sleep(1)
		#pygame.mixer.pre_init(frequency=32000)
		#pygame.mixer.init(24000)
		instance.mode = 3
		continue
	if mytext == "mode 0\n" :
		print("Default")
		sleep(1)
		instance.mode = 0
		continue
	if mytext == "playmode\n":
		print("Play a song from your directory (regex applied)")	
		sleep(1)
		instance.mode = 4
		continue
	
	curr = str(pathlib.Path().absolute())
	regex2 = re.compile(mytext.rstrip()+'(.)*')
	if (instance.mode == 4):
		found = 0
		for root,dirs,files in os.walk(curr):
			for file in files:
				#print(file)
				if regex2.match(file):
					#print(file)
					filename = file
					print("Playing file : " + file)
					found = 1
					y = threading.Thread(target = playsound, args=(filename,))
					y.start()
		if found == 0:
			print("Couldn't find the file")
		continue

	#print (instance.switch)
	if mytext == "clear\n" :
		clear()
		continue

#	if instance.switch == 0:
#		for root,dirs,files in os.walk(curr):
#			for file in files:
#				#print(file)
#				if regex.match(file):
#					#print(file)
#					os.unlink(file)
#
	#lock.acquire()
	if (instance.mode == 3):
		mytext = "만세! 회원님의 " + str(rand2) + "개월 구독을 알리세요."

	tts = gTTS(text=mytext, lang=language, slow=False) 
	
	# Saving the converted audio in a mp3 file
	filename = 'temp' + str(instance.rand) + '.mp3'
	tts.save(filename) 
	instance.rand = instance.rand + 1
	#lock.release()
	#playsound(mytext)
	
	if instance.mode == 1:
		print(instance.mode)	
		pygame.mixer.music.load('The_award.wav')
		pygame.mixer.music.play(0)
		sleep(3)

	elif instance.mode == 2:
		print(instance.mode)	
		pygame.mixer.music.load('Coins.wav')
		pygame.mixer.music.play(0)
		sleep(3)

	elif instance.mode == 3:
		print(instance.mode)	
		pygame.mixer.music.load('Positive_Win_Game_Sound_4.wav')
		pygame.mixer.music.play(0)
		sleep(3)
	
	y = threading.Thread(target = playsound, args=(filename,))
	y.start()
	if instance.rand == 5:
		clear()
