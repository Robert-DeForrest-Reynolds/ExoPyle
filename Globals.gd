extends Node

var ExamplesFilePath = "C:\\Users\\rldre\\Documents\\GitHub\\EliJ\\Examples"
var CurrentlyOpenFileName = ""
var SourceFile:FileAccess = null


func Save_File():
	if CurrentlyOpenFileName != "":
		SourceFile = FileAccess.open(CurrentlyOpenFileName, FileAccess.WRITE)
		SourceFile.store_string($/root/ExoFyle.get_node("%Code").text)
		SourceFile.close()
