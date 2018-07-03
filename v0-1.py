from DF_MusicXML import *

ProgramID = "Test_code v 0.1"
WorkTitle = "This is a Test"

X = DF_MusicXML(WorkTitle, ProgramID)
X.addNote()
X.addMeasure()
X.addNote()
X.endXMLFile()