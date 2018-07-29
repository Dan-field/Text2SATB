####################################################################
# DF_TextInput class by Daniel Field                               #
#                                                                  #
# This class handles the importing and initial processing of text  #
#                                                                  #
# check out www.github.com/dan-field/Text2SATB for info and rights #
####################################################################
from DF_Syllables import *

class DF_TextInput:
   def __init__(self):
      """Initialises a DF_TextInput object"""
      self.S = DF_Syllables()
      self.verses = []
      self.positions = []
      self.scrabbleScores = []
      self.verseCount = 0
      self.lineCount = 0
      self.lastWord = False
      lineText = []
      inputText = []
      infile = None
      usrFileName = raw_input("please enter the filename of the text input file, e.g. 'mypoem.txt'\n: ")
      try:
         infile = open(usrFileName, "r")
      except (OSError, IOError):
         infile = None
         print "\nThere was an issue attempting to open the file."
         print "Please double-check your filename; "+usrFileName+"\n"
         print "Note your input text file must be in the same"
         print "folder as the Python files."
         return
      if infile is not None:
         for line in infile.readlines():
            inputText.append(line)
         infile.close()
      # The input file has been read, and all of the text is in 'inputText'
      lineText.append("---BREAK---") # this will be used to signify a new verse
      noted = True # this is a flag to avoid multiple 'new verse' indications in a row
      for line in inputText:
         line = line.strip() # removes the 'newline' characters from the ends of the lines
         if line == "" and noted is False: # empty line - used to signify a new verse - and a new verse has not yet been noted
            lineText.append("---BREAK---") # insert a marker for a new verse
            noted = True # change the flag (just in case there are a few blank lines in a row)
         elif line != "" and noted is True: # the 'already noted' flag is set, but it's not a new line;
            noted = False # reset the flag ready for the next verse
         breakpoints = [0] # start a list of the locations of punctuation breaks
         for index, character in enumerate(line):
            if character in ".,:;!?-":
               breakpoints.append(index+1) # note the positions of any breaking punctuation marks
            elif index == len(line)-1:
               breakpoints.append(index+1) # also note a breakpoint at the end of the line, if not already noted due to punctuation
         for breakpoint in breakpoints:
            if breakpoint != 0: # for all breakpoints except the zero point,
               lineText.append(line[previousBreakPoint:breakpoint]) # add the text from the previous point to this one to lineText
            previousBreakPoint = breakpoint
      if lineText[-1] == "---BREAK---": # this is a new verse marker at the end, due to empty lines at the end
         del lineText[-1] # but it's the end; there is no new verse, so we delete the marker
      for line in lineText:
         if line == "---BREAK---": # new verse
            self.verseCount += 1 # add one to the verse count
            self.verses.append([]) # create a new empty list within 'verses'
            self.positions.append([]) # create a new empty list within 'positions'
            self.scrabbleScores.append([]) # create a new empty list within 'scrabbleScores'
            self.lastWord = False # reset the lastWord flag
            self.lineCount = 1 # restart the line count
            self.verses[self.verseCount-1].append([]) # create a new empty sub-list within the new verse list
            self.positions[self.verseCount-1].append([]) # create a new empty sub-list within the new positions list
            self.scrabbleScores[self.verseCount-1].append([]) # create a new empty sub-list within the new scrabbleScores list
         else:
            if line[-1] not in ".,;:!?-": # if there's a line that doesn't end in punctuation,
               line = line+"*" # add an asterisk. Note all the lines will get blended together so the line breaks will be lost unless they're marked
            for word in line.split(): # this splits the line into words (using 'space' as the delimiter)
               if self.lastWord is True: # the previous word was the last word of its line
                  self.lineCount += 1 # increment the line counter
                  self.verses[self.verseCount-1].append([]) # create a new line sublist within the verse list
                  self.positions[self.verseCount-1].append([]) # create a new line sublist within the position list
                  self.scrabbleScores[self.verseCount-1].append([]) # create a new line sublist within the scrabbleScores list
                  self.lastWord = False # reset the lastWord flag
               scrabbleScore = self.scoreScrabble(word) # add up the scrabble score for the word using the scoreScrabble function (below)
               punctuated = False
               punctuation = ""
               if word[-1] in ".,;:!?-*": # if there's a punctuation mark (noting that it will appear at the word end, thanks to the previous breakdown)
                  punctuation = word[-1] # store the punctuation mark separately
                  punctuated = True # set a flag to note that this has happened
                  word = word[:len(word)-1] # remove the punctuation mark from the end of the word
               syllables = self.S.b(word) # send the word to the syllable breakdown function, get back a list of syllables
               if punctuated is True: # this is the flag that was set earlier
                  if punctuation != "*": # if it's anything other than an asterisk (which is just a temporary marker, not actually needed in the text)
                     syllables[-1] = syllables[-1]+punctuation # add the punctuation back on where it came from
                  if punctuation in ".;:!?*": # these punctuation marks will create new lines
                     self.lastWord = True # this will be the last word in this line
               positions = range(len(syllables)) # start an 'empty' list with as many members as there are syllables in the word
               if len(positions) == 1: # this means there's only one syllable in the word
                  positions[0] = "single" # this follows the MusicXML 'syllabic' convention
               else: # there are two or more syllables in the word
                  for index, position in enumerate(positions):
                     if index == 0: # first syllable
                        positions[index] = "begin"
                     elif index == len(positions)-1: # last syllable
                        positions[index] = "end"
                     else: # between first and last
                        positions[index] = "middle"
               for element in syllables:
                  self.verses[self.verseCount-1][self.lineCount-1].append(element)
                  self.scrabbleScores[self.verseCount-1][self.lineCount-1].append(scrabbleScore) # list the word's Scrabble score at each syllable position
               for element in positions:
                  self.positions[self.verseCount-1][self.lineCount-1].append(element)

   def provideVerses(self):
      return self.verses

   def providePositions(self):
      return self.positions

   def provideScrabbleScores(self):
      return self.scrabbleScores

   def provideTitle(self):
      usrTitle = raw_input("please enter a Title for the work\n: ")
      if usrTitle == "":
         usrTitle = None
      return usrTitle

   def provideLyricist(self):
      usrLyricist = raw_input("please enter the Lyricist's name\n: ")
      if usrLyricist == "":
         usrLyricist = None
      return usrLyricist

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