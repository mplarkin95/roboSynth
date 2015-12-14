from mingus.containers import NoteContainer


#rules for synth part:
#Runs always n 4/4
#alternates between arpegiation and chords
#sticks to major chord progressions
#switches up tempo sometimes
#randomizes
#ends on arpegiation of starting note and then base note of key


n = NoteContainer(['C','E','F','G'])

print n.determine(True)

