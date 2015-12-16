import synthPlayer, autosynth
import threading
import time, Queue, random
from mingus.containers import NoteContainer 
import listener
import pyaudio
import analyse
import numpy


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
		CHUNK = 1024
		FORMAT = pyaudio.paInt16
		CHANNELS = 1
		RATE = 22400

		midi_dict = {0:'C', 1:'C#', 2:'D', 3:'D#', 4:'E', 5:'F', 6:'F#', 7:'G', 8:'G#', 9:'A', 10:'A#', 11:'B',
					12:'C', 13:'C#', 14:'D', 15:'D#', 16:'E', 17:'F', 18:'F#', 19:'G', 20:'G#', 21:'A', 22:'A#', 23:'B',
					24:'C', 25:'C#', 26:'D', 27:'D#', 28:'E', 29:'F', 30:'F#', 31:'G', 32:'G#', 33:'A', 34:'A#', 35:'B',
					36:'C', 37:'C#', 38:'D', 39:'D#', 40:'E', 41:'F', 42:'F#', 43:'G', 44:'G#', 45:'A', 46:'A#', 47:'B',
					48:'C', 49:'C#', 50:'D', 51:'D#', 52:'E', 53:'F', 54:'F#', 55:'G', 56:'G#', 57:'A', 58:'A#', 59:'B',
					60:'C', 61:'C#', 62:'D', 63:'D#', 64:'E', 65:'F', 66:'F#', 67:'G', 68:'G#', 69:'A', 70:'A#', 71:'B',
					72:'C', 73:'C#', 74:'D', 75:'D#', 76:'E', 77:'F', 78:'F#', 79:'G', 80:'G#', 81:'A', 82:'A#', 83:'B',
					84:'C', 85:'C#', 86:'D', 87:'D#', 88:'E', 89:'F', 90:'F#', 91:'G', 92:'G#', 93:'A', 94:'A#', 95:'B',
					96:'C', 97:'C#', 98:'D', 99:'D#', 100:'E', 101:'F', 102:'F#', 103:'G', 104:'G#', 105:'A', 106:'A#', 107:'B',
					108:'C', 109:'C#', 110:'D', 111:'D#', 112:'E', 113:'F', 114:'F#', 115:'G', 116:'G#', 117:'A', 118:'A#', 119:'B',
					 120:'C', 121:'C#', 122:'D', 123:'D#', 124:'E', 125:'F', 126:'F#', 127:'G'}
		notes_array = [0,0,0,0,0,0,0,0,0,0,0,0]
		note_count = 0
		step_count = 0
		player_delay =  False
		sound = "chord" #default arguments for player
		time = .5
		note = "C"
		vel = 120
		a_sy = autosynth.synth_Constructor(bpm) #initialize synth automoton
		p = pyaudio.PyAudio()

		stream = p.open(format=FORMAT,   #open stream 
						channels=CHANNELS,
						rate=RATE,
						input=True)
		while True:

			rawsamps = stream.read(CHUNK) #read chunk of data into string of sound input
			samps = numpy.fromstring(rawsamps, dtype=numpy.int16) #convert to numpy interger

			midi = analyse.musical_detect_pitch(samps)  #find associated midi pitch and therefore note
			step_count+=1
			if midi is not None:
				note =  midi_dict[int(midi)] #pull note from dictionary and update note array
				print note
				if note == 'A':notes_array[0]+=1
				if note =='A#':notes_array[1]+=1
				if note == 'B':notes_array[2]+=1
				if note == 'C':notes_array[3]+=1
				if note =='C#':notes_array[4]+=1
				if note == 'D':notes_array[5]+=1
				if note == 'D#':notes_array[6]+=1
				if note == 'E':notes_array[7]+=1
				if note == 'F':notes_array[8]+=1
				if note == 'F#':notes_array[9]+=1
				if note == 'G':notes_array[10]+=1
				if note == 'G#':notes_array[11]+=1
				note_count+= 1
			if note_count == 35 or (step_count==50 and player_delay):  #after 50 note samples return array for key recognitions	
				step_count=0
				if note_count == 35:
					a_sy.update(notes_array) #whenever there is an update of sounds update key and then return sound
					note_count=0
					player_delay = True
				t = random.randint(0,5)  #generate random int to see if chord is arpegiated
				if t==3:
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
	c2.start()
	c1.start()

	
