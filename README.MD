---
A script to convert prepared MIDI files to .csv to support custom songs in Drums Rock

---
# Requirements:
* Python 3.10 or newer
* A DAW or Midi editor (FL Studio is used in the examples)
* Mido python package (`python -m pip install mido`)

# How to use:
`python drumsrockparser.py midifile.mid`


---
# Instructions:
1. If using FL Studio, download drumsrocktemplate.flp and open it. For any other method, adapt the instructions appropriately
2. Move the sound file you want to use to the playlist view
![Image](/instructions/1.png)
3. Adjust the BPM
![Image](/instructions/2.png)
4. Adjust the sound file using the cutting tool in playlist view so that it lines up with the bars in the background
5. Click on the piano roll to start making your own chart
![Image](/instructions/3.png)
7. After you are finished making it, make sure you have saved the file.
8. First go to Tools > Macros Prepare for MIDI export. Then Go to File > Export > MIDI File.
(If your chart does not contain any tempo changes, then you can also export the midi directly from the piano roll. Press the dorito next to the wrench, and then File > Export as MIDI File).
![Image](/instructions/4.png)
9. Make sure to select Full song and not pattern (this is especially important if your chart has variable bpm)
10. Now open the command line in the same folder as the script.
11. Type in `python drumsrockparser.py yourmidifile.mid`
![Image](/instructions/5.png)
12. Your .csv file is now done. Follow the [official instructions](https://garage51.es/drumsrock/custom_songs.html) on how to set it up in the game

# How to do drumrolls
In order to do drum rolls, you have to extend the note so that it becomes longer than 1 quarter note. I advise to put the note over the lines to make sure the script recognises it as a drumroll
![Image](/instructions/6.png)

# TO DO:
* Implement time signature changes for drumrolls.
