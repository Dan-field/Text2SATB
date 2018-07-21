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
      self.verseCount = 0
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
      lineText.append("---BREAK---")
      noted = True
      for line in inputText:
         line = line.strip()
         if line == "" and noted is False:
            lineText.append("---BREAK---")
            noted = True
         elif line != "" and noted is True:
            noted = False
         breakpoints = [0]
         for index, character in enumerate(line):
            if character in ".,:;!?-":
               breakpoints.append(index+1)
            elif index == len(line)-1:
               breakpoints.append(index+1)
         for breakpoint in breakpoints:
            if breakpoint != 0:
               lineText.append(line[previousBreakPoint:breakpoint])
            previousBreakPoint = breakpoint
      if lineText[-1] == "---BREAK---":
         del lineText[-1]
      for line in lineText:
         if line == "---BREAK---":
            self.verseCount += 1
            self.verses.append([])
            self.positions.append([])
         else:
            if line[-1] not in ".,;:!?-":
               line = line+";" # make sure an end of line is treated like a semicolon, if there's no punctuation there
            for word in line.split():
               punctuated = False
               punctuation = ""
               if word[-1] in ".,;:!?-":
                  punctuation = word[-1]
                  punctuated = True
                  word = word[:len(word)-1]
               syllables = self.S.b(word)
               if punctuated is True:
                  syllables[-1] = syllables[-1]+punctuation
               positions = range(len(syllables))
               if len(positions) == 1:
                  positions[0] = "a" # 'a' for 'alone'. There's also 's' for start, 'm' for mid, 'e' for end
               else:
                  for index, position in enumerate(positions):
                     if index == 0:
                        positions[index] = "s"
                     elif index == len(positions)-1:
                        positions[index] = "e"
                     else:
                        positions[index] = "m"
               for element in syllables:
                  self.verses[self.verseCount-1].append(element)
               for element in positions:
                  self.positions[self.verseCount-1].append(element)
      print self.verses, self.positions


