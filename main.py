import synthPlayer, autosynth
import threading
import time, Queue, random
from mingus.containers import NoteContainer 
import listener


class synthThread(threading.Thread):
	def run(self):
		p = synthPlayer.player('piano.SF2',bpm) #initialize synthplayer Object
		while True:
			if not play.empty():  #check play queue from updates from synthesizer
				item = play.get() #find oldest item in queue and process
				if item == "Kill": #kill ends loop
					break
				if item[0]== "chord":  #play a chord using list in queue as arguments
					p.play_chord(item[1],item[2],item[3])
				elif item[0]== "arp": #play an arpeggio using list in queue as arguments
					p.arpegiate_chord(item[1],item[2],item[3])
		return

class autoSynthThread(threading.Thread):
	def run(self):
		sound = "chord" #default arguments for player
		time = .5
		note = "C"
		vel = 120
		a_sy = autosynth.synth_Constructor(bpm) #initialize synth automoton
		while True:
			if not action.empty():
				item = action.get()
				if item == "Kill":
					play.put("Kill")
					break
				a_sy.update(item) #whenever there is an update of sounds update key and then return sound
				t = random.randint(0,10)  #generate random int to see if chord is arpegiated
				if t==7 or t==3:
					sound = "arp"
					time = .5/4
				else:
					sound = 'chord'
					time = .5
				note = a_sy.player()
				play.put([sound,time,note,vel]) #call actual player function
				if sound=='arp':
					sound = 'chord'
					time = .5/4
					play.put([sound,time,note,vel])

				


if __name__ == '__main__':
	print "Testing module"
	bpm = int(raw_input("enter bpm: "))
	play = Queue.Queue()  #initialize queues
	action = Queue.Queue()
	c1 = autoSynthThread()
	c2 = synthThread()
	c3 = listener.listenerThread()
	c3.start() #start threads
	c2.start()
	c1.start()

	
