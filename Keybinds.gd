extends PanelContainer

var FileSearchOpen = false

func _notification(Notification):
	if Notification == NOTIFICATION_WM_CLOSE_REQUEST:
		if Globals.SourceFile != null:
			Globals.SourceFile.close()

func _process(Delta):
	if FileSearchOpen == true and Input.is_action_just_released("Accept"):
		var PotentialExampleFile = Globals.ExamplesFilePath + "\\" + %LineEdit.text
		if FileAccess.file_exists(PotentialExampleFile):
			print("Opening: ", PotentialExampleFile)
			Globals.CurrentlyOpenFileName = PotentialExampleFile
			Globals.SourceFile = FileAccess.open(PotentialExampleFile, FileAccess.READ_WRITE)
			%Code.text = Globals.SourceFile.get_as_text()
			Globals.SourceFile.close()
			Toggle_Search()
	if Input.is_action_just_released("FileSearch"):
		Toggle_Search()
	if Input.is_action_just_released("Save"):
		Globals.Save_File()

func Toggle_Search():
	if FileSearchOpen == false:
		FileSearchOpen = true
		%LineEdit.visible = true
		%LineEdit.grab_focus()
	else:
		FileSearchOpen = false
		%LineEdit.visible = false
		%Code.grab_focus()
