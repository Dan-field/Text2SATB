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

   def planHarmonicStructure(self):
      # looks at the incoming verse structure and generates a chord sequence
      # Try to keep the chord references numeric/relative for easy adaptation
      key = 0 # number zero will represent the 'home' key
      verseKey = 0
      lineKey = 0
      chords = [] # start an empty list to hold the chords
      for index, verse in enumerate(self.verses):
         if index == 0: # first verse
            verseKey = 0 # start in the 'home' key
         elif index == len(self.verses)-1: # last verse
            verseKey = 0 # last verse also in the 'home' key
         else:
            verseSyllables = 0
            for number in self.versesLinesSyllables[index]:
               verseSyllables += number
            keyshift = self.keyShift(int(verseSyllables/20)%12) # this shifts the key by one step for every 20 syllables in the verse
            # but if there are more than 240 syllables, it goes back to zero and starts over again
            verseKey += keyshift
         for i, line in enumerate(self.verses[index]):
            if i == 0: # first line
               lineKey = verseKey # first line of each verse is in the verse's key
            elif index == len(self.verses)-1 and i == len(self.verses[index])-1: # this is the last line of the last verse
               lineKey = verseKey # last line of the song should be in the home key
            else:
               lineSyllables = self.versesLinesSyllables[index][i]
               keyshift = self.keyShift(int(lineSyllables/12)%12)
               lineKey += keyshift

   def keyShift(self, num0_12):
      # takes the key shift number 0 to 11 and changes it to +/-
      # (we're assuming the cycle of fifths but this function does not explicitly require it)
      result = 0
      if num0_12%2 == 0: # even; go negative
         result = -num0_12/2
      else: # go positive
         result = 1+num0_12/2
      return result

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
            