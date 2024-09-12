# Yo, I just need to state now, I'm really not a fan of wildcard imports, but you think I'm going to going through every function?
# I feel like this is a very Pythonic way of pointing out that .h files suck duck feet.
# Moving on, I guess

from raylibpy import *

from os import listdir as List_Directory
from sys import exit as Exit

# Here's a bit of notes #
# A function should return None|str if error handling is necssary
# Banner Font Type: Banner3 | I recommend: https://www.asciiart.eu/text-to-ascii-art


# _____                            _____ 
#( ___ )                          ( ___ )
# |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | 
# |   |                            |   | 
# |   |     ###    ########  ####  |   | 
# |   |    ## ##   ##     ##  ##   |   | 
# |   |   ##   ##  ##     ##  ##   |   | 
# |   |  ##     ## ########   ##   |   | 
# |   |  ######### ##         ##   |   | 
# |   |  ##     ## ##         ##   |   | 
# |   |  ##     ## ##        ####  |   | 
# |   |                            |   | 
# |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| 
#(_____)                          (_____)

# API Begin #
# These Are Mostly For Quality of Life, and Ease of Use #
def Set_Background_Color():
    Background["Color"] = Color(Background["Red"], Background["Blue"], Background["Green"])


def Insert_Content_Constructor(ContentKey, ContentConstructor):
    ContentConstructors.update({ContentKey:ContentConstructor})


def Remove_Content_Constructor(ContentKey):
    ContentConstructors.pop(ContentKey)
# API End #

# _____                            _____ 
#( ___ )                          ( ___ )
# |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | 
# |   |                            |   | 
# |   |   ######   ##     ## ####  |   | 
# |   |  ##    ##  ##     ##  ##   |   | 
# |   |  ##        ##     ##  ##   |   | 
# |   |  ##   #### ##     ##  ##   |   | 
# |   |  ##    ##  ##     ##  ##   |   | 
# |   |  ##    ##  ##     ##  ##   |   | 
# |   |   ######    #######  ####  |   | 
# |   |                            |   | 
# |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| 
#(_____)                          (_____)

# A Content Constructor is just a GUI implement


def Build_Editor() -> None | str:
    EditorRectangle = Rectangle(Editor["X"], Editor["Y"], Editor["Width"], Editor["Height"])
    LineSpace = 10
    for Line in Editor["Content"]:
        draw_text(Line, 10, LineSpace, 20, RAYWHITE)
        LineSpace += 20
    draw_rectangle_rounded_lines(EditorRectangle, 0.025, 10, 2, Color(50, 255, 50, 255))
    return None


def Toggle_Editor() -> None | str:
    if Application["CurrentState"] == Insert_Mode: return
    if Editor["Exposed"] == False:
        Editor["Exposed"] = True
        Insert_Content_Constructor("Editor", [Build_Editor, "FailFast"])
    else:
        Editor["Exposed"] = False
        Remove_Content_Constructor("Editor")
    return None


def Build_Frame() -> None | str:
    begin_drawing()
    clear_background(Background["Color"])
    FailType:str
    for ContentConstructor, FailType in ContentConstructors.values():
        if Handle_Error(ContentConstructor, ContentConstructor(), FailType) == False:
            return "Failed to build frame because of broken content constructor."
    end_drawing()
    return None


# _____                                                                               _____ 
#( ___ )                                                                             ( ___ )
# |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | 
# |   |                                                                               |   | 
# |   |  ########     ###     ######  ##    ##    ###     ######   ########  ######   |   | 
# |   |  ##     ##   ## ##   ##    ## ##   ##    ## ##   ##    ##  ##       ##    ##  |   | 
# |   |  ##     ##  ##   ##  ##       ##  ##    ##   ##  ##        ##       ##        |   | 
# |   |  ########  ##     ## ##       #####    ##     ## ##   #### ######    ######   |   | 
# |   |  ##        ######### ##       ##  ##   ######### ##    ##  ##             ##  |   | 
# |   |  ##        ##     ## ##    ## ##   ##  ##     ## ##    ##  ##       ##    ##  |   | 
# |   |  ##        ##     ##  ######  ##    ## ##     ##  ######   ########  ######   |   | 
# |   |                                                                               |   | 
# |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| 
#(_____)                                                                             (_____)

def Load_All_Packages() -> None | str:
    print("Loading Packages")
    for PackageFile in List_Directory("Packages"):
        with open("Packages/" + PackageFile, 'r') as PackageFile:
            PackageFileInstructions = [Line for Line in PackageFile.readlines()]
            ScriptContent = [Instruction for Instruction in PackageFileInstructions]
            Instructions = "\n".join(ScriptContent).replace("from Source.ExoFyle import *\n", "")
            if Handle_Error(Is_Legal_Script(Instructions)) == False: exec(Instructions)
    return None


# _____                                         _____ 
#( ___ )                                       ( ___ )
# |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | 
# |   |                                         |   | 
# |   |   ######   #######  ########  ########  |   | 
# |   |  ##    ## ##     ## ##     ## ##        |   | 
# |   |  ##       ##     ## ##     ## ##        |   | 
# |   |  ##       ##     ## ########  ######    |   | 
# |   |  ##       ##     ## ##   ##   ##        |   | 
# |   |  ##    ## ##     ## ##    ##  ##        |   | 
# |   |   ######   #######  ##     ## ########  |   | 
# |   |                                         |   | 
# |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| 
#(_____)                                       (_____)


def Change_State(StateKey:int) -> None | str:
    Application["CurrentState"] = StateMapping[StateKey]


