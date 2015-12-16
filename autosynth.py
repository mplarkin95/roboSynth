from mingus.containers import NoteContainer, Note
import mingus.core.progressions as progressions
import mingus.core.intervals as intervals
import random
from scipy.stats import pearsonr as correlation_coefficient
#rules for synth part:
#Runs always n 4/4
#if pattern hits chord with pattern
#alternates between arpegiation and chords
#sticks to major chord progressions
#switches up tempo sometimes
#randomizes
#ends on arpegiation of starting note and then base note of key

chords = {'C':['C','Dm','Em','F','G','Am','Bdim'],
'C#':['C#','D#m','E#m','F#','G#','A#m','B#dim'],
'D':['D','Em','F#m','G','A','Bm','C#dim'],
'D#':['D#','E#m','Gm','G#','A#','B#m','Ddim'],
'E':['E','F#m','G#m','A','B','C#m','D#dim'],
'F':['F','Gm','Am','Bb','C','Dm','Edim'],
'F#':['F#','G#m','A#m','B','C#','D#m','Fdim'],
'G':['G','Am','Bm','C','D','Em','F#dim'],
'G#':['G#','A#m','Cm','C#','D#','Fm','Gdim'],
'A':['A','Bm','C#m','D','E','F#m','G#dim'],
'A#':['A#','Cm','Dm','D#','F','Gm','Adim'], 	
'B':['B','C#m','D#m','E','F#','G#m','A#dim']}

weights = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39,3.66, 2.29, 2.88]

class synth_Constructor(object):
	def __init__(self,bpm):
		self.bpm=bpm
		self.key = 'None'
		self.chord_prog = []
		self.previous_chords = []
		self.position = 0
	def key_decider(self,notes):
		greatest_r = 0
		for x in sorted(chords.iterkeys()):
			cur_r = correlation_coefficient(weights,notes)[0]
			if cur_r > greatest_r:
				greatest_r = cur_r
			 	decided_key = x
			notes = notes[1:]+notes[:1]
		return decided_key
	def chord_prog_decider(self):
		return chords[self.key]
	def update(self,notes):
		cur_key = self.key
		self.key=self.key_decider(notes)
		if self.key != cur_key:
			self.chord_prog = self.chord_prog_decider()
			self.previous_chords = []

	def player(self):
		if self.position >= len(self.previous_chords):
			self.position = 0
		if len(self.previous_chords) < 8:
			r = random.randint(0,6)
			self.previous_chords.append(self.chord_prog[r])
			return self.chord_prog[r]
		else:
			self.position +=1
			return self.previous_chords[self.position-1]


if __name__ == '__main__':
	s = synth_Constructor(120)
	n = [0,191,1,432,231,0,405,12,316,4,126,612]
	s.update(n)
