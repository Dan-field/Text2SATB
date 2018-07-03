####################################################################
# DF_MusicXML class by Daniel Field                                #
#                                                                  #
# This class handles the creation and appending of a MusicXML file #
#                                                                  #
# check out www.github.com/dan-field/Text2SATB for info and rights #
####################################################################


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
      self.measureNo = 0
      usrFileName = raw_input(" please enter a name for the output file ")
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
      self.file.write('  </part-list>\n')
      self.file.write('  <part id="P1">\n')
      self.measureNo += 1
      self.file.write('    <measure number="'+str(self.measureNo)+'">\n')
      self.file.write('      <attributes>\n')
      self.file.write('        <divisions>1</divisions>\n')
      self.file.write('        <key>\n')
      self.file.write('          <fifths>0</fifths>\n')
      self.file.write('        </key>\n')
      self.file.write('        <time>\n')
      self.file.write('          <beats>4</beats>\n')
      self.file.write('          <beat-type>4</beat-type>\n')
      self.file.write('        </time>\n')
      self.file.write('        <clef>\n')
      self.file.write('          <sign>G</sign>\n')
      self.file.write('          <line>2</line>\n')
      self.file.write('        </clef>\n')
      self.file.write('      </attributes>\n')

   def endXMLFile(self):
      if self.file is not None:
         self.file.write('    </measure>\n')
         self.file.write('  </part>\n')
         self.file.write('</score-partwise>\n')
         self.file.close()

   def addMeasure(self):
      if self.file is not None:
         self.file.write('    </measure>\n')
         self.measureNo += 1
         self.file.write('    <measure number="'+str(self.measureNo)+'">\n')

   def addNote(self):
      if self.file is not None:
         self.file.write('      <note>\n')
         self.file.write('        <pitch>\n')
         self.file.write('          <step>C</step>\n')
         self.file.write('          <octave>4</octave>\n')
         self.file.write('        </pitch>\n')
         self.file.write('        <duration>2</duration>\n')
         self.file.write('        <type>half</type>\n')
         self.file.write('      </note>\n')
         self.file.write('      <note>\n')
         self.file.write('        <pitch>\n')
         self.file.write('          <step>D</step>\n')
         self.file.write('          <octave>4</octave>\n')
         self.file.write('        </pitch>\n')
         self.file.write('        <duration>2</duration>\n')
         self.file.write('        <type>half</type>\n')
         self.file.write('      </note>\n')

