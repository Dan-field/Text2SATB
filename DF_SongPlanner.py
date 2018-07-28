6####################################################################
# DF_SongPlanner class by Daniel Field                             #
#                                                                  #
# This class takes the syllabic text input and plans a song        #
# from it                                                          #
# check out www.github.com/dan-field/Text2SATB for info and rights #
####################################################################

class DF_SongPlanner:
   def __init__(self, verses, positions, scores):
      """Initialises a DF_SongPlanner object"""
      self.homeKey = 8 # MIDI number 8 = 'A flat' (or G sharp)
      self.verses = verses
      self.positions = positions
      self.scores = scores
      self.durations, self.sylRests = self.holdPlanner()
      self.measureNo = 0
      self.voice = 1 # 1 Soprano, 2 Alto, 3 Tenor, 4 Bass
      self.numberOfVerses = len(self.verses)
      self.versesLinesSyllables = self.getLinesAndSyllables(self.verses)
      self.chordPlan = self.planHarmonicStructure()
      self.chordBase, self.chordType = self.determineChordSequence()
      self.rangeSop = [60, 80]
      self.rangeAlto = [55, 76]
      self.rangeTenor = [47, 67]
      self.rangeBass = [42, 64]
      self.bassNotes = []
      self.bassRhythms = []
      self.bassWords = []
      self.bassPositions = []
      self.bassTies = []
      self.tenNotes = []
      self.tenRhythms = []
      self.tenWords = []
      self.tenPositions = []
      self.tenTies = []
      self.altoNotes = []
      self.altoRhythms = []
      self.altoWords = []
      self.altoPositions = []
      self.altoTies = []
      self.sopNotes = []
      self.sopRhythms = []
      self.sopWords = []
      self.sopPositions = []
      self.sopTies = []
      self.sopLatestNote = 72

   def planHarmonicStructure(self):
      # looks at the incoming verse structure and generates a chord sequence
      # Try to keep the chord references numeric/relative for easy adaptation
      key = 0 # number zero will represent the 'home' key
      verseKey = 0
      lineKey = 0
      chords = [] # start an empty list to hold the chords
      for index, verse in enumerate(self.verses):
         chords.append([]) # start an empty sub-list for each verse
         if index == 0: # first verse
            verseKey = 0 # start in the 'home' key
         elif index == len(self.verses)-1: # last verse
            verseKey = 0 # last verse also in the 'home' key
         else: # for the middle verses, key change is based on number of syllables in the verse
            verseSyllables = 0
            for number in self.versesLinesSyllables[index]:
               verseSyllables += number # add up the number of syllables in the verse
            keyshift = self.keyShift(int(verseSyllables/20)%12) # this shifts the key by one step for every 20 syllables in the verse
            # but if there are more than 240 syllables, it goes back to zero and starts over again
            verseKey += keyshift
         for i, line in enumerate(verse): # similarly, we might change key from line to line using the same sort of logic
            if i == 0: # first line
               lineKey = verseKey # first line of each verse is in the verse's key
            elif index == len(self.verses)-1 and i == len(self.verses[index])-1: # this is the last line of the last verse
               lineKey = verseKey # last line of the song should be in the home key
            else:
               lineSyllables = self.versesLinesSyllables[index][i] # this is the previously-calculated number of syllables in the line
               keyshift = self.keyShift(int(lineSyllables/12)%12) # shift key one 'step' for every 12 syllables in the line
               lineKey += keyshift
            chords[index].append(lineKey)
      return chords

   def determineChordSequence(self):
      # sets a chord sequence based on the scrabble scores and the pre-determined harmonic structure
      chordBase = []
      chordType = []
      for index, verse in enumerate(self.verses):
         chordBase.append([])
         chordType.append([])
         for i, line in enumerate(verse):
            chordBase[index].append([])
            chordType[index].append([])
            for j, syllable in enumerate(line):
               cycleMove = 0
               chordComplexity = 0
               # we want to set a chord degree and type that reflects the Scrabble score of the word
               # There are 7 degrees in a cycle: 4, 7, 3, 6, 2, 5, 1
               # There are 4 types: base, base with extensions, alterations level 1, alterations level 2
               # Without triples, doubles and bonuses, a Scrabble score of about 30 is quite high.
               if self.scores[index][i][j] > 31:
                  cycleMove = 6
                  chordComplexity = 3
               else:
                  cycleMove = int(self.scores[index][i][j]/6)%7 # moves one step for every 6 points
                  chordComplexity = int(self.scores[index][i][j]/8)%4 # one degree of complexity for every 8 points
               chordBase[index][i].append(cycleMove)
               chordType[index][i].append(chordComplexity)
      # now convert the 'cycle moves' to cycle numbers
      for index, verse in enumerate(chordBase): # we want to end each line on its 'zero' position
         for i, line in enumerate(verse):
            totalMove = 0
            for move in line:
               totalMove += move # work out the total cycle movement in the line
            start = totalMove%7 # start the line with that amount of shift (%7 to go back to the start of the cycle if necessary)
            last = start # we want to go 'backwards' by the starting amount, to end up in the right place at the finish
            for j, move in enumerate(line):
               chordBase[index][i][j] = (last-move)%7 # work out which degree we are on, at each given syllable
               last = last-move
      return chordBase, chordType

   def holdPlanner(self):
      # determines how many beats each syllable should be given, in accordance with the word's Scrabble score
      # as well as the amenity of the vowel sound to being held
      sylLengths = []
      sylRest = []
      for index, verse in enumerate(self.verses):
         sylLengths.append([])
         sylRest.append([])
         beatCount = 0
         for i, line in enumerate(verse):
            sylLengths[index].append([])
            sylRest[index].append([])
            for j, syllable in enumerate(line):
               thisLength = 4 # default length will be one crotchet
               # we will set the length in accordance with the Scrabble score and the vowel sound
               score = self.scores[index][i][j]
               position = self.positions[index][i][j]
               if score < 5 and str.lower(syllable) not in ["a", "i", "o", "u"]: # short common words excluding nice vowels
                  if beatCount%4 != 0: # we're off the beat
                     thisLength = 2 # quaver
                  else: # we're on the beat
                     thisLength = 4 # crotchet
               else:
                  thisLength = 2 + 2*int(score/6) # eighth plus an extra eighth for every 6 points in the word
                  # but we want to modify the lengths to suit good vowel sounds
                  if position != "single": # this is a multisyllabic word
                     if str.lower(syllable[0]) in 'aou' or str.lower(syllable[-1]) in 'aou': # looks like we might have a nice vowel sound
                        thisLength += 4 # extend the length
                     consInARow = 0
                     consonanty = False
                     for letter in syllable:
                        if str.lower(letter) not in 'aeiouy':
                           consInARow +=1
                           if consInARow > 2: # we have at least three consonants in a row; probably better to sing this a little shorter
                              consonanty = True
                        else:
                           consInARow = 0
                     if consonanty is True and thisLength >= 4:
                        thisLength -= 2
               if thisLength < 2:
                  thisLength = 2 # in case it somehow ends up as zero
               if i == len(verse)-1 and j == len(line)-1: # last syllable in a line
                  remainingBeatsInBar = 16 - beatCount
                  if remainingBeatsInBar > 7:
                     thisLength = remainingBeatsInBar
                  else:
                     thisLength = remainingBeatsInBar+8
               # now we know how long we want this syllable to last, the next thing is to check if we'll go over the barline
               remainingBeatsInBar = 16 - beatCount
               if thisLength < remainingBeatsInBar:
                  sylLengths[index][i].append([int(thisLength)])
                  sylRest[index][i].append([False])
                  beatCount += thisLength
               elif thisLength == remainingBeatsInBar:
                  sylLengths[index][i].append([int(thisLength)])
                  sylRest[index][i].append([False])
                  beatCount = 0
               else: # note will go over the next barline
                  leftoverLength = thisLength - remainingBeatsInBar
                  if leftoverLength > 16: # the note wants to tie over more than one bar - that's very long
                     leftoverLength = 16 # limit it to just the next bar.
                  if leftoverLength < 16: # the note will go into the next bar, but not beyond
                     sylLengths[index][i].append([int(remainingBeatsInBar), int(leftoverLength)])
                     sylRest[index][i].append([False, False])
                     beatCount = leftoverLength
                  else: # the note will go exactly to the end of the next bar
                     sylLengths[index][i].append([int(remainingBeatsInBar), 16])
                     sylRest[index][i].append([False, False])
                     beatCount = 0
            if beatCount%16 != 0: # we're at the end of the text line but we're not at the end of a bar
               L = int(4-(beatCount%4)) # counts to next crotchet
               if L > 0:
                  sylLengths[index][i].append([L])
                  sylRest[index][i].append([True])
                  beatCount += L
                  if beatCount == 16:
                     beatCount = 0
                  self.verses[index][i].append("")
                  self.positions[index][i].append(None)
                  self.scores[index][i].append(0)
               if beatCount%16 != 0: # still not at the end of the bar, but at least we know there's a whole number of crotchet beats to go
                  L = int(16-(beatCount%16))
                  if L > 0:
                     sylLengths[index][i].append([L])
                     sylRest[index][i].append([True])
                     beatCount = 0
                     self.verses[index][i].append("")
                     self.positions[index][i].append(None)
                     self.scores[index][i].append(0)
      return sylLengths, sylRest

   def getBassPart(self, homeKey):
      bassNotes = []
      bassRhythms = []
      bassWords = []
      bassPositions = []
      bassTies = []
      count = 0
      for index, verse in enumerate(self.verses):
         bassNotes.append([])
         bassRhythms.append([])
         bassWords.append([])
         bassPositions.append([])
         bassTies.append([])
         bassNotes[index].append([])
         bassRhythms[index].append([])
         bassWords[index].append([])
         bassPositions[index].append([])
         bassTies[index].append([])
         count = 0
         barNo = -1
         for i, line in enumerate(verse):
            for j, syllable in enumerate(line):
               keyRef = self.chordPlan[index][i]
               chordDegree = self.chordBase[index][i][j] # this is just the step number - it needs to be converted to a chromatic degree number
               chordDegree = self.convertChordDegree(chordDegree)
               fifth = self.getFifth(chordDegree)
               chordType = self.chordType[index][i][j]
               if chordType in [0, 1, 2]:
                  bassRef = [homeKey+keyRef+chordDegree]
               else: # complex chord: sing the 5th in the bass
                  bassRef = [homeKey+keyRef+fifth]
               if i == len(verse)-1 and j == len(line)-1: # last syllable in the line
                  bassRef = [homeKey+keyRef+chordDegree]
               bassTargets = self.buildFullRange(bassRef, self.rangeBass[0], self.rangeBass[1])
               loose_target = 52.4 # seek out a comfortable mid-point in the bass range
               differences = [abs(loose_target - float(note)) for note in bassTargets]
               closest = differences.index(min(differences))
               thisNote = bassTargets[closest] # pick the bass note that is closest to the comfortable mid point
               thisDuration = 4
               # we have all the info we need to start assembling the Bass part
               if count%16 == 0: # the previous bar is full
                  bassNotes[index].append([])
                  bassRhythms[index].append([])
                  bassWords[index].append([])
                  bassPositions[index].append([])
                  bassTies[index].append([])
                  barNo += 1
               bassNotes[index][barNo].append(thisNote)
               bassWords[index][barNo].append(self.verses[index][i][j])
               bassPositions[index][barNo].append(self.positions[index][i][j])
               if len(self.durations[index][i][j]) == 1: # the note does not cross a barline
                  L = self.durations[index][i][j][0]
                  R = self.sylRests[index][i][j][0]
                  bassRhythms[index][barNo].append(L)
                  bassTies[index][barNo].append(None)
                  count += L
                  # now check if it was supposed to be a rest
                  if self.sylRests[index][i][j][0] is True:
                     bassNotes[index][barNo][-1] = "RRR"
               else: # we are crossing a barline
                  L = self.durations[index][i][j][0]
                  bassRhythms[index][barNo].append(L)
                  bassTies[index][barNo].append("start")
                  count += L
                  # add a new bar
                  bassNotes[index].append([])
                  bassRhythms[index].append([])
                  bassWords[index].append([])
                  bassPositions[index].append([])
                  bassTies[index].append([])
                  barNo += 1
                  bassNotes[index][barNo].append(thisNote)
                  bassWords[index][barNo].append(None)
                  bassPositions[index][barNo].append(None)
                  L = self.durations[index][i][j][1]
                  bassRhythms[index][barNo].append(L)
                  bassTies[index][barNo].append("stop")
                  count += L
      self.bassNotes = bassNotes
      self.bassRhythms = bassRhythms
      self.bassWords = bassWords
      self.bassPositions = bassPositions
      self.bassTies = bassTies

   def getTenorPart(self, homeKey):
      tenNotes = []
      tenRhythms = []
      tenWords = []
      tenPositions = []
      tenTies = []
      count = 0
      for index, verse in enumerate(self.verses):
         tenNotes.append([])
         tenRhythms.append([])
         tenWords.append([])
         tenPositions.append([])
         tenTies.append([])
         tenNotes[index].append([])
         tenRhythms[index].append([])
         tenWords[index].append([])
         tenPositions[index].append([])
         tenTies[index].append([])
         count = 0
         barNo = -1
         for i, line in enumerate(verse):
            for j, syllable in enumerate(line):
               keyRef = self.chordPlan[index][i]
               chordDegree = self.chordBase[index][i][j] # this is just the step number - it needs to be converted to a chromatic degree number
               chordDegree = self.convertChordDegree(chordDegree)
               third = self.getThird(chordDegree)
               fifth = self.getFifth(chordDegree)
               seventh = self.getSeventh(chordDegree)
               chordType = self.chordType[index][i][j]
               if chordType in [0, 1]:
                  tenRef = [homeKey+keyRef+chordDegree, homeKey+keyRef+fifth]
               else:
                  tenRef = [homeKey+keyRef+third, homeKey+keyRef+seventh]
               if i == len(verse)-1 and j == len(line)-1: # last syllable in the line
                  tenRef = [homeKey+keyRef+chordDegree, homeKey+keyRef+third, homeKey+keyRef+fifth]
               tenTargets = self.buildFullRange(tenRef, self.rangeTenor[0], self.rangeTenor[1])
               loose_target = 57.4 # seek out a comfortable mid-point in the tenor range
               differences = [abs(loose_target - float(note)) for note in tenTargets]
               closest = differences.index(min(differences))
               thisNote = tenTargets[closest] # pick the tenor note that is closest to the comfortable mid point
               thisDuration = 4
               # we have all the info we need to start assembling the Tenor part
               if count%16 == 0: # the previous bar is full
                  tenNotes[index].append([])
                  tenRhythms[index].append([])
                  tenWords[index].append([])
                  tenPositions[index].append([])
                  tenTies[index].append([])
                  barNo += 1
               tenNotes[index][barNo].append(thisNote)
               tenWords[index][barNo].append(self.verses[index][i][j])
               tenPositions[index][barNo].append(self.positions[index][i][j])
               if len(self.durations[index][i][j]) == 1: # the note does not cross a barline
                  L = self.durations[index][i][j][0]
                  R = self.sylRests[index][i][j][0]
                  tenRhythms[index][barNo].append(L)
                  tenTies[index][barNo].append(None)
                  count += L
                  # now check if it was supposed to be a rest
                  if self.sylRests[index][i][j][0] is True:
                     tenNotes[index][barNo][-1] = "RRR"
               else: # we are crossing a barline
                  L = self.durations[index][i][j][0]
                  tenRhythms[index][barNo].append(L)
                  tenTies[index][barNo].append("start")
                  count += L
                  # add a new bar
                  tenNotes[index].append([])
                  tenRhythms[index].append([])
                  tenWords[index].append([])
                  tenPositions[index].append([])
                  tenTies[index].append([])
                  barNo += 1
                  tenNotes[index][barNo].append(thisNote)
                  tenWords[index][barNo].append(None)
                  tenPositions[index][barNo].append(None)
                  L = self.durations[index][i][j][1]
                  tenRhythms[index][barNo].append(L)
                  tenTies[index][barNo].append("stop")
                  count += L
      self.tenNotes = tenNotes
      self.tenRhythms = tenRhythms
      self.tenWords = tenWords
      self.tenPositions = tenPositions
      self.tenTies = tenTies

   def getAltoPart(self, homeKey):
      altoNotes = []
      altoRhythms = []
      altoWords = []
      altoPositions = []
      altoTies = []
      count = 0
      for index, verse in enumerate(self.verses):
         altoNotes.append([])
         altoRhythms.append([])
         altoWords.append([])
         altoPositions.append([])
         altoTies.append([])
         altoNotes[index].append([])
         altoRhythms[index].append([])
         altoWords[index].append([])
         altoPositions[index].append([])
         altoTies[index].append([])
         count = 0
         barNo = -1
         for i, line in enumerate(verse):
            for j, syllable in enumerate(line):
               keyRef = self.chordPlan[index][i]
               chordDegree = self.chordBase[index][i][j] # this is just the step number - it needs to be converted to a chromatic degree number
               chordDegree = self.convertChordDegree(chordDegree)
               third = self.getThird(chordDegree)
               fifth = self.getFifth(chordDegree)
               seventh = self.getSeventh(chordDegree)
               chordType = self.chordType[index][i][j]
               if chordType in [0, 1]:
                  altoRef = [homeKey+keyRef+chordDegree, homeKey+keyRef+fifth]
               else:
                  altoRef = [homeKey+keyRef+third, homeKey+keyRef+seventh]
               if i == len(verse)-1 and j == len(line)-1: # last syllable in the line
                  altoRef = [homeKey+keyRef+chordDegree, homeKey+keyRef+third, homeKey+keyRef+fifth]
               altoTargets = self.buildFullRange(altoRef, self.rangeAlto[0], self.rangeAlto[1])
               loose_target = 64.4 # seek out a comfortable mid-point in the alto range
               differences = [abs(loose_target - float(note)) for note in altoTargets]
               closest = differences.index(min(differences))
               thisNote = altoTargets[closest] # pick the alto note that is closest to the comfortable mid point
               thisDuration = 4
               # we have all the info we need to start assembling the Alto part
               if count%16 == 0: # the previous bar is full
                  altoNotes[index].append([])
                  altoRhythms[index].append([])
                  altoWords[index].append([])
                  altoPositions[index].append([])
                  altoTies[index].append([])
                  barNo += 1
               altoNotes[index][barNo].append(thisNote)
               altoWords[index][barNo].append(self.verses[index][i][j])
               altoPositions[index][barNo].append(self.positions[index][i][j])
               if len(self.durations[index][i][j]) == 1: # the note does not cross a barline
                  L = self.durations[index][i][j][0]
                  R = self.sylRests[index][i][j][0]
                  altoRhythms[index][barNo].append(L)
                  altoTies[index][barNo].append(None)
                  count += L
                  # now check if it was supposed to be a rest
                  if self.sylRests[index][i][j][0] is True:
                     altoNotes[index][barNo][-1] = "RRR"
               else: # we are crossing a barline
                  L = self.durations[index][i][j][0]
                  altoRhythms[index][barNo].append(L)
                  altoTies[index][barNo].append("start")
                  count += L
                  # add a new bar
                  altoNotes[index].append([])
                  altoRhythms[index].append([])
                  altoWords[index].append([])
                  altoPositions[index].append([])
                  altoTies[index].append([])
                  barNo += 1
                  altoNotes[index][barNo].append(thisNote)
                  altoWords[index][barNo].append(None)
                  altoPositions[index][barNo].append(None)
                  L = self.durations[index][i][j][1]
                  altoRhythms[index][barNo].append(L)
                  altoTies[index][barNo].append("stop")
                  count += L
      self.altoNotes = altoNotes
      self.altoRhythms = altoRhythms
      self.altoWords = altoWords
      self.altoPositions = altoPositions
      self.altoTies = altoTies

   def getSopPart(self, homeKey):
      sopNotes = []
      sopRhythms = []
      sopWords = []
      sopPositions = []
      sopTies = []
      count = 0
      for index, verse in enumerate(self.verses):
         sopNotes.append([])
         sopRhythms.append([])
         sopWords.append([])
         sopPositions.append([])
         sopTies.append([])
         sopNotes[index].append([])
         sopRhythms[index].append([])
         sopWords[index].append([])
         sopPositions[index].append([])
         sopTies[index].append([])
         count = 0
         barNo = -1
         for i, line in enumerate(verse):
            for j, syllable in enumerate(line):
               ScrabbleScores = []
               for letter in syllable:
                  ScrabbleScores.append(self.scoreScrabble(letter))
               keyRef = self.chordPlan[index][i]
               chordDegree = self.chordBase[index][i][j] # this is just the step number - it needs to be converted to a chromatic degree number
               chordDegree = self.convertChordDegree(chordDegree)
               chordType = self.chordType[index][i][j]
               if chordType == 2:
                  scale = self.getMajorisedScale(chordDegree)
               elif chordType == 3:
                  scale = self.getAlteredScale(chordDegree)
               else:
                  scale = self.getMajorModeScale(chordDegree)
               third = self.getThird(chordDegree)
               fifth = self.getFifth(chordDegree)
               seventh = self.getSeventh(chordDegree)
               sopChordTargets = [homeKey+keyRef+chordDegree, homeKey+keyRef+third, homeKey+keyRef+fifth, homeKey+keyRef+seventh]
               if i == len(verse)-1 and j == len(line)-1: # last syllable in the line
                  sopChordTargets = [homeKey+keyRef+chordDegree, homeKey+keyRef+third, homeKey+keyRef+fifth]
               sopChordTargets = self.buildFullRange(sopChordTargets, self.rangeSop[0], self.rangeSop[1])
               shiftedScale = []
               for note in scale:
                  shiftedScale.append(homeKey+keyRef+note)
               sopScaleTargets = self.buildFullRange(shiftedScale, self.rangeSop[0], self.rangeSop[1])
               if i == len(verse)-1 and j == len(line)-1:
                  sopScaleTargets = sopChordTargets
               # LOOSE TARGET needs to be modified so that it's a melody note -------------------------------
               loose_target = 70.4 # seek out a comfortable mid-point in the soprano range
               if chordType == 0:
                  loose_target = 67.4
               elif chordType == 1:
                  loose_target = self.sopLatestNote - 3
               differences = [abs(loose_target - float(note)) for note in sopChordTargets]
               closest = differences.index(min(differences))
               thisNote = sopChordTargets[closest] # pick the soprano note that is closest to the comfortable mid point
               thisDuration = 4
               # we have all the info we need to start assembling the Soprano part
               if count%16 == 0: # the previous bar is full
                  sopNotes[index].append([])
                  sopRhythms[index].append([])
                  sopWords[index].append([])
                  sopPositions[index].append([])
                  sopTies[index].append([])
                  barNo += 1
               if len(self.durations[index][i][j]) == 1: # the note does not cross a barline
                  if chordType != 0: # the word's Scrabble score is reasonably high; we want more complexity/movement
                     idealNumberOfNotes = len(ScrabbleScores)
                     if self.durations[index][i][j][0] >= idealNumberOfNotes*2: # we have enough time for at least one quaver per note
                        numberOfNotes = idealNumberOfNotes
                        averageLength = int(self.durations[index][i][j][0]/numberOfNotes)
                        if averageLength%2 != 0: # averageLength is not an integer multiple of 2 (quavers)
                           averageLength -= 1 # shorten it by a semiquaver so it's a whole number of quavers
                        if averageLength == 0: # might somehow happen
                           averageLength = 2
                     else:
                        numberOfNotes = int(self.durations[index][i][j][0]/2)
                        averageLength = 2
                     fillDurations = range(numberOfNotes)
                     runningTotal = 0
                     for position in fillDurations:
                        loose_target = self.sopLatestNote + float(ScrabbleScores[position]*1.7)
                        differences = [abs(loose_target - float(note)) for note in sopChordTargets]
                        closest = differences.index(min(differences))
                        thisNote = sopChordTargets[closest]
                        if position == 0: # this is the 'actual' note with the word, prior to any fill
                           sopNotes[index][barNo].append(thisNote)
                           sopWords[index][barNo].append(self.verses[index][i][j])
                           sopPositions[index][barNo].append(self.positions[index][i][j])
                           sopTies[index][barNo].append(None)
                           sopRhythms[index][barNo].append(averageLength)
                           runningTotal += averageLength
                           count += averageLength
                        elif position < len(fillDurations)-1: # these are the middle notes of the fill
                           if thisNote != self.sopLatestNote: # it's not a repeat note
                              sopNotes[index][barNo].append(thisNote)
                              sopWords[index][barNo].append(None)
                              sopPositions[index][barNo].append(None)
                              sopTies[index][barNo].append(None)
                              sopRhythms[index][barNo].append(2)                    
                              runningTotal += 2
                              count += 2
                           else: # it is a repeat note: don't sing it twice; just lengthen the previous note
                              sopRhythms[index][barNo][-1] += 2
                              runningTotal += 2
                              count += 2
                        else: # it is the last fill note; length needs to be adjusted to take up the remaining time
                           fillDuration = self.durations[index][i][j][0] - runningTotal
                           if thisNote != self.sopLatestNote: # it's not a repeat note
                              sopNotes[index][barNo].append(thisNote)
                              sopWords[index][barNo].append(None)
                              sopPositions[index][barNo].append(None)
                              sopTies[index][barNo].append(None)
                              sopRhythms[index][barNo].append(fillDuration)                    
                              runningTotal += fillDuration
                              count += fillDuration
                           else: # it is a repeat note: don't sing it twice; just lengthen the previous note
                              sopRhythms[index][barNo][-1] += fillDuration
                              runningTotal += fillDuration
                              count += fillDuration
                        self.sopLatestNote = thisNote
                  else:
                     L = self.durations[index][i][j][0]
                     R = self.sylRests[index][i][j][0]
                     sopRhythms[index][barNo].append(L)
                     sopTies[index][barNo].append(None)
                     sopNotes[index][barNo].append(thisNote)
                     self.sopLatestNote = thisNote
                     sopWords[index][barNo].append(self.verses[index][i][j])
                     sopPositions[index][barNo].append(self.positions[index][i][j])
                     count += L
                  # now check if it was supposed to be a rest
                  if self.sylRests[index][i][j][0] is True:
                     sopNotes[index][barNo][-1] = "RRR"
               else: # we are crossing a barline
                  sopNotes[index][barNo].append(thisNote)
                  self.sopLatestNote = thisNote
                  sopWords[index][barNo].append(self.verses[index][i][j])
                  sopPositions[index][barNo].append(self.positions[index][i][j])
                  L = self.durations[index][i][j][0]
                  sopRhythms[index][barNo].append(L)
                  sopTies[index][barNo].append("start")
                  count += L
                  # add a new bar
                  sopNotes[index].append([])
                  sopRhythms[index].append([])
                  sopWords[index].append([])
                  sopPositions[index].append([])
                  sopTies[index].append([])
                  barNo += 1
                  sopNotes[index][barNo].append(thisNote)
                  self.sopLatestNote = thisNote
                  sopWords[index][barNo].append(None)
                  sopPositions[index][barNo].append(None)
                  L = self.durations[index][i][j][1]
                  sopRhythms[index][barNo].append(L)
                  sopTies[index][barNo].append("stop")
                  count += L
      self.sopNotes = sopNotes
      self.sopRhythms = sopRhythms
      self.sopWords = sopWords
      self.sopPositions = sopPositions
      self.sopTies = sopTies

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
            
   def buildFullRange(self, notes, range_bottom=None, range_top=None):
      if range_bottom is None: range_bottom = 60
      if range_top is None: range_top = 64
      full_scale = []
      pool_first_octave = []
      pool_octave = int(notes[0]/12)
      octaves = [0, 12, 24, 36, 48, 60, 72, 84, 96, 108]
      for note in notes:
         pool_first_octave.append(note - (12*pool_octave))
      for octave in octaves:
         for value in pool_first_octave:
            if octave+value >= range_bottom and octave+value <= range_top:
               full_scale.append(octave+value)
      return full_scale

   def convertChordDegree(self, stepNo): # converst a chordDegree 'distance' into a chordDegree position on the scale (in semitones)
      # note a major root scale is assumed
      chordDegree = 0
      if stepNo == 0:
         chordDegree = 0
      elif stepNo == 1:
         chordDegree = 7
      elif stepNo == 2:
         chordDegree = 2
      elif stepNo == 3:
         chordDegree = 9
      elif stepNo == 4:
         chordDegree = 4
      elif stepNo == 5:
         chordDegree = 11
      elif stepNo == 6:
         chordDegree = 5
      return chordDegree

   def getThird(self, degree):
      if degree in [0, 5, 7]: # major third
         third = degree + 4
      elif degree in [2, 4, 9, 11]: # minor third
         third = degree + 3
      if third > 11:
         third -= 12
      return third

   def getFifth(self, degree):
      if degree in [0, 2, 4, 5, 7, 9]: # perfect fifth
         fifth = degree + 7
      elif degree in [11]: # flattened fifth
         fifth = degree + 6
      if fifth > 11:
         fifth -= 12
      return fifth

   def getSeventh(self, degree):
      if degree in [0, 5]: # major 7th
         seventh = degree + 11
      elif degree in [2, 4, 7, 9, 11]: # minor 7th
         seventh = degree + 10
      if seventh > 11:
         seventh -= 12
      return seventh

   def getMajorModeScale(self, degree): # regular major modes
      if degree == 0:
         scale = [0, 2, 4, 5, 7, 9, 11]
      elif degree == 2:
         scale = [0, 2, 3, 5, 7, 9, 10]
      elif degree == 4:
         scale = [0, 1, 3, 5, 7, 8, 10]
      elif degree == 5:
         scale = [0, 2, 4, 6, 7, 9, 11]
      elif degree == 7:
         scale = [0, 2, 4, 5, 7, 9, 10]
      elif degree == 9:
         scale = [0, 2, 3, 5, 7, 9, 10]
      elif degree == 11:
         scale = [0, 1, 3, 5, 6, 8, 10]
      answer = []
      for step in scale:
         note = degree+step
         if note > 11:
            note -= 12
         answer.append(note)
      return answer

   def getMajorisedScale(self, degree): # the 'ii' and 'vi' scales are modified to be (secondary) dominants
      if degree == 0:
         scale = [0, 2, 4, 5, 7, 9, 11]
      elif degree == 2:
         scale = [0, 2, 4, 5, 7, 9, 10]
      elif degree == 4:
         scale = [0, 1, 3, 5, 7, 8, 10]
      elif degree == 5:
         scale = [0, 2, 4, 6, 7, 9, 11]
      elif degree == 7:
         scale = [0, 2, 4, 5, 7, 9, 10]
      elif degree == 9:
         scale = [0, 2, 4, 5, 7, 9, 10]
      elif degree == 11:
         scale = [0, 1, 3, 5, 6, 8, 10]
      answer = []
      for step in scale:
         note = degree+step
         if note > 11:
            note -= 12
         answer.append(note)
      return answer

   def getAlteredScale(self, degree):
      scale = [0, 1, 3, 4, 6, 8, 10]
      answer = []
      for step in scale:
         note = degree+step
         if note > 11:
            note -= 12
         answer.append(note)
      return answer

   def scoreScrabble(self, string):
      # adds up the Scrabble score of the string
      runningTotal = 0
      for letter in str.lower(string):
         if letter in 'aeioulnrst':
            runningTotal += 1
         elif letter in 'dg':
            runningTotal += 2
         elif letter in 'bcmp':
            runningTotal += 3
         elif letter in 'fhvwy':
            runningTotal += 4
         elif letter in 'k':
            runningTotal += 5
         elif letter in 'jx':
            runningTotal += 8
         elif letter in 'qz':
            runningTotal += 10
      return runningTotal