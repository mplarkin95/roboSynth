from mingus.containers import Note, NoteContainer
from mingus.midi import fluidsynth as synth
import time



class player(object):
	'''Synthesizer player'''
	#Implement note duration dictionary
	def __init__(self,sf_file,bpm):
		synth.init(sf_file,"alsa")
		self.bpm = float(bpm)
		self.me_time = (bpm/60)*4
	def play_chord(self,note_length,chord):
		synth.play_NoteContainer(NoteContainer().from_chord(chord))
		time.sleep(self.me_time*note_length)
	def arpegiate_chord(self,note_length,chord):
		for x in NoteContainer().from_chord(chord):
			synth.play_Note(x)
			time.sleep(self.me_time*note_length)
	def play_note(self,note_length,note):
		synth.play_Note()
		time.sleep(self.me_time*note_length)



p = player('piano.SF2',60)

p.play_chord(.25,"G")
p.play_chord(.25/2,"C")
p.play_chord(.25/2,"A")
p.play_chord(.25,"F")
p.play_chord(.25,"C")
p.arpegiate_chord(.5/3, "A")
p.play_chord(.5,"C")

