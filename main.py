import synthPlayer 
import threading
import time, Queue, random
from mingus.containers import NoteContainer 


class synthThread(threading.Thread):
	def run(self):
		p = synthPlayer.player('piano.SF2',bpm)
		while True:
			if not play.empty():
				item = play.get()
				if item == "Kill":
					break
				if item[0]== "chord":
					p.play_chord(item[1],item[2],item[3])
				elif item[0]== "note":
					p.play_note(item[1],item[2],item[3])
				elif item[0]== "arp":
					p.arpegiate_chord(item[1],item[2],item[3])
		return

class autoSynthThread(threading.Thread):
	def run(self):
		sound = "chord"
		time = .5
		note = "C"
		vel = 120

		chords = ["C","Am","G","F"]

		while True:
			if not action.empty():
				item = action.get()
				ch = random.randint(0,3)
				t = random.randint(0,10)
				if t==7 or t==3:
					sound = "arp"
					time = .5/3
				else:
					sound = 'chord'
					time = .5
				note=chords[ch]
				play.put([sound,time,note,vel])
				print sound+ " :"+ note
				if sound=='arp':
					sound = 'chord'
					time = .5
					play.put([sound,time,note,vel])
				


	

if __name__ == '__main__':
	bpm = int(raw_input("enter bpm: "))
	play = Queue.Queue()
	action = Queue.Queue()
	c1 = autoSynthThread()
	c2 = synthThread()
	c2.start()
	c1.start()

	for x in range(0,1):
		print int(x)
		action.put(x)
		time.sleep(.5)

	play.put(['chord',1,NoteContainer().from_chord('C'),120])