from mingus.containers import NoteContainer 
import mingus.core.diatonic as diatonic
import mingus.core.progressions as progressions

#rules for synth part:
#Runs always n 4/4
#if pattern hits chord with pattern
#alternates between arpegiation and chords
#sticks to major chord progressions
#switches up tempo sometimes
#randomizes
#ends on arpegiation of starting note and then base note of key


n = NoteContainer(['C','E','F','G'])

class synth_Constructor(object):
	def __init__(self,notes,bpm):
		self.notes = notes
		self.bpm=bpm
		self.key = key_decider()
		self.chord_dict = chord_dict_decider()

	def key_decider(self):
		#implement key detection algorithim
		#return key
		return 'C-5'
	def chord_dict_decider(self):

