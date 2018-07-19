####################################################################
# DF_Syllables class by Daniel Field                               #
#                                                                  #
# This class handles syllable-related operations                   #
# It is based on the English language                              #
# check out www.github.com/dan-field/Text2SATB for info and rights #
####################################################################


class DF_Syllables:
   def __init__(self):
      """Initialises a DF_Syllables object"""
      self.vowels = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]
      self.vowels_y = ["a", "e", "i", "o", "u", "y", "A", "E", "I", "O", "U", "Y"]
      self.suffixesOne = ["i", "y"]
      self.suffixesTwo = ["ac", "al", "an", "ar", "ee", "en", "er", "ic", "or"]
      self.suffixesThree = ["ade", "age", "ant", "ard", "ary", "ate", "day", "dom", "dox", "eer", "ent", "ern", "ese",
      "ess", "est", "ful", "gam", "gon", "ial", "ian", "iel", "ify", "ile", "ily", "ine", "ing", "ion", "ish", "ism", "ist",
      "ite", "ity", "ive", "ise", "ize", "let", "log", "oid", "oma", "ory", "ous", "ure"]
      self.suffixesFour = ["able", "ance", "cide", "crat", "cule", "emia", "ence", "ency", "etic", "ette", "gamy", "hood",
      "ible", "ical", "ious", "itis", "less", "like", "ling", "ment", "ness", "onym", "opia", "opsy", "osis", "path",
      "sect", "ship", "sion", "some", "tion", "tome", "tomy", "tude", "ular", "uous", "ward", "ware", "wise", "xion"]
      self.suffixesFive = ["acity", "algia", "arian", "arium", "ation", "ative", "cracy", "cycle", "esque", "gonic", "iasis",
      "loger", "ocity", "ology", "otomy", "orium", "pathy", "phile", "phone", "phyte", "scopy", "scope", "sophy", "ulous", "wards"]
      self.suffixesSix = ["aholic", "ectomy", "iatric", "logist", "oholic", "ostomy", "phobia", "plegia", "plegic", "scribe",
      "script", "sophic", "trophy"]
      self.suffixesSeven = ["alogist", "escence", "isation", "ization", "ologist"]
      self.prefixesTwo = ["de", "il", "im", "in", "ir", "re", "un", "up"]
      self.le_exceptions = ["whole", "mobile", "pole", "male", "female", "hale", "pale", "tale", "sale", "aisle", "whale", "while", "bale"]
      self.co_exceptions = ["cool", "coach", "coat", "coal", "count", "coin", "coarse", "coup", "coif", "cook", "coign", "coiffe", "coof", "court"]

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
         # NEED to add something here to further break down the 'rest'
         result = []
         if start != "":
            result.append(start)
         if rest != "":
            result.append(rest)
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

   def regularBreakdown(self, word):
      w = str.lower(word)
      # look for consonant and vowel groups
      for index, letter in enumerate(w):
         if index == 0: # first letter
            if letter in self.vowels: # the word starts with a vowel (excluding 'y')
               v_c = "v"
            else: # we're treating an initial 'y' as a consonant
               v_c = "c"
         else: # every other letter
            if letter in self.vowels_y: # from here on, 'y' is treated like a vowel
               v_c = v_c+"v"
            else:
               v_c = v_c+"c"

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
      if len(suffix) < 3 or suffix in ["day", "dom", "dox", "ful", "gam", "gon", "let", "log", "cide", "crat", "cule", "hood",
      "less", "like", "ling", "ment", "ness", "path", "sect", "ship", "some", "tome", "tude", "ward", "ware", "wise",
      "phile", "phone", "phyte", "scope", "wards", "scribe", "script", "ade", "age", "ant", "ard", "ate", "eer", "ent",
      "ern", "ese", "ess", "est", "ile", "ine", "ing", "ish", "ism", "ist", "ite", "ive", "ise", "ize", "oid", "ous",
      "ure", "ance", "ence", "ette", "esque"]:
         return [S]
      # 2. Other suffixes
      elif suffix in ["ency", "gamy", "opsy", "sion", "tion", "tomy", "xion"]: # 2,2
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
