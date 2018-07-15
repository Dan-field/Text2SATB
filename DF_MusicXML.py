####################################################################
# DF_MusicXML class by Daniel Field                                #
#                                                                  #
# This class handles the creation and appending of a MusicXML file #
#                                                                  #
# check out www.github.com/dan-field/Text2SATB for info and rights #
####################################################################
from DF_MIDINumbers import *

class DF_MusicXML:
   def __init__(self, usrTitle=None, progID=None):
      """Initialises a DF_MusicXML object"""
      if usrTitle is None:
         self.Title = "Sonification"
      else:
         self.Title = "Sonification: "+str(usrTitle)
      if progID is None:
         self.progID = "Dan Field's Sonifier v 0.1"
      else:
         self.progID = progID
      self.MIDI = DF_MIDINumbers()
      self.DIVISIONS = 4
      self.measureNo = 0
      self.voice = 1 # 1 Soprano, 2 Alto, 3 Tenor, 4 Bass
      self.flats = True # assumes black notes should be written as flats - will need to be updated once a 'key' functionality is added
      usrFileName = raw_input("please enter a name for the output file: ")
      self.fileName = usrFileName+".musicxml"
      try:
         self.file = open(self.fileName, "w")
      except IOError:
         self.file = None
         print "\nThere was an issue with the file operation."
         print "Please double-check your filename.\n"
         print "Note the MusicXML file will attempt to save in the"
         print "same folder as the Python files; please ensure you"
         print "have write permission for that folder."
         return
      self.file.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
      self.file.write('<!DOCTYPE score-partwise PUBLIC\n')
      self.file.write('     "-//Recordare//DTD MusicXML 3.1 Partwise//EN"\n')
      self.file.write('     "http://www.musicxml.org/dtds/partwise.dtd">\n')
      self.file.write('<score-partwise version="3.1">\n')
      self.file.write('  <work>\n')
      self.file.write('    <work-title>'+str(self.Title)+'</work-title>\n')
      self.file.write('  </work>\n')
      self.file.write('  <identification>\n')
      self.file.write('    <creator type="composer">'+str(self.progID)+'</creator>\n')
      self.file.write('  </identification>\n')
      self.file.write('  <part-list>\n')
      self.file.write('    <score-part id="P1">\n')
      self.file.write('      <part-name>Soprano</part-name>\n')
      self.file.write('    </score-part>\n')
      self.file.write('    <score-part id="P2">\n')
      self.file.write('      <part-name>Alto</part-name>\n')
      self.file.write('    </score-part>\n')
      self.file.write('    <score-part id="P3">\n')
      self.file.write('      <part-name>Tenor</part-name>\n')
      self.file.write('    </score-part>\n')
      self.file.write('    <score-part id="P4">\n')
      self.file.write('      <part-name>Bass</part-name>\n')
      self.file.write('    </score-part>\n')
      self.file.write('  </part-list>\n')

   def startSoprano(self):
      if self.file is not None:
         self.measureNo = 0
         self.voice = 1
         self.file.write('  <part id="P1">\n')
         self.file.write('    <measure number="'+str(self.measureNo)+'">\n')
         self.file.write('      <attributes>\n')
         self.file.write('        <divisions>'+str(self.DIVISIONS)+'</divisions>\n')
         self.file.write('        <key>\n')
         self.file.write('          <fifths>0</fifths>\n')
         self.file.write('        </key>\n')
         self.file.write('        <time>\n')
         self.file.write('          <beats>4</beats>\n')
         self.file.write('          <beat-type>4</beat-type>\n')
         self.file.write('        </time>\n')
         self.file.write('        <clef number="1">\n')
         self.file.write('          <sign>G</sign>\n')
         self.file.write('          <line>2</line>\n')
         self.file.write('        </clef>\n')
         self.file.write('      </attributes>\n')

   def startAlto(self):
      if self.file is not None:
         self.measureNo = 0
         self.voice = 2
         self.file.write('  <part id="P2">\n')
         self.file.write('    <measure number="'+str(self.measureNo)+'">\n')
         self.file.write('      <attributes>\n')
         self.file.write('        <divisions>'+str(self.DIVISIONS)+'</divisions>\n')
         self.file.write('        <key>\n')
         self.file.write('          <fifths>0</fifths>\n')
         self.file.write('        </key>\n')
         self.file.write('        <time>\n')
         self.file.write('          <beats>4</beats>\n')
         self.file.write('          <beat-type>4</beat-type>\n')
         self.file.write('        </time>\n')
         self.file.write('        <clef number="1">\n')
         self.file.write('          <sign>G</sign>\n')
         self.file.write('          <line>2</line>\n')
         self.file.write('        </clef>\n')
         self.file.write('      </attributes>\n')

   def startTenor(self):
      if self.file is not None:
         self.measureNo = 0
         self.voice = 3
         self.file.write('  <part id="P3">\n')
         self.file.write('    <measure number="'+str(self.measureNo)+'">\n')
         self.file.write('      <attributes>\n')
         self.file.write('        <divisions>'+str(self.DIVISIONS)+'</divisions>\n')
         self.file.write('        <key>\n')
         self.file.write('          <fifths>0</fifths>\n')
         self.file.write('        </key>\n')
         self.file.write('        <time>\n')
         self.file.write('          <beats>4</beats>\n')
         self.file.write('          <beat-type>4</beat-type>\n')
         self.file.write('        </time>\n')
         self.file.write('        <clef number="1">\n')
         self.file.write('          <sign>G</sign>\n')
         self.file.write('          <line>2</line>\n')
         self.file.write('          <clef-octave-change>-1</clef-octave-change>\n')
         self.file.write('        </clef>\n')
         self.file.write('      </attributes>\n')

   def startBass(self):
      if self.file is not None:
         self.measureNo = 0
         self.voice = 4
         self.file.write('  <part id="P4">\n')
         self.file.write('    <measure number="'+str(self.measureNo)+'">\n')
         self.file.write('      <attributes>\n')
         self.file.write('        <divisions>'+str(self.DIVISIONS)+'</divisions>\n')
         self.file.write('        <key>\n')
         self.file.write('          <fifths>0</fifths>\n')
         self.file.write('        </key>\n')
         self.file.write('        <time>\n')
         self.file.write('          <beats>4</beats>\n')
         self.file.write('          <beat-type>4</beat-type>\n')
         self.file.write('        </time>\n')
         self.file.write('        <clef number="1">\n')
         self.file.write('          <sign>F</sign>\n')
         self.file.write('          <line>4</line>\n')
         self.file.write('        </clef>\n')
         self.file.write('      </attributes>\n')

   def endPart(self):
      if self.file is not None:
         self.file.write('    </measure>\n')
         self.file.write('  </part>\n')

   def endXMLFile(self):
      if self.file is not None:
         self.file.write('</score-partwise>\n')
         self.file.close()

   def addMeasure(self):
      if self.file is not None:
         self.file.write('    </measure>\n')
         self.measureNo += 1
         self.file.write('    <measure number="'+str(self.measureNo)+'">\n')

   def addNote(self, MIDI_No, duration=None, lyric=None): # duration: 4 = crotchet, 16 = semi-breve
      if self.file is not None:
         if duration is None:
            duration = 4 # default to a crotchet
         if lyric is None:
            lyric = "" # default to no text
         note_type = self.MIDI.Duration2Type(duration)
         octave, step, alter = self.MIDI.MIDI2Note(MIDI_No, self.flats)
         self.file.write('      <note>\n')
         self.file.write('        <pitch>\n')
         self.file.write('          <step>'+str(step)+'</step>\n')
         if alter != 0:
            self.file.write('          <alter>'+str(alter)+'</alter>\n')
         self.file.write('          <octave>'+str(octave)+'</octave>\n')
         self.file.write('        </pitch>\n')
         self.file.write('        <duration>'+str(duration)+'</duration>\n')
         self.file.write('        <voice>'+str(self.voice)+'</voice>\n')
         self.file.write('        <type>'+str(note_type)+'</type>\n')
         self.file.write('        <lyric>\n')
         self.file.write('          <text>'+str(lyric)+'</text>\n')
         self.file.write('        </lyric>\n')
         self.file.write('      </note>\n')

   def backOneBar(self):
      if self.file is not None:
         self.file.write('      <backup>\n')
         self.file.write('        <duration>'+str(int(self.DIVISIONS*4))+'</duration>\n')
         self.file.write('      </backup>\n')

   def writeSop(self, notes, durations, lyrics=None):
      self.startSoprano()
      for Bindex, bar in enumerate(notes):
         if Bindex != 0:
            self.addMeasure()
         if lyrics is not None:
            for Nindex, note in enumerate(bar):
               self.addNote(bar[Nindex], durations[Bindex][Nindex], lyrics[Bindex][Nindex])
         else:
            for Nindex, note in enumerate(bar):
               self.addNote(bar[Nindex], durations[Bindex][Nindex])
      self.endPart()

   def writeAlto(self, notes, durations, lyrics=None):
      self.startAlto()
      for Bindex, bar in enumerate(notes):
         if Bindex != 0:
            self.addMeasure()
         if lyrics is not None:
            for Nindex, note in enumerate(bar):
               self.addNote(bar[Nindex], durations[Bindex][Nindex], lyrics[Bindex][Nindex])
         else:
            for Nindex, note in enumerate(bar):
               self.addNote(bar[Nindex], durations[Bindex][Nindex])
      self.endPart()

   def writeTenor(self, notes, durations, lyrics=None):
      self.startTenor()
      for Bindex, bar in enumerate(notes):
         if Bindex != 0:
            self.addMeasure()
         if lyrics is not None:
            for Nindex, note in enumerate(bar):
               self.addNote(bar[Nindex], durations[Bindex][Nindex], lyrics[Bindex][Nindex])
         else:
            for Nindex, note in enumerate(bar):
               self.addNote(bar[Nindex], durations[Bindex][Nindex])
      self.endPart()

   def writeBass(self, notes, durations, lyrics=None):
      self.startBass()
      for Bindex, bar in enumerate(notes):
         if Bindex != 0:
            self.addMeasure()
         if lyrics is not None:
            for Nindex, note in enumerate(bar):
               self.addNote(bar[Nindex], durations[Bindex][Nindex], lyrics[Bindex][Nindex])
         else:
            for Nindex, note in enumerate(bar):
               self.addNote(bar[Nindex], durations[Bindex][Nindex])
      self.endPart()
