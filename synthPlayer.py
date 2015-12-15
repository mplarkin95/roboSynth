from mingus.containers import Note, NoteContainer
from mingus.midi import fluidsynth as synth
import time



class player(object):
	'''Synthesizer player
		Uses Chord names as depicted by mingus for chord playing and iterates through chords for arpegiation
		2 methods: one for arpegiation and one for classic chord playing takes same arguments: 
		Length of note(decimal in terms of part of the measure), chord name (use mingus notation),velocity (volume),
		arpegiation has an extra optional argument ascending=False which when True increments velocity of each note in the 
		arpeggio '''
	def __init__(self,sf_file,bpm):
		synth.init(sf_file,"alsa") #initialize synth module from Mingus with soundfont file and alsa as default
		self.bpm = float(bpm)
		self.me_time = float(240/bpm)  #Set the time in seconds that each measure in 4/4 time takes
	def play_chord(self,note_length,chord,velocity):
		synth.play_NoteContainer(NoteContainer().from_chord(chord),velocity=velocity) #if it is not create chord from string
		time.sleep(self.me_time*note_length)
	def arpegiate_chord(self,note_length,chord,velocity,ascending=False):
		chord = NoteContainer().from_chord(chord)
		for x in chord:
			synth.play_Note(x,velocity=velocity)
			time.sleep(self.me_time*note_length)
			if ascending:
				velocity += 15


#TESTING
# p = player('piano.SF2',60)
# for x in range(0,5):
# 	p.play_chord(.25,"G",(50+x*10))
# 	p.play_chord(.25/2,"C",(50+x*10))
# 	p.play_chord(.25/2,"C",(50+x*10))
# p.play_chord(.25,"G",100)
# p.play_chord(.25,"C",120)
# p.arpegiate_chord(.5/3, "G",75,ascending=True)
# p.play_chord(.5,"C",120)
# time.sleep(2)