def Insert_Mode() -> None | str:
    Key = Handle_Key_Press(InsertModeInputTree)
    print(type(Key))
    if type(Key) == int:
        print(Key.encode())


def Normal_Mode() -> None | str:
    Handle_Key_Press(NormalModeInputTree)


def Handle_Key_Press(InputTree) -> None | str | int:
    Key: int
    KeyChord:int
    for Key, Function, KeyChord in InputTree:
        if is_key_pressed(Key):
            if KeyChord != None:
                if is_key_down(KeyChord) == False: return f"Command Requires KeyChord {KeyChord}"
            Function()
            return Key
    return None


def Handle_Input() -> None | str:
    Application["CurrentState"]()


def Handle_Error(FunctionSignature, FunctionReturn, FunctionFailType) -> bool:
    try:
        if FunctionReturn is not None:
            print(f"Error from {FunctionSignature}: {FunctionReturn}")
            if FunctionFailType == "FailFast":
                Exit()
        return True
    except Exception as SomeException:
        print(f"Yo, I don't know even know what you broke:\n{SomeException}")
        return False


def Is_Legal_Script(UserInstruction:str) -> None | str:
    for Instruction in InvalidInstructions:
        if Instruction in UserInstruction: return "Illegal Script"
    return None


# _____                                                                                                               _____ 
#( ___ )                                                                                                             ( ___ )
# |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | 
# |   |                                                                                                               |   | 
# |   |   ######   #######  ##    ## ######## ########   #######  ##          ######## ##        #######  ##      ##  |   | 
# |   |  ##    ## ##     ## ###   ##    ##    ##     ## ##     ## ##          ##       ##       ##     ## ##  ##  ##  |   | 
# |   |  ##       ##     ## ####  ##    ##    ##     ## ##     ## ##          ##       ##       ##     ## ##  ##  ##  |   | 
# |   |  ##       ##     ## ## ## ##    ##    ########  ##     ## ##          ######   ##       ##     ## ##  ##  ##  |   | 
# |   |  ##       ##     ## ##  ####    ##    ##   ##   ##     ## ##          ##       ##       ##     ## ##  ##  ##  |   | 
# |   |  ##    ## ##     ## ##   ###    ##    ##    ##  ##     ## ##          ##       ##       ##     ## ##  ##  ##  |   | 
# |   |   ######   #######  ##    ##    ##    ##     ##  #######  ########    ##       ########  #######   ###  ###   |   | 
# |   |                                                                                                               |   | 
# |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| 
#(_____)                                                                                                             (_____)

def Handle_Control_Flow() -> None | str:
    Boolean:bool = True
    Function: function
    for Function, FailType in ControlFlow:
        Boolean = Handle_Error(Function, Function(), FailType)
        if Boolean == False:
            return f"Control flow interrupted by {Function} error"
    return None


def Initialize() -> None | str:
    set_trace_log_level(LOG_ERROR)
    print("Welcome to the thunderdome bitches.")
    Set_Background_Color()
    Load_All_Packages()
    init_window(Resolution["Width"], Resolution["Height"], Window["Title"])
    set_target_fps(Window["FPS"])
    return None


def Cleanup() -> None | str:
    close_window()


def Entry():
    Handle_Error(Initialize, Initialize(), "FailFast")
    while Application["Alive"]:
        if Handle_Error(Handle_Control_Flow, Handle_Control_Flow(), "FailSafe") == False: break
    Handle_Error(Cleanup, Cleanup(), "FailFast")


#  _____                                                       _____ 
# ( ___ )                                                     ( ___ )
#  |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | 
#  |   |                                                       |   | 
#  |   |   ######   #######  ##    ## ######## ####  ######    |   | 
#  |   |  ##    ## ##     ## ###   ## ##        ##  ##    ##   |   | 
#  |   |  ##       ##     ## ####  ## ##        ##  ##         |   | 
#  |   |  ##       ##     ## ## ## ## ######    ##  ##   ####  |   | 
#  |   |  ##       ##     ## ##  #### ##        ##  ##    ##   |   | 
#  |   |  ##    ## ##     ## ##   ### ##        ##  ##    ##   |   | 
#  |   |   ######   #######  ##    ## ##       ####  ######    |   | 
#  |   |                                                       |   | 
#  |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| 
# (_____)                                                     (_____)
# Config Begin #
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
Application = {
    "Alive":True,
    "CurrentState":Normal_Mode,
}
Window = {
    "Title": "ExoFyle",
    "FPS": 60,
    "NaturalPadding":5,
}
StateMapping = {
    0:Normal_Mode,
    1:Insert_Mode,
}
KeyChords = {
    "Leader": KEY_SPACE
}
NormalModeInputTree = [
    [KEY_R, Load_All_Packages, KeyChords["Leader"]],
    [KEY_Q, Exit, KeyChords["Leader"]],
    [KEY_E, Toggle_Editor, None],
    [KEY_I, lambda: Change_State(1), None],
]
InsertModeInputTree = [
    [KEY_ESCAPE, lambda: Change_State(0), None],
]
ContentConstructors = {

}
ControlFlow = [
    [Build_Frame, "FailSafe"],
    [Handle_Input, "FailSafe"],
]
Editor = {
    "Exposed": False,
    "Content": [],
    "X": Window["NaturalPadding"]/2,
    "Y":  Window["NaturalPadding"]/2,
    "Width": Resolution["Width"] - Window["NaturalPadding"],
    "Height": Resolution["Height"] - Window["NaturalPadding"],
}
# Config End #
if __name__ == '__main__':
    Entry()