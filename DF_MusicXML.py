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
      usrFileName = raw_input(" please enter a name for the output file ")
      self.fileName = usrFileName+".musicxml"
      try:
         with open(self.fileName, "w") as file:
            file.write("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n""")
            file.write("""<!DOCTYPE score-partwise PUBLIC\n""")
            file.write("""     "-//Recordare//DTD MusicXML 3.1 Partwise//EN"\n""")
            file.write("""     "http://www.musicxml.org/dtds/partwise.dtd">\n""")
            file.write("""<score-partwise version="3.1">\n""")
            file.write("""  <work>\n""")
            file.write("""    <work-title>"""+str(self.Title)+"""</work-title>\n""")
            file.write("""  </work>\n""")
            file.write("""  <identification>\n""")
            file.write("""    <creator type="composer">"""+str(self.progID)+"""</creator>\n""")
            file.write("""  </identification>\n""")
            file.write("""  <part-list>\n""")
            file.write("""    <score-part id="P1">\n""")
            file.write("""      <part-name>Soprano</part-name>\n""")
            file.write("""    </score-part>\n""")
            file.write("""  </part-list>\n""")
            file.write("""  <part id="P1">\n""")
            file.write("""    <measure number="1">\n""")
            file.write("""      <attributes>\n""")
            file.write("""        <divisions>1</divisions>\n""")
            file.write("""        <key>\n""")
            file.write("""          <fifths>0</fifths>\n""")
            file.write("""        </key>\n""")
            file.write("""        <time>\n""")
            file.write("""          <beats>4</beats>\n""")
            file.write("""          <beat-type>4</beat-type>\n""")
            file.write("""        </time>\n""")
            file.write("""        <clef>\n""")
            file.write("""          <sign>G</sign>\n""")
            file.write("""          <line>2</line>\n""")
            file.write("""        </clef>\n""")
            file.write("""      </attributes>\n""")
            file.write("""      <note>\n""")
            file.write("""        <pitch>\n""")
            file.write("""          <step>C</step>\n""")
            file.write("""          <octave>4</octave>\n""")
            file.write("""        </pitch>\n""")
            file.write("""        <duration>4</duration>\n""")
            file.write("""        <type>whole</type>\n""")
            file.write("""      </note>\n""")
            file.write("""    </measure>\n""")
            file.write("""  </part>\n""")
            file.write("""</score-partwise>\n""")
      except IOError:
         print "There was an issue with the file operation."
         print "Please double-check your filename.\n"
         print "Note the MusicXML file will attempt to save in the"
         print "same folder as the Python files; please ensure you"
         print "have write permission for that folder."