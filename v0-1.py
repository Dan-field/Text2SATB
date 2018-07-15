from DF_MusicXML import *

ProgramID = "Test_code v 0.1"
WorkTitle = "This is a Test"

X = DF_MusicXML(WorkTitle, ProgramID)
sopNotes = [[60, 65, 57], [59, 61, 63]]
sopDurations = [[4, 4, 8], [4, 4, 8]]
sopLyric = [["boo", "yah", "yeah"],["har", "har", "har"]]
altNotes = [[60, 65, 57], [59, 61, 63]]
altDurations = [[4, 4, 8], [4, 4, 8]]
tenNotes = [[52, 52, 49, 48], [51, 53, 56]]
tenDurations = [[4, 4, 4, 4], [4, 4, 8]]
basNotes = [[48, 46, 45, 44, 41], [47, 49, 51]]
basDurations = [[4, 4, 4, 2, 2], [4, 4, 8]]
X.writeSop(sopNotes, sopDurations, sopLyric)
X.writeAlto(altNotes, altDurations)
X.writeTenor(tenNotes, tenDurations)
X.writeBass(basNotes, basDurations)
X.endXMLFile()