import mido
import time
import math
import argparse
from itertools import tee, islice, chain

#The numbers are the notes according to general midi
class DrumNotes:
	purpleNote = 65
	greenNote = 64
	redNote = 63
	yellowNote = 62
	blueNote = 61
	orangeNote = 60

def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(prevs, items, nexts)

def get_color_note(midi_note):
	match midi_note:
		case DrumNotes.purpleNote:
			return 4
		case DrumNotes.greenNote:
			return 6
		case DrumNotes.redNote:
			return 2
		case DrumNotes.yellowNote:
			return 1
		case DrumNotes.blueNote:
			return 5
		case DrumNotes.orangeNote:
			return 3

def convert_midi(midi):
	print("Converting midi...")
	#Set up variables to be used
	currentTime = 0
	previousTime = 1
	bpm = 0
	quarter_note_duration = 0
	drumroll = False
	noteCount = ""
	enemyType = 1
	auxColor1 = 0
	auxColor2 = 0
	aux = 0
	doubleNote = False

	#Create file and name it the same as the midi file but with .csv instead
	with open(".".join(cmd_args.midi.split(".")[:-1])+".csv", "a") as csvFile:

		#First row
		csvFile.write("Time [s],Enemy Type,Aux Color 1,Aux Color 2,Nº Enemies,interval,Aux\n")

		for previousMsg, msg, nxtMsg in previous_and_next(midi):
			currentTime += msg.time

			#Check for tempo changes
			if msg.is_meta:
				if msg.type == 'set_tempo':
					bpm = mido.tempo2bpm(msg.tempo)
				continue
			#If we detected a double note in the previous loop, then skip this one.
			if doubleNote:
				doubleNote = False
				continue

			#Check if a long note is longer than a quarter note
			if nxtMsg.type == 'note_off':
				if nxtMsg.time > 60.0 / bpm / 4:
					drumroll = True


			if msg.type == 'note_on':
				#If we have detected a drumroll then check how high the fat demon has to be
				if drumroll:
					enemyType = 3
					quarter_note_duration = 60.0 / bpm / 4
					noteCount = int(math.floor(nxtMsg.time // quarter_note_duration + 1))
					print(noteCount)
					drumroll = False

				#If in the next loop the delta time is 0, then assume it is a double note
				if nxtMsg.time == 0:
					enemyType = 2
					auxColor2 = get_color_note(nxtMsg.note)
					doubleNote = True

				auxColor1 = get_color_note(msg.note)

				if doubleNote == False:
					auxColor2 = get_color_note(msg.note)

				#Sort the colors the right way. 
				if auxColor2 < auxColor1:
					temp = auxColor1
					auxColor1 = auxColor2
					auxColor2 = temp

				#No idea what aux is for(Probably position of double notes when the notes are sticky), but in the excel sheet this is the right order
				match auxColor1:
					case 2:
						aux = 7
					case 1:
						aux = 6
					case 5:
						aux = 5
					case 3:
						aux = 5
					case 6:
						aux = 8
					case 4:
						aux = 8
				csvFile.write("{0},{1},{2},{3},1,{4},{5}\n".format(math.floor(currentTime * 100) / 100.0, enemyType, auxColor1, auxColor2, noteCount, aux))

				noteCount = ""
				enemyType = 1

			previousTime = currentTime
		print("Finished")

#Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("midi", help="The midi file to be converted")

cmd_args = parser.parse_args()

convert_midi(mido.MidiFile(cmd_args.midi))