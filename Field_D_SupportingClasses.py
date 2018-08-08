####################################################################
# DF_SupportingClasses by Daniel Field                             #
#                                                                  #
# This file contains the supporting classes for the SATB algorithm #
# check out www.github.com/dan-field/Text2SATB for info and rights #
####################################################################


class DF_Syllables:
   def __init__(self):
      """Initialises a DF_Syllables object"""
      self.vowels = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]
      self.vowels_y = ["a", "e", "i", "o", "u", "y", "A", "E", "I", "O", "U", "Y"]
      self.vowels_c_g_s = ["a", "c", "e", "g", "i", "o", "s", "u", "A", "C", "E", "G", "I", "O", "S", "U"]
      self.suffixesOne = ["i", "y"]
      self.suffixesTwo = []#"ac", "al", "an", "ar", "ee", "en", "er", "ic", "or"]
      self.suffixesThree = ["ade", "age", "ant", "ard", "ary", "ate", "day", "dom", "dox", "eer", "ent", "ern", "ese",
      "ess", "est", "ful", "gam", "gon", "ial", "ian", "iel", "ify", "ile", "ily", "ine", "ing", "ion", "ish", "ism", "ist",
      "ite", "ity", "ive", "ise", "ize", "let", "log", "oid", "oma", "ory", "ous", "ure"]
      self.suffixesFour = ["able", "ance", "bred", "cide", "crat", "cule", "emia", "ence", "ency", "etic", "ette", "gamy", "hood",
      "ible", "ical", "ious", "itis", "less", "like", "ling", "ment", "ness", "onym", "opia", "opsy", "osis", "path",
      "sect", "ship", "sion", "some", "tion", "tome", "tomy", "tude", "ular", "uous", "ward", "ware", "wise", "xion", "yond"]
      self.suffixesFive = ["acity", "algia", "arian", "arium", "ation", "ative", "cracy", "cycle", "esque", "gonic", "guage", "iasis",
      "ledge", "loger", "ocity", "ology", "otomy", "orium", "pathy", "phile", "phone", "phyte", "scopy", "scope", "sophy", "thing", "times", "tions", "ulous", "wards"]
      self.suffixesSix = ["aholic", "ectomy", "iatric", "logist", "oholic", "ostomy", "phobia", "plegia", "plegic", "scribe",
      "script", "sophic", "trophy"]
      self.suffixesSeven = ["alogist", "escence", "isation", "ization", "ologist"]
      self.prefixesTwo = ["de", "il", "im", "in", "ir", "re", "un", "up"]
      self.le_exceptions = ["whole", "mobile", "pole", "male", "female", "hale", "pale", "tale", "sale", "aisle", "whale", "while", "bale"]
      self.co_exceptions = ["cool", "coach", "coat", "coal", "could", "count", "coin", "coarse", "coup", "coif", "cook", "coign", "coiffe", "coof", "court"]
      self.consonantGroups_two = ["bl", "br", "ch", "ck", "cl", "cr", "dr", "fl", "fr", "gh", "gl", "gr", "kn", "ng", "ph", "pl",
      "pr", "sc", "sh", "sk", "sl", "sm", "sn", "sp", "st", "sw", "th", "tr", "tw", "wh", "wr"]
      self.consonantGroups_three = ["n't", "nth", "sch", "scr", "shr", "spl", "spr", "squ", "str", "thr"]

   def b(self, word):
      if len(word) < 4:
         return self.breakDownShortWord(word)
      else:
         start, rest = self.breakDownFromFront(word)
         if len(rest) < 4:
            adjusted_endLength = 0
         else:
            ending, endLength = self.searchSuffix(rest)
            rest = rest[:len(rest)-endLength]
            adjusted_ending = self.breakDownFromBack(rest, ending)
            adjusted_endLength = 0
            for syllable in adjusted_ending:
               for letter in syllable:
                  adjusted_endLength += 1
            if adjusted_endLength > endLength:
               rest = rest[:len(rest)+endLength-adjusted_endLength]
         restBrokenDown = self.r(rest)
         if len(restBrokenDown) > 1: # make a late adjustment for 'ed' endings that don't sound separately
            if restBrokenDown[-1] == "ed":
               if restBrokenDown[-2][-1] not in ["c", "d", "i", "t"]:
                  restBrokenDown[-2] = restBrokenDown[-2]+restBrokenDown[-1]
                  del restBrokenDown[-1]
            elif len(restBrokenDown[-1]) > 2:
               if restBrokenDown[-1][-2] == "e" and restBrokenDown[-1][-1] == "d":
                  if restBrokenDown[-1][-3] not in ["c", "d", "i", "t"] and restBrokenDown[-1][0] not in self.vowels:
                     restBrokenDown[-2] = restBrokenDown[-2]+restBrokenDown[-1]
                     del restBrokenDown[-1]
            # also, make a late adjustment for first two syllables that should actually be one (note: 'co' starts are not affected here if they are part of the prefix i.e. 'start')
            if len(restBrokenDown[0]) == 2 and len(restBrokenDown[1]) == 2:
               if restBrokenDown[0][0] not in self.vowels and restBrokenDown[0][1] in self.vowels_y:
                  if restBrokenDown[1][0] not in self.vowels and restBrokenDown[1][1] in ["e", "E"]:
                     restBrokenDown[0] = restBrokenDown[0]+restBrokenDown[1]
                     del restBrokenDown[1]
         result = []
         if start != "":
            result.append(start)
         if restBrokenDown != []:
            for syllable in restBrokenDown:
               result.append(syllable)
         if adjusted_endLength > 0:
            for syllable in adjusted_ending:
               result.append(syllable)
         return result

   def breakDownShortWord(self, word):
      # this function breaks an English word down into its syllables, starting at the end of the word
      word = str(word)
      w = str.lower(word)
      wordLength = len(word)
      if wordLength < 2: # either there is no word, or it's a single letter. No breakdown necessary
         return [word]
      elif wordLength == 2:
         if w[0] not in self.vowels or w[1] not in self.vowels:
            # there is at least one consonant in the two-letter word - it's a single syllable
            return [word]
         else:
            # two vowels (unusual) - let's assume they'll be sung as two separate syllables
            return [word[0], word[1]]
      elif wordLength == 3:
         if w[0] in self.vowels and w[1] not in self.vowels and w[2] in self.vowels_y:
            # we have VOWEL-CONSONANT-VOWEL or VOWEL-CONS-y
            if w[2] != "e":
               # the last vowel is not 'e', so it's probably two syllables
               return[word[0], word[1]+word[2]]
         # in any other case, it's probably one syllable
         return [word]

   def breakDownFromBack(self, word, suffix):
      # pass in the found suffix plus the preceding word elements
      w = str.lower(word)
      lengthRemaining = len(word)+len(suffix)
      wordLength = lengthRemaining
      suffixLength = len(suffix)
      lengthRemaining -= suffixLength
      if suffix != "":
         suffix = self.breakDownSuffix(suffix)
         if suffixLength == wordLength: # somehow we've got a whole word that matches a suffix; no need for further work
            return suffix
         elif suffixLength > wordLength-4: # there are only one or two letters before the suffix - let's deal with them now
            if suffixLength == wordLength-1: # in fact there's only one letter before the suffix
               if w[0] not in self.vowels: # that first letter is a consonant
                  suffix[0] = word[0]+suffix[0] # add that consonant on to the start of the first syllable
                  return suffix # and we're done
               else: # we've got a leading vowel; best to treat it as its own syllable
                  adjusted_suffix = [word[0]] # this is a new list; the first element is the first letter of the word
                  for syllable in suffix:
                     adjusted_suffix.append(syllable) # now add the original syllable/s behind the initial vowel syllable
                  return adjusted_suffix # and we're done
            elif suffixLength == wordLength-2: # there are actually two letters before the suffix; if they are both consonants, we tack them on; otherwise, they're a syllable
               if w[0] not in self.vowels and w[1] not in self.vowels_y:
                  suffix[0] = word[0]+word[1]+suffix[0]
                  return suffix
               else:
                  adjusted_suffix = [word[0]+word[1]]
                  for syllable in suffix:
                     adjusted_suffix.append(syllable)
                  return adjusted_suffix
            else: # there are exactly three letters before the suffix; we can treat this like a 3-letter word
               if w[0] in self.vowels and w[1] not in self.vowels and w[2] in self.vowels_y:
                  # we have VOWEL-CONSONANT-VOWEL or VOWEL-CONS-y
                  if w[2] != "e":
                     # the last vowel is not 'e', so it's probably two syllables
                     adjusted_suffix = [word[0], word[1]+word[2]]
                     for syllable in suffix:
                        adjusted_suffix.append(syllable)
                     return adjusted_suffix
               # in any other case, it's probably one syllable
               adjusted_suffix = [word[0]+word[1]+word[2]]
               for syllable in suffix:
                  adjusted_suffix.append(syllable)
               return adjusted_suffix
         else: # we have found a suffix and there are more than three letters before it
            pass
      # now check for 'e' endings (on the whole word, or the word with suffix removed, as applicable)
      if w[-1] == "e": # last letter is 'e'
         if w[-2] not in self.vowels and w[-3] in self.vowels_y: # second-last is consonant and third-last is vowel
            ending = word[-3]+word[-2]+word[-1] # this is a Vowel-Consonant-e ending
            if w[-4] not in self.vowels and len(w) == 4: # it's cons-vowel-cons-'e' so it's a single syllable (note the 'le' ending has already been dealt with in the 'searchSuffix' function)
               if suffix == "":
                  return [word]
               else:
                  adjusted_word = [word[:(lengthRemaining)]]
                  for syllable in suffix:
                     adjusted_word.append(syllable)
                  return adjusted_word
            else:
               return suffix
         else:
            return suffix
      else:
         return suffix

   def breakDownFromFront(self, word):
      word = str(word)
      w = str.lower(word)
      start = ""
      if len(w) > 1:
         if w[:2] == "mc":
            start = word[0]+word[1]
      if len(w) > 2:
         if w[:2] == "bi" and w[2] in self.vowels:
            start = word[0]+word[1]
      if len(w) > 3:
         if w[:3] == "tri" and w[3] in self.vowels:
            start = word[0]+word[1]+word[2]
         if w[:3] == "pre" and w[3] in self.vowels:
            start = word[0]+word[1]+word[2]
      if len(w) > 5:
         if w[:2] == "co" and w[2] in self.vowels and w[:6] not in self.co_exceptions and w[:5] not in self.co_exceptions and w[:4] not in self.co_exceptions:
            start = word[0]+word[1]
      elif len(w) > 4:
         if w[:2] == "co" and w[2] in self.vowels and w[:5] not in self.co_exceptions and w[:4] not in self.co_exceptions:
            start = word[0]+word[1]
      elif len(w) > 3:
         if w[:2] == "co" and w[2] in self.vowels and w[:4] not in self.co_exceptions:
            start = word[0]+word[1]
      if start != "": # a start has been found
         if len(start) == 2 and len(w) > 2:
            rest = ""+word[2:len(w)]
         elif len(start) == 3 and len(w) > 3:
            rest = ""+word[3:len(w)]
         else:
            rest = ""
      else:
         rest = word
      return start, rest

   def r(self, word):
      if word == "":
         return []
      breakdown, tracker = self.regularBreakDown(word)
      result = []
      skipNext = False
      for index, element in enumerate(breakdown):
         if index == 0: # this is the beginning of the word
            result.append(element)
            if len(breakdown) > 1:
               if tracker[0] == "c" and tracker[1] == "v":
                  result[0] = result[0]+breakdown[1]
                  skipNext = True
         elif index == len(breakdown)-1: # there are at least two elements in the word and this is the last one
            # in general, we want to join a consonant group unless it's "n't" or starts with an apostrophe
            # if it's a vowel group then we want to sound it separately
            # also, if it's an unsounded "e" we might need to modify the previous group/s slightly
            if tracker[index] == "c" and str.lower(element) != "n't" and element[0] != "'":
               result[-1] = result[-1]+element # join this final consonant group onto the end of the last syllable
               break
            else: # check if it's an unsounded e -- adjust for 'skipNext' dynamic
               if str.lower(element) == "e":
                  if skipNext is True: # will be true if the preceding group was a consonant; if it's false then it's preceded by a vowel group so it's sounded
                     if len(result[-1]) > 2: # the current last syllable has at least three letters
                        if result[-1][-2] not in self.vowels and result[-1][-3] in self.vowels:
                           # we have a final e preceded by something that ends in vowel-consonant
                           # the 'e' is already in place and it's already a single syllable, there's nothing more to do
                           # Note: this shouldn't really happen; if 'skipNext' is true then the preceding syllable should NOT have a vowel group at the start
                           break
                     if len(result) > 1: # there are at least two syllables already in the result
                        if len(result[-1]) == 2 and result[-1][0] not in self.vowels and result[-2][-1] in self.vowels:
                           # we have a final 'e' preceded by a single consonant preceded by a vowel
                           result[-2] = result[-2]+result[-1] # join the last 'xe' syllable on to the preceding vowel-ending syllable
                           del result[-1] # remove the 'xe' syllable
                           break
                        elif len(result[-1]) == 2 and result[-1][0] in ["c", "g", "s"]:
                           # most likely the final e is modifying the consonant, and is not a separate syllable
                           result[-2] = result[-2]+result[-1] # join the last 'xe' syllable on to the preceding vowel-ending syllable
                           del result[-1] # remove the 'xe' syllable
                           break
               # we arrive here if we have not hit a 'break' statement above; that is, none of the above conditions applied
               # so we have n't, 'xyz or a vowel group that's not an unsounded e
               if skipNext is False:
                  result.append(element) # add it as a separate syllable
         else: # there's at least one element before and after this one
            if tracker[index] == "c" and tracker[index+1] == "v":
               result.append(element+breakdown[index+1])
               skipNext = True
            elif tracker[index] == "c" and tracker[index+1] == "c":
               result[-1] = result[-1]+element
               skipNext = False
            elif tracker[index] == "v":
               if skipNext is False:
                  result.append(element)
               else:
                  skipNext = False
                  # check for an unsounded e followed by an s - unless the e is preceded by a c, g or s
                  if str.lower(element) == "e" and str.lower(breakdown[index+1]) == "s" and len(result) > 1: # mostly copied from the 'final e' check above
                     if len(result[-1]) == 2 and result[-1][0] not in self.vowels_c_g_s and result[-2][-1] in self.vowels_y:
                        # we have a standalone 'e' preceded by a single consonant preceded by a vowel
                        result[-2] = result[-2]+result[-1] # join the last 'xe' syllable on to the preceding vowel-ending syllable
                        del result[-1] # remove the 'xe' syllable
      return result

   def regularBreakDown(self, word):
      w = str.lower(word)
      syllableEstimate = 0
      thisGroupLength = 0
      wordBreakdown = []
      VCTracker = []
      # look for consonant and vowel groups
      for index, letter in enumerate(w):
         if index == 0: # first letter
            if letter in self.vowels: # the word starts with a vowel (excluding 'y')
               syllableEstimate += 1
               thisGroupLength += 1
               v_c = "v"
            else: # we're treating an initial 'y' as a consonant
               v_c = "c"
               thisGroupLength += 1
         else: # every other letter
            if letter in self.vowels_y: # from here on, 'y' is treated like a vowel
               if v_c[-1] != "v": # the preceding letter was not a vowel
                  syllableEstimate += 1
                  grouping = self.checkConsonantGroup(word[index-thisGroupLength:index])
                  for group in grouping:
                     wordBreakdown.append(group)
                     VCTracker.append("c")
                  thisGroupLength = 1
               else: # the preceding letter was also a vowel
                  thisGroupLength += 1
               v_c = v_c+"v"
            else: # this letter is a consonant
               if v_c[-1] != "c": # the preceding letter was not a consonant
                  grouping = self.checkVowelGroup(word[index-thisGroupLength:index])
                  for group in grouping:
                     wordBreakdown.append(group)
                     VCTracker.append("v")
                  thisGroupLength = 1
               else: # the preceding letter was also a consonant
                  thisGroupLength += 1
               v_c = v_c+"c"
            # the last vowel/consonant grouping has not been dealt with yet (because you have to get 'past' the end of it before it's dealt with)
            # so now we have to handle that final group
            if index == len(w)-1: # this is the last letter
               if v_c[-1] == "v": # the final group is a vowel group
                  grouping = self.checkVowelGroup(word[-thisGroupLength:])
                  for group in grouping:
                     wordBreakdown.append(group)
                     VCTracker.append("v")
               else: # the final group is a consonant group
                  grouping = self.checkConsonantGroup(word[-thisGroupLength:])
                  for group in grouping:
                     wordBreakdown.append(group)
                     VCTracker.append("c")
      return wordBreakdown, VCTracker

   def checkVowelGroup(self, group): # for simplicity, we'll say every vowel group is one syllable unless it starts with an 'i' (other than 'ie'); then it's two
      if len(group) == 1:
         return [group]
      elif len(group) == 2:
         if group[0] in ["i", "I"] and group[1] not in ["e", "E"]:
            return [group[0], group[1]]
         else:
            return [group]
      elif group[0] in ["i", "I"]:
         return [group[0], group[1:]]
      else:
         return [group]

   def checkConsonantGroup(self, group):
      g = str.lower(group)
      if len(g) == 1:
         return [group]
      elif len(g) == 2:
         if g in self.consonantGroups_two:
            return [group]
         elif g[0] == g[1]: # double letter
            return [group]
         else:
            return [group[0], group[1]]
      elif len(g) == 3:
         if g in self.consonantGroups_three:
            return [group]
         elif g[0]+g[1] in self.consonantGroups_two:
            return [group[0]+group[1], group[2]]
         elif g[1]+g[2] in self.consonantGroups_two:
            return [group[0], group[1]+group[2]]
         else: # no consonant groups found
            return [group[0], group[1]+group[2]]
      elif len(g) > 3:
         if g[-3]+g[-2]+g[-1] in self.consonantGroups_three:
            return [group[:-3], group[-3:]]
         elif g[0]+g[1]+g[2] in self.consonantGroups_three:
            return [group[:3], group[3:]]
         elif g[-2]+g[-1] in self.consonantGroups_two:
            return [group[:-2], group[-2:]]
         elif g[0]+g[1] in self.consonantGroups_two:
            return [group[:2], group[2:]]
         else: # no consonant groups found
            return [group[:2], group[2:]]

   def searchSuffix(self, word):
      # conducts a search for common suffixes
      word = str(word)
      w = str.lower(word)
      wordLength = len(word)
      lastTwo = w[-2]+w[-1]
      lastThree = w[-3]+lastTwo
      lastFour = w[-4]+lastThree
      if wordLength > 4:
         lastFive = w[-5]+lastFour
         if wordLength > 5:
            lastSix = w[-6]+lastFive
            if wordLength > 6:
               lastSeven = w[-7]+lastSix
               if lastSeven in self.suffixesSeven:
                  return word[-7:], 7
            if lastSix in self.suffixesSix:
               return word[-6:], 6
         if lastFive in self.suffixesFive:
            return word[-5:], 5
      if lastFour in self.suffixesFour:
         return word[-4:], 4
      elif lastThree in self.suffixesThree:
         return word[-3:], 3
      elif lastTwo in self.suffixesTwo:
         return word[-2:], 2
      elif w[-1] == 'y' and w[-2] not in self.vowels: # for example, by, ly, ty, etc
         return word[-2:], 2
      elif w[-1] == 'e' and w[-2] == 'l' and w not in self.le_exceptions: # 'le' ending other than the specified exceptions
         return word[-2:], 2
      else:
         return "", 0

   def breakDownSuffix(self, S):
      suffix = str.lower(S)
      # manually break down the items in the suffix list
      # 1. Single-syllable suffixes
      if len(suffix) < 3 or suffix in ["bred", "day", "dom", "dox", "ful", "gam", "gon", "let", "log", "cide", "crat", "cule", "guage", "hood",
      "ledge", "less", "like", "ling", "ment", "ness", "path", "sect", "ship", "some", "tome", "tude", "ward", "ware", "wise",
      "phile", "phone", "phyte", "scope", "wards", "scribe", "script", "thing", "yond", "ade", "age", "ant", "ard", "ate", "eer", "ent",
      "ern", "ese", "ess", "est", "ile", "ine", "ing", "ish", "ism", "ist", "ite", "ive", "ise", "ize", "oid", "ous",
      "ure", "ance", "ence", "ette", "esque", "sion", "tion", "times", "tions", "xion"]:
         return [S]
      # 2. Other suffixes
      elif suffix in ["ency", "gamy", "opsy", "tomy"]: # 2,2
         return [S[-4]+S[-3], S[-2]+S[-1]]
      elif suffix in ["cycle", "loger", "pathy", "sophy"]: # 2,3
         return [S[-5]+S[-4], S[-3]+S[-2]+S[-1]]
      elif suffix in ["cracy", "gonic", "scopy"]: # 3,2
         return [S[-5]+S[-4]+S[-3], S[-2]+S[-1]]
      elif suffix in ["emia", "opia"]: # 1,2,1
         return [S[-4], S[-3]+S[-2], S[-1]]
      elif suffix in ["algia"]: # 2,2,1
         return [S[-5]+S[-4], S[-3]+S[-2], S[-1]]
      elif suffix in ["acity", "arian", "arium", "ocity", "ology", "otomy", "orium"]: # 1,2,2
         return [S[-5], S[-4]+S[-3], S[-2]+S[-1]]
      elif suffix in ["iasis"]: # 1,1,3
         return [S[-5], S[-4], S[-3]+S[-2]+S[-1]]
      elif suffix in ["aholic", "oholic"]: # 1,2,3
         return [S[-6], S[-5]+S[-4], S[-3]+S[-2]+S[-1]]
      elif suffix in ["phobia", "plegia"]: # 3,2,1
         return [S[-6]+S[-5]+S[-4], S[-3]+S[-2], S[-1]]
      elif suffix in ["ostomy"]: # 1,3,2
         return [S[-6], S[-5]+S[-4]+S[-3], S[-2]+S[-1]]
      elif suffix in ["iatric"]: # 1,1,4
         return [S[-6], S[-5], S[-4]+S[-3]+S[-2]+S[-1]]
      elif suffix in ["plegic", "trophy"]: # 3,3
         return [S[-6]+S[-5]+S[-4], S[-3]+S[-2]+S[-1]]
      elif suffix in ["logist", "sophic"]: # 2,4
         return [S[-6]+S[-5], S[-4]+S[-3]+S[-2]+S[-1]]
      elif suffix in ["ectomy"]: # 2,2,2
         return [S[-6]+S[-5], S[-4]+S[-3], S[-2]+S[-1]]
      elif suffix in ["alogist", "isation", "ization", "ologist"]: # 1,2,4
         return [S[-7], S[-6]+S[-5], S[-4]+S[-3]+S[-2]+S[-1]]
      else:
         remainder = ""
         for i, letter in enumerate(S):
            if i != 0:
               remainder = remainder+letter
         return [S[0], remainder]

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
      self.chordPlan, self.keysOfVerses = self.planHarmonicStructure()
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
      verseKeys = []
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
         verseKeys.append(verseKey)
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
      return chords, verseKeys

   def getVerseKeys(self):
      return self.keysOfVerses

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
               if L > 0 and L < 4:
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
               if self.sylRests[index][i][j][0] is False:
                  tenNotes[index][barNo].append(thisNote)
               else:
                  tenNotes[index][barNo].append("RRR")
               tenWords[index][barNo].append(self.verses[index][i][j])
               tenPositions[index][barNo].append(self.positions[index][i][j])
               # add up the total length of this note (since it might be in two parts - if it crosses a barline)
               noteTotalLength = 0
               trill = False
               for partNote in self.durations[index][i][j]:
                  noteTotalLength += int(partNote)
               if noteTotalLength >= 8 and self.sylRests[index][i][j][0] is False and len(tenWords[index][barNo][-1]) < 3:
                  # the total period of the hold is at least a minim, it's not a rest, and the syllable is short
                  trill = True # set the flag to say this note should be trilled
               if len(self.durations[index][i][j]) == 1: # the note does not cross a barline
                  L = self.durations[index][i][j][0]
                  if trill is False:
                     tenRhythms[index][barNo].append(L)
                     tenTies[index][barNo].append(None)
                     count += L
                  else: # trill is True.
                     # First, assemble the scale to trill on
                     if chordType in [2, 3]:
                        scale = self.getMajorisedScale(chordDegree)
                     else:
                        scale = self.getMajorModeScale(chordDegree)
                     shiftedScale = []
                     for note in scale:
                        shiftedScale.append(homeKey+keyRef+note)
                     scaleTargets = self.buildFullRange(shiftedScale, self.rangeTenor[0], self.rangeTenor[1])
                     differences = [abs(thisNote - float(note)) for note in scaleTargets]
                     closest = differences.index(min(differences))
                     if closest < len(scaleTargets)-2: # there're at least two 'higher' scale note in the range
                        trillNote = scaleTargets[closest+len(tenWords[index][barNo][-1])] # the next or uber-next note in the list, according to the number of letters in the syllable
                     else: # we're already on the range top; trill 'down' instead
                        trillNote = scaleTargets[closest-1]
                     tenNotes[index][barNo].append(trillNote)
                     tenNotes[index][barNo].append(thisNote)
                     tenNotes[index][barNo].append(trillNote)
                     # add all the rest of the additional list items
                     tenRhythms[index][barNo].append(2)
                     tenRhythms[index][barNo].append(2)
                     tenRhythms[index][barNo].append(2)
                     tenRhythms[index][barNo].append(2)
                     tenTies[index][barNo].append(None)
                     tenTies[index][barNo].append(None)
                     tenTies[index][barNo].append(None)
                     tenTies[index][barNo].append(None)
                     tenWords[index][barNo].append(None) # just three of these because one was already written, above
                     tenWords[index][barNo].append(None)
                     tenWords[index][barNo].append(None)
                     tenPositions[index][barNo].append(None) # similarly, just three of these
                     tenPositions[index][barNo].append(None)
                     tenPositions[index][barNo].append(None)
                     if L > 8:
                        tenNotes[index][barNo].append(thisNote)
                        tenRhythms[index][barNo].append(L-8)
                        tenTies[index][barNo].append(None)
                        tenWords[index][barNo].append(None)
                        tenPositions[index][barNo].append(None)
                     count += L
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
               if self.sylRests[index][i][j][0] is False:
                  altoNotes[index][barNo].append(thisNote)
               else:
                  altoNotes[index][barNo].append("RRR")
               altoWords[index][barNo].append(self.verses[index][i][j])
               altoPositions[index][barNo].append(self.positions[index][i][j])
               # add up the total length of this note (since it might be in two parts - if it crosses a barline)
               noteTotalLength = 0
               trill = False
               for partNote in self.durations[index][i][j]:
                  noteTotalLength += int(partNote)
               if noteTotalLength >= 8 and self.sylRests[index][i][j][0] is False and len(altoWords[index][barNo][-1]) < 3:
                  # the total period of the hold is at least a minim, it's not a rest, and it's a short syllable
                  trill = True # set the flag to say this note should be trilled
               if len(self.durations[index][i][j]) == 1: # the note does not cross a barline
                  L = self.durations[index][i][j][0]
                  if trill is False:
                     altoRhythms[index][barNo].append(L)
                     altoTies[index][barNo].append(None)
                     count += L
                  else: # trill is True.
                     # First, assemble the scale to trill on
                     if chordType in [2, 3]:
                        scale = self.getMajorisedScale(chordDegree)
                     else:
                        scale = self.getMajorModeScale(chordDegree)
                     shiftedScale = []
                     for note in scale:
                        shiftedScale.append(homeKey+keyRef+note)
                     scaleTargets = self.buildFullRange(shiftedScale, self.rangeAlto[0], self.rangeAlto[1])
                     differences = [abs(thisNote - float(note)) for note in scaleTargets]
                     closest = differences.index(min(differences))
                     if closest < len(scaleTargets)-2:
                        trillNote = scaleTargets[closest+len(altoWords[index][barNo][-1])]
                     else:
                        trillNote = scaleTargets[closest-1]
                     altoNotes[index][barNo].append(trillNote)
                     altoNotes[index][barNo].append(thisNote)
                     altoNotes[index][barNo].append(trillNote)
                     # add all the rest of the additional list items
                     altoRhythms[index][barNo].append(2)
                     altoRhythms[index][barNo].append(2)
                     altoRhythms[index][barNo].append(2)
                     altoRhythms[index][barNo].append(2)
                     altoTies[index][barNo].append(None)
                     altoTies[index][barNo].append(None)
                     altoTies[index][barNo].append(None)
                     altoTies[index][barNo].append(None)
                     altoWords[index][barNo].append(None) # just three of these because one was already written, above
                     altoWords[index][barNo].append(None)
                     altoWords[index][barNo].append(None)
                     altoPositions[index][barNo].append(None) # similarly, just three of these
                     altoPositions[index][barNo].append(None)
                     altoPositions[index][barNo].append(None)
                     if L > 8:
                        altoNotes[index][barNo].append(thisNote)
                        altoRhythms[index][barNo].append(L-8)
                        altoTies[index][barNo].append(None)
                        altoWords[index][barNo].append(None)
                        altoPositions[index][barNo].append(None)
                     count += L
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
         #if note > 11:
         #   note -= 12
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
         #if note > 11:
         #   note -= 12
         answer.append(note)
      return answer

   def getAlteredScale(self, degree):
      scale = [0, 1, 3, 4, 6, 8, 10]
      answer = []
      for step in scale:
         note = degree+step
         #if note > 11:
         #   note -= 12
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

class DF_MIDINumbers:
   def __init__(self):
      """Initialises a DF_MIDINumbers object"""
      pass

   def MIDI2Note(self, MIDI_No, flats=None):
      # this function converts a MIDI number into a note and octave
      # 'flats' means to notate 'black notes' as flats; if flats is False then they'll be notated as sharps
      if flats is None:
         flats = True
      octave = (int(MIDI_No)/12)-1 # based on MIDI note 'zero' being in octave '-1'
      note = int(MIDI_No)%12 # MIDI note 'zero' is a C
      alter = 0 # this is the individual note's sharp/flat designation in MusicXML
      if note == 0:
         step = "C"
      elif note == 1:
         if flats is True:
            step = "D"
            alter = -1
         else:
            step = "C"
            alter = 1
      elif note == 2:
         step = "D"
      elif note == 3:
         if flats is True:
            step = "E"
            alter = -1
         else:
            step = "D"
            alter = 1
      elif note == 4:
         step = "E"
      elif note == 5:
         step = "F"
      elif note == 6:
         if flats is True:
            step = "G"
            alter = -1
         else:
            step = "F"
            alter = 1
      elif note == 7:
         step = "G"
      elif note == 8:
         if flats is True:
            step = "A"
            alter = -1
         else:
            step = "G"
            alter = 1
      elif note == 9:
         step = "A"
      elif note == 10:
         if flats is True:
            step = "B"
            alter = -1
         else:
            step = "A"
            alter = 1
      elif note == 11:
         step = "B"
      return octave, step, alter

   def Duration2Type(self, duration):
      # this function converts a duration value to a note type
      # it assumes 4 = crotchet, 16 = semi-breve (that is, "divisions" is equal to 4)
      dotted = False
      tiedToMinim = False
      if duration == 1:
         Ntype = "16th"
      elif duration == 2:
         Ntype = "eighth"
      elif duration == 3:
         Ntype = "eighth"
         dotted = True
      elif duration == 4:
         Ntype = "quarter"
      elif duration == 6:
         Ntype = "quarter"
         dotted = True
      elif duration == 8:
         Ntype = "half"
      elif duration == 10:
         Ntype = "eighth"
         tiedToMinim = True
      elif duration == 12:
         Ntype = "half"
         dotted = True
      elif duration == 14:
         Ntype = "quarter"
         dotted = True
         tiedToMinim = True
      elif duration == 16:
         Ntype = "whole"
      else:
         Ntype = "quarter"
      return Ntype, dotted, tiedToMinim

