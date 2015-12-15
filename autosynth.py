from mingus.containers import NoteContainer 
import mingus.core.progressions as progressions
import mingus.core.intervals as intervals
import random
#rules for synth part:
#Runs always n 4/4
#if pattern hits chord with pattern
#alternates between arpegiation and chords
#sticks to major chord progressions
#switches up tempo sometimes
#randomizes
#ends on arpegiation of starting note and then base note of key

chords = {'C':['C','Dm','Em','F','G','Am','Bdim'],
'D':['D','Em','F#m','G','A','Bm','C#dim'],
'E':['E','F#m','G#m','A','B','C#m','D#dim'],
'F':['F','Gm','Am','Bb','C','Dm','Edim'],
'G':['G','Am','Bm','C','D','Em','F#dim'],
'A':['A','Bm','C#m','D','E','F#m','G#dim'],
'B':['B','C#m','D#m','E','F#','G#m','A#dim']}

class synth_Constructor(object):
	def __init__(self,notes,bpm):
		self.notes = notes
		self.bpm=bpm
		self.key = 'C'
		self.chord_prog = self.chord_prog_decider()
		self.previous_chords = list()
		self.position = 0
	def key_decider(self):
		#implement key detection algorithim
		#return key
		return 'C'
	def chord_prog_decider(self):
		
		return chords[self.key]
	def update(self):
		cur_key = self.key
		self.key=self.key_decider()
		if self.key != cur_key:
			self.chord_prog = self.chord_prog_decider()

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
	s = synth_Constructor('C',120)
	print s.chord_prog[1]
