from Field_D_SupportingClasses import *

ProgramID = "DF Word Score Sonifier v1.0"
WorkTitle = "Untitled Sonification"
Lyricist = ""

Input = DF_TextInput()
WorkTitle = Input.provideTitle()
Lyricist = Input.provideLyricist()
verses = Input.provideVerses()
positions = Input.providePositions()
scores = Input.provideScrabbleScores()
Planner = DF_SongPlanner(verses, positions, scores)
verseKeys =  Planner.getVerseKeys()
Planner.getBassPart(Planner.homeKey)
Planner.getTenorPart(Planner.homeKey)
Planner.getAltoPart(Planner.homeKey)
Planner.getSopPart(Planner.homeKey)

X = DF_MusicXML(WorkTitle, ProgramID, Lyricist)
basNotes = Planner.bassNotes
basDurations = Planner.bassRhythms
basLyric = Planner.bassWords
basPos = Planner.bassPositions
basTies = Planner.bassTies
tenNotes = Planner.tenNotes
tenDurations = Planner.tenRhythms
tenLyric = Planner.tenWords
tenPos = Planner.tenPositions
tenTies = Planner.tenTies
altoNotes = Planner.altoNotes
altoDurations = Planner.altoRhythms
altoLyric = Planner.altoWords
altoPos = Planner.altoPositions
altoTies = Planner.altoTies
sopNotes = Planner.sopNotes
sopDurations = Planner.sopRhythms
sopLyric = Planner.sopWords
sopPos = Planner.sopPositions
sopTies = Planner.sopTies
X.writeSop(sopNotes, sopDurations, sopLyric, sopPos, sopTies)
X.writeAlto(altoNotes, altoDurations, altoLyric, altoPos, altoTies)
X.writeTenor(tenNotes, tenDurations, tenLyric, tenPos, tenTies)
X.writeBass(basNotes, basDurations, basLyric, basPos, basTies)
X.endXMLFile()