# Yo, I just need to state now, I'm really not a fan of wildcard imports, but you think I'm going to going through every function?
# I feel like this is a very Pythonic way of pointing out that .h files suck duck feet.
# Moving on, I guess

from raylibpy import *

from os import listdir as List_Directory
from sys import exit as Exit

# API Related Functions #
def Set_Background_Color(): Background["Color"] = Color(Background["Red"], Background["Blue"], Background["Green"])


# Technically all of these are usable within in ExoFyle config files, and I'm not saying you should or shouldn', but uh, let's consider this a hazard sign#
def Load_All_Packages():
    # TO DO: yo, we can't allow for anyone to import anything else.
    # I think that will be the easiest way to secure the api up front, and then I'll implement more along the way.
    print("Loading Packages")
    for PackageFile in List_Directory("Packages"):
        with open("Packages/" + PackageFile, 'r') as PackageFile:
            PackageFileInstructions = [Line for Line in PackageFile.readlines()]
            ScriptContent = [Instruction for Instruction in PackageFileInstructions]
            Instructions = "\n".join(ScriptContent).replace("from Source.ExoFyle import *\n", "")
            if Is_Legal_Script(Instructions) == False:
                return
            exec(Instructions)



def Is_Legal_Script(UserInstruction:str) -> bool:
    for Instruction in InvalidInstructions:
        if Instruction in UserInstruction:
            return False
    return True


# We have to take into account the packages within the user's folder, and whatever changes they may make when live
def Build_Frame():
    begin_drawing()
    clear_background(Background["Color"])
    end_drawing()


def Initialize():
    print("Welcome to the thunderdome bitches.")
    Set_Background_Color()
    Load_All_Packages()
    init_window(Resolution["Width"], Resolution["Height"], WindowSettings["Title"])
    set_target_fps(WindowSettings["FPS"])


def Cleanup():
    close_window()


def Handle_Input() -> None | str:
    Key: int
    Function:function
    KeyChord:int
    for Key, Function, KeyChord in InputTree:
        if is_key_pressed(Key):
            if KeyChord != None:
                if is_key_down(KeyChord) == False:
                    return f"Command Requires KeyChord {KeyChord}"
            Function()


def Handle_Control_Flow() -> bool:
    Boolean:bool = True
    Function: function
    for Function, FailType in ControlFlow:
        Boolean = Handle_Error(Function(), FailType)
        if Boolean == False:return Boolean
    return Boolean


def Handle_Error(FunctionReturn, FunctionFailType) -> bool:
    try:
        if FunctionReturn != None:
            print(f"ERROR: {FunctionReturn}")
            if FunctionFailType == "FailFast":
                Exit()
        return True
    except Exception as SomeException:
        print(f"Yo, I don't know even know what you broke:\n{SomeException}")
        return False


def Entry():
    Handle_Error(Initialize(), "FailFast")
    while not window_should_close():
        if Handle_Control_Flow() == False: break
    Handle_Error(Cleanup(), "FailFast")


# These are not top level variables, they are configurations
InvalidInstructions = [
    "Entry()",
    "Exit()",
]
Resolution = {
    "Width":800,
    "Height":600,
}
Background = {
    "DefaultRed": 34,
    "DefaultBlue": 34,
    "DefaultGreen": 34,
    "DefaultAlpha": 255,
    "Red": None,
    "Blue": None,
    "Green": None,
    "Alpha": None,
    "Color": None,
}
Background.update({
    "Red":Background["DefaultRed"],
    "Blue":Background["DefaultBlue"],
    "Green":Background["DefaultGreen"],
})
WindowSettings = {
    "Title": "ExoFyle",
    "FPS": 60,
}
KeyChords = {
    "Leader": KEY_SPACE
}
InputTree = [
    [KEY_R, Load_All_Packages, KeyChords["Leader"]],
    [KEY_Q, Exit, KeyChords["Leader"]],
]
ControlFlow = [
    [Build_Frame, "FailSafe"],
    [Handle_Input, "FailSafe"],
]

if __name__ == '__main__':
    Entry()
