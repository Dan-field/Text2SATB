####################################################################
# DF_MIDINumbers class by Daniel Field                             #
#                                                                  #
# This class handles MIDI number operations                        #
#                                                                  #
# check out www.github.com/dan-field/Text2SATB for info and rights #
####################################################################


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