class DF_MusicXML:
   def __init__(self, usrTitle=None, progID=None, usrAuthor=None):
      """Initialises a DF_MusicXML object"""
      if usrTitle is None:
         self.Title = "Untitled Sonification"
      else:
         self.Title = str(usrTitle)
      if progID is None:
         self.progID = "DF Word Score Sonifier v1.0"
      else:
         self.progID = str(progID)
      if usrAuthor is None:
         self.Author = "from text file"
      else:
         self.Author = str(usrAuthor)
      self.MIDI = DF_MIDINumbers()
      self.DIVISIONS = 4
      self.measureNo = 0
      self.voice = 1 # 1 Soprano, 2 Alto, 3 Tenor, 4 Bass
      self.flats = True # assumes black notes should be written as flats - will need to be updated once a 'key' functionality is added
      usrFileName = raw_input("please enter a name for the output file\n: ")
      self.fileName = usrFileName+".musicxml"
      try:
         self.file = open(self.fileName, "w")
      except (OSError, IOError):
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
      self.file.write('    <creator type="lyricist">'+str(self.Author)+'</creator>\n')
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
         self.file.write('          <fifths>-3</fifths>\n')
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
         self.file.write('          <fifths>-3</fifths>\n')
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
         self.file.write('          <fifths>-3</fifths>\n')
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
         self.file.write('          <fifths>-3</fifths>\n')
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
         self.file.write('      <barline location="right">\n')
         self.file.write('        <bar-style>light-heavy</bar-style>\n')
         self.file.write('      </barline>\n')
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

   def addMeasureDbl(self):
      if self.file is not None:
         self.file.write('    </measure>\n')
         self.measureNo += 1
         self.file.write('    <measure number="'+str(self.measureNo)+'">\n')
         self.file.write('      <barline location="left">\n')
         self.file.write('        <bar-style>light-light</bar-style>\n')
         self.file.write('      </barline>\n')

   def addMeasureKeyChange(self, newKey):
      if self.file is not None:
         self.file.write('    </measure>\n')
         self.measureNo += 1
         self.file.write('    <measure number="'+str(self.measureNo)+'">\n')
         self.file.write('      <barline location="left">\n')
         self.file.write('        <bar-style>light-light</bar-style>\n')
         self.file.write('      </barline>\n')
         self.file.write('      <attributes>\n')
         self.file.write('        <key>\n')
         self.file.write('          <fifths>'+str(newKey)+'</fifths>\n')
         self.file.write('        </key>\n')
         self.file.write('      </attributes>\n')

   def addNote(self, MIDI_No, duration=None, lyric=None, position=None, tie=None): # duration: 4 = crotchet, 16 = semi-breve
      if self.file is not None:
         if duration is None:
            duration = 4 # default to a crotchet
         if lyric is None:
            lyric = "" # default to no text
         note_type, dotted, tiedToMinim = self.MIDI.Duration2Type(duration)
         self.file.write('      <note>\n')
         if MIDI_No != "RRR":
            octave, step, alter = self.MIDI.MIDI2Note(MIDI_No, self.flats)
            self.file.write('        <pitch>\n')
            self.file.write('          <step>'+str(step)+'</step>\n')
            if alter != 0:
               self.file.write('          <alter>'+str(alter)+'</alter>\n')
            self.file.write('          <octave>'+str(octave)+'</octave>\n')
            self.file.write('        </pitch>\n')
         else:
            self.file.write('        <rest/>\n')
         if tiedToMinim is False:
            self.file.write('        <duration>'+str(duration)+'</duration>\n')
         else:
            self.file.write('        <duration>'+str(duration-8)+'</duration>\n')
         self.file.write('        <voice>'+str(self.voice)+'</voice>\n')
         self.file.write('        <type>'+str(note_type)+'</type>\n')
         if dotted is True:
            self.file.write('        <dot></dot>\n')
         if tie is not None and tiedToMinim is False:
            self.file.write('        <notations>\n')
            self.file.write('          <tied type="'+str(tie)+'"></tied>\n')
            self.file.write('        </notations>\n')
         if tiedToMinim is True:
            self.file.write('        <notations>\n')
            if tie == "stop":
               self.file.write('          <tied type="stop"></tied>\n')
            self.file.write('          <tied type="start"></tied>\n')
            self.file.write('        </notations>\n')            
         self.file.write('        <lyric>\n')
         if position is not None:
            self.file.write('          <syllabic>'+str(position)+'</syllabic>\n')
         self.file.write('          <text>'+str(lyric)+'</text>\n')
         self.file.write('        </lyric>\n')
         self.file.write('      </note>\n')
         if tiedToMinim is True:
            self.file.write('      <note>\n')
            if MIDI_No != "RRR":
               self.file.write('        <pitch>\n')
               self.file.write('          <step>'+str(step)+'</step>\n')
               if alter != 0:
                  self.file.write('          <alter>'+str(alter)+'</alter>\n')
               self.file.write('          <octave>'+str(octave)+'</octave>\n')
               self.file.write('        </pitch>\n')
            else:
               self.file.write('        <rest/>\n')
            self.file.write('        <duration>8</duration>\n')
            self.file.write('        <voice>'+str(self.voice)+'</voice>\n')
            self.file.write('        <type>half</type>\n')
            self.file.write('        <notations>\n')
            self.file.write('          <tied type="stop"></tied>\n')
            if tie == "start":
               self.file.write('          <tied type="start"></tied>\n')
            self.file.write('        </notations>\n')
            self.file.write('      </note>\n')


   def backOneBar(self):
      if self.file is not None:
         self.file.write('      <backup>\n')
         self.file.write('        <duration>'+str(int(self.DIVISIONS*4))+'</duration>\n')
         self.file.write('      </backup>\n')

   def writeSop(self, notes, durations, lyrics=None, positions=None, ties=None):
      self.startSoprano()
      for Vindex, verse in enumerate(notes):
         for Bindex, bar in enumerate(verse):
            if Bindex == len(verse)-1 and Vindex != len(notes)-1: # it's the last bar of the verse but not the last verse
               self.addMeasureDbl()
            elif Bindex == len(verse)-1 and Vindex == len(notes)-1: # this is the very last bar; don't add a new bar
               pass
            elif Bindex != 0:
               self.addMeasure()
            if lyrics is not None and positions is not None and ties is not None:
               for Nindex, note in enumerate(bar):
                  self.addNote(bar[Nindex], durations[Vindex][Bindex][Nindex], lyrics[Vindex][Bindex][Nindex], positions[Vindex][Bindex][Nindex], ties[Vindex][Bindex][Nindex])
            elif lyrics is not None:
               for Nindex, note in enumerate(bar):
                  self.addNote(bar[Nindex], durations[Vindex][Bindex][Nindex], lyrics[Vindex][Bindex][Nindex])
            else:
               for Nindex, note in enumerate(bar):
                  self.addNote(bar[Nindex], durations[Vindex][Bindex][Nindex])
      self.endPart()

   def writeAlto(self, notes, durations, lyrics=None, positions=None, ties=None):
      self.startAlto()
      for Vindex, verse in enumerate(notes):
         for Bindex, bar in enumerate(verse):
            if Bindex == len(verse)-1 and Vindex != len(notes)-1: # it's the last bar of the verse but not the last verse
               self.addMeasureDbl()
            elif Bindex == len(verse)-1 and Vindex == len(notes)-1: # this is the very last bar; don't add a new bar
               pass
            elif Bindex != 0:
               self.addMeasure()
            if lyrics is not None and positions is not None and ties is not None:
               for Nindex, note in enumerate(bar):
                  self.addNote(bar[Nindex], durations[Vindex][Bindex][Nindex], lyrics[Vindex][Bindex][Nindex], positions[Vindex][Bindex][Nindex], ties[Vindex][Bindex][Nindex])
            elif lyrics is not None:
               for Nindex, note in enumerate(bar):
                  self.addNote(bar[Nindex], durations[Vindex][Bindex][Nindex], lyrics[Vindex][Bindex][Nindex])
            else:
               for Nindex, note in enumerate(bar):
                  self.addNote(bar[Nindex], durations[Vindex][Bindex][Nindex])
      self.endPart()

   def writeTenor(self, notes, durations, lyrics=None, positions=None, ties=None):
      self.startTenor()
      for Vindex, verse in enumerate(notes):
         for Bindex, bar in enumerate(verse):
            if Bindex == len(verse)-1 and Vindex != len(notes)-1: # it's the last bar of the verse but not the last verse
               self.addMeasureDbl()
            elif Bindex == len(verse)-1 and Vindex == len(notes)-1: # this is the very last bar; don't add a new bar
               pass
            elif Bindex != 0:
               self.addMeasure()
            if lyrics is not None and positions is not None and ties is not None:
               for Nindex, note in enumerate(bar):
                  self.addNote(bar[Nindex], durations[Vindex][Bindex][Nindex], lyrics[Vindex][Bindex][Nindex], positions[Vindex][Bindex][Nindex], ties[Vindex][Bindex][Nindex])
            elif lyrics is not None:
               for Nindex, note in enumerate(bar):
                  self.addNote(bar[Nindex], durations[Vindex][Bindex][Nindex], lyrics[Vindex][Bindex][Nindex])
            else:
               for Nindex, note in enumerate(bar):
                  self.addNote(bar[Nindex], durations[Vindex][Bindex][Nindex])
      self.endPart()

   def writeBass(self, notes, durations, lyrics=None, positions=None, ties=None):
      self.startBass()
      for Vindex, verse in enumerate(notes):
         for Bindex, bar in enumerate(verse):
            if Bindex == len(verse)-1 and Vindex != len(notes)-1: # it's the last bar of the verse but not the last verse
               self.addMeasureDbl()
            elif Bindex == len(verse)-1 and Vindex == len(notes)-1: # this is the very last bar; don't add a new bar
               pass
            elif Bindex != 0:
               self.addMeasure()
            if lyrics is not None and positions is not None and ties is not None:
               for Nindex, note in enumerate(bar):
                  self.addNote(bar[Nindex], durations[Vindex][Bindex][Nindex], lyrics[Vindex][Bindex][Nindex], positions[Vindex][Bindex][Nindex], ties[Vindex][Bindex][Nindex])
            elif lyrics is not None:
               for Nindex, note in enumerate(bar):
                  self.addNote(bar[Nindex], durations[Vindex][Bindex][Nindex], lyrics[Vindex][Bindex][Nindex])
            else:
               for Nindex, note in enumerate(bar):
                  self.addNote(bar[Nindex], durations[Vindex][Bindex][Nindex])
      self.endPart()

   def MIDI2Fifths(self, MIDI_Key):
      MIDI_Key = int(MIDI_Key)
      MIDI_Key = MIDI_Key%12
      if MIDI_Key == 1: # D flat
         fifths = -5
      elif MIDI_Key == 2: # D
         fifths = 2
      elif MIDI_Key == 3: # E flat
         fifths = -3
      elif MIDI_Key == 4: # E
         fifths = 4
      elif MIDI_Key == 5: # F
         fifths = -1
      elif MIDI_Key == 6: # F sharp
         fifths = 6
      elif MIDI_Key == 7: # G
         fifths = 1
      elif MIDI_Key == 8: # A flat
         fifths = -4
      elif MIDI_Key == 9: # A
         fifths = 3
      elif MIDI_Key == 10: # B flat
         fifths = -2
      elif MIDI_Key == 11: # B
         fifths = 5
      else:
         fifths = 0
      return fifths
      