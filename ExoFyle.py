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


def Insert_User_Interface(ContentKey, ContentConstructor):
    UserInterface.update({ContentKey:ContentConstructor})


def Remove_User_Interface(ContentKey):
    UserInterface.pop(ContentKey)
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
        draw_text(Line, 10, LineSpace, Editor["FontSize"], RAYWHITE)
        LineSpace += 20
    draw_rectangle_rounded_lines(EditorRectangle, 0.025, 10, 2, Color(50, 255, 50, 255))
    return None


def Toggle_Editor() -> None | str:
    if Application["CurrentState"] == Insert_Mode: return
    if Editor["Exposed"] == False:
        Editor["Exposed"] = True
        Insert_User_Interface("Editor", [Build_Editor, "FailFast"])
    else:
        Editor["Exposed"] = False
        Remove_User_Interface("Editor")
    return None


def Build_Frame() -> None | str:
    begin_drawing()
    clear_background(Background["Color"])
    FailType:str
    for ContentConstructor, FailType in UserInterface.values():
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


def Input_Key() -> None | str:
    Key = get_key_pressed()
    if Key in KeyMap.keys():
        Editor["Content"][Editor["CurrentLine"]] += KeyMap[Key]
        LineSize = measure_text(Editor["Content"][Editor["CurrentLine"]], Editor["FontSize"])
        if LineSize >= Editor["Width"] - 20:
            Editor["Content"].append("")
            Editor["CurrentLine"] += 1
    else:
        Handle_Key_Press(InsertModeInputTree)
    return None


def Insert_Mode() -> None | str:
    for Function, FailType in InsertModeControlFlow:
        Handle_Error(Function, Function(), FailType)
    return None


def Normal_Mode() -> None | str:
    for Function, FailType in NormalModeControlFlow:
        Handle_Error(Function, Function(NormalModeInputTree), FailType)
    return None


def Handle_Key_Press(InputTree) -> None | str | int:
    Key: int
    KeyChord:int
    for Key, Function, KeyChord in InputTree:
        if is_key_pressed(Key):
            if KeyChord != None:
                if is_key_down(KeyChord) == False: return f"Command Requires KeyChord {KeyChord}"
            Function()
    return None


def Handle_Input() -> None | str:
    Application["CurrentState"]()

# Handle error is to be used for core control flow error checking.
# Anything outside of the core control flow is to be manage with None | str return.
# This is to abstract away the handling of the core control flow from the user space.
# Only the developers should have to worry about the core breaking, how, and why.
# If a build is released with core bugs, it is on the developer to investigate, not the user.
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
    # set_trace_log_level(LOG_ERROR)
    print("Welcome to the thunderdome bitches.")
    Set_Background_Color()
    Load_All_Packages()
    set_config_flags(FLAG_BORDERLESS_WINDOWED_MODE | FLAG_WINDOW_UNDECORATED)
    init_window(Resolution["Width"], Resolution["Height"], Window["Title"])
    set_target_fps(Window["FPS"])
    set_window_size(Resolution["Width"], Resolution["Height"])
    print(get_screen_width())
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
    "Buffer":"",
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
UserInterface = {

}
ControlFlow = [
    [Build_Frame, "FailSafe"],
    [Handle_Input, "FailSafe"],
]
InsertModeControlFlow = [
    [Input_Key, "FailSafe"]
]
NormalModeControlFlow = [
    [Handle_Key_Press, "FailSafe"]
]
Editor = {
    "Exposed": False,
    "Content": [""],
    "CurrentLine":0,
    "FontSize":16,
    "X": Window["NaturalPadding"]/2,
    "Y":  Window["NaturalPadding"]/2,
    "Width": Resolution["Width"] - Window["NaturalPadding"],
    "Height": Resolution["Height"] - Window["NaturalPadding"],
}
KeyMap = {
    KEY_A: 'a',
    KEY_B: 'b',
    KEY_C: 'c',
    KEY_D: 'd',
    KEY_E: 'e',
    KEY_F: 'f',
    KEY_G: 'g',
    KEY_H: 'h',
    KEY_I: 'i',
    KEY_J: 'j',
    KEY_K: 'k',
    KEY_L: 'l',
    KEY_M: 'm',
    KEY_N: 'n',
    KEY_O: 'o',
    KEY_P: 'p',
    KEY_Q: 'q',
    KEY_R: 'r',
    KEY_S: 's',
    KEY_T: 't',
    KEY_U: 'u',
    KEY_V: 'v',
    KEY_W: 'w',
    KEY_X: 'x',
    KEY_Y: 'y',
    KEY_Z: 'z',
    KEY_SPACE: ' ',
    KEY_ENTER: 'enter',
    KEY_BACKSPACE: 'backspace',
}
# Config End #
if __name__ == '__main__':
    Entry()