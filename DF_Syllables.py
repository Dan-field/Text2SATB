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
      self.vowels = ["A", "a", "E", "e", "I", "i", "O", "o", "U", "u"]
      self.vowels_y = ["A", "a", "E", "e", "I", "i", "O", "o", "U", "u", "Y", "y"]

   def b(self, word):
      # this function breaks an English word down into its syllables
      word = str(word)
      wordLength = len(word)
      if wordLength < 2: # either there is no word, or it's a single letter. No breakdown necessary
         return [word]
      elif wordLength == 2:
         if word[0] not in self.vowels or word[1] not in self.vowels:
            # there is at least one consonant in the two-letter word - it's a single syllable
            return [word]
         else:
            # two vowels (unusual) - let's assume they'll be sung as two separate syllables
            return [word[0], word[1]]
      elif wordLength == 3:
         if word[0] in self.vowels and word[1] not in self.vowels and word[2] in self.vowels_y:
            # we have VOWEL-CONSONANT-VOWEL or VOWEL-CONS-y
            if word[2] != "e" and word[2] != "E":
               # the last vowel is not 'e', so it's probably two syllables
               return[word[0], word[1]+word[2]]
         # in any other case, it's probably one syllable
         return [word]

