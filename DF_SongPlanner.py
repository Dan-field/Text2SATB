####################################################################
# DF_SongPlanner class by Daniel Field                             #
#                                                                  #
# This class takes the syllabic text input and plans a song        #
# from it                                                          #
# check out www.github.com/dan-field/Text2SATB for info and rights #
####################################################################

class DF_SongPlanner:
   def __init__(self, verses, positions):
      """Initialises a DF_SongPlanner object"""
      self.verses = verses
      self.positions = positions
      self.measureNo = 0
      self.voice = 1 # 1 Soprano, 2 Alto, 3 Tenor, 4 Bass
      self.numberOfVerses = len(self.verses)
      self.versesLinesSyllables = self.getLinesAndSyllables(self.verses)
      self.rangeSop = [60, 84]
      self.rangeAlto = [55, 79]
      self.rangeTenor = [47, 69]
      self.rangeBass = [40, 64]

   def planStructure(self):
      # looks at the incoming verse structure and plans a song structure
      pass

   def getLinesAndSyllables(self, verses):
      resultSong = []
      for verse in verses:
         resultVerse = []
         for line in verse:
            syllableCount = 0
            for syllable in line:
               syllableCount += 1
            resultVerse.append(syllableCount)
         resultSong.append(resultVerse)
      return resultSong
            