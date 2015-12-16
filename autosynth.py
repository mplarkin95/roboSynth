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
		greatest_r = 0  #pearson coefficient for use in the Krumhansl-Schmuckler key finding algorithim
		for x in sorted(chords.iterkeys()): #iterate through possible keys
			cur_r = correlation_coefficient(weights,notes)[0]
			if cur_r > greatest_r: 
				greatest_r = cur_r
			 	decided_key = x
			notes = notes[1:]+notes[:1] #change the notes array to shift all notes down one for next key
		return decided_key
	def chord_prog_decider(self):
		return chords[self.key] #call dictionary of chords in a key
	def update(self,notes):
		cur_key = self.key
		self.key=self.key_decider(notes) #update key
		print self.key
		if self.key != cur_key:   #if key is updated forget previous chord progression
			self.chord_prog = self.chord_prog_decider()
			self.previous_chords = []
			print 'Key change'

	def player(self):
		if self.position >= len(self.previous_chords):  #if at end of chord progression start from beggining
			self.position = 0
		if len(self.previous_chords) < 8:  #create an 8 chord progression
			r = random.randint(0,15)
			if r>=0 and r<=4:r= 0
			elif r>4 and r<=5:r=1
			elif r>5 and r<=7:r=2
			elif r>7 and r<=10:r=3
			elif r>10 and r<=13:r=4
			elif r>13 and r<=14:r=5
			elif r>14 and r<=15:r=6 
			self.previous_chords.append(self.chord_prog[r])
			return self.chord_prog[r]
		else:
			self.position +=1
			return self.previous_chords[self.position-1]


if __name__ == '__main__':
	print 'Testing'
	s = synth_Constructor(120)
	n = [0,191,1,432,231,0,405,12,316,4,126,612]  #key of G#
	s.update(n)
