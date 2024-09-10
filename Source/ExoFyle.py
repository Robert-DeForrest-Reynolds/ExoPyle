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

# These Are Mostly For Quality of Life, and Ease of Use #
def Set_Background_Color() -> None:
    Background["Color"] = Color(Background["Red"], Background["Blue"], Background["Green"])


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
def Insert_Content_Constructor(ContentKey:str, ContentConstructor) -> None:
    ContentConstructors.update({ContentKey:ContentConstructor})


def Remove_Content_Constructor(ContentKey:str) -> None:
    ContentConstructors.pop(ContentKey)


def Build_Editor() -> None | str:
    EditorRectangle = Rectangle(Editor["X"], Editor["Y"], Editor["Width"], Editor["Height"])
    LineSpace = 10
    for Line in Editor["Content"]:
        draw_text(Line, 10, LineSpace, 20, RAYWHITE)
        LineSpace += 20
    draw_rectangle_rounded_lines(EditorRectangle, 0.025, 10, 2, Color(50, 255, 50, 255))


def Toggle_Editor():
    if WindowSettings["EditorExposed"] == False:
        WindowSettings["EditorExposed"] = True
        Insert_Content_Constructor("Editor", [Build_Editor, "FailFast"])
    else:
        WindowSettings["EditorExposed"] = False
        Remove_Content_Constructor("Editor")


def Build_Frame():
    begin_drawing()
    clear_background(Background["Color"])
    Boolean:bool = True
    ContentConstructor: function
    for ContentConstructor, FailType in ContentConstructors.values():
        Boolean = Handle_Error(ContentConstructor(), FailType)
        if Boolean == False:return Boolean
    end_drawing()
    return Boolean

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

def Load_All_Packages():
    print("Loading Packages")
    for PackageFile in List_Directory("Packages"):
        with open("Packages/" + PackageFile, 'r') as PackageFile:
            PackageFileInstructions = [Line for Line in PackageFile.readlines()]
            ScriptContent = [Instruction for Instruction in PackageFileInstructions]
            Instructions = "\n".join(ScriptContent).replace("from Source.ExoFyle import *\n", "")
            if Is_Legal_Script(Instructions) == False:
                return
            exec(Instructions)


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


def Handle_Error(FunctionReturn, FunctionFailType) -> bool:
    try:
        if type(FunctionReturn) == None:
            print(f"ERROR: {FunctionReturn}")
            if FunctionFailType == "FailFast":
                Exit()
        return True
    except Exception as SomeException:
        print(f"Yo, I don't know even know what you broke:\n{SomeException}")
        return False


def Is_Legal_Script(UserInstruction:str) -> bool:
    for Instruction in InvalidInstructions:
        if Instruction in UserInstruction:
            return False
    return True


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

def Handle_Control_Flow() -> bool:
    Boolean:bool = True
    Function: function
    for Function, FailType in ControlFlow:
        Boolean = Handle_Error(Function(), FailType)
        if Boolean == False:return Boolean
    return Boolean


def Initialize():
    set_trace_log_level(LOG_ERROR)
    print("Welcome to the thunderdome bitches.")
    Set_Background_Color()
    Load_All_Packages()
    init_window(Resolution["Width"], Resolution["Height"], WindowSettings["Title"])
    set_target_fps(WindowSettings["FPS"])


def Cleanup():
    close_window()


def Entry():
    Handle_Error(Initialize(), "FailFast")
    while not window_should_close():
        if Handle_Control_Flow() == False: break
    Handle_Error(Cleanup(), "FailFast")


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
    "NaturalPadding":5,
    "EditorExposed":False,
}
KeyChords = {
    "Leader": KEY_SPACE
}
InputTree = [
    [KEY_R, Load_All_Packages, KeyChords["Leader"]],
    [KEY_Q, Exit, KeyChords["Leader"]],
    [KEY_E, lambda: Toggle_Editor(), None]
]
ContentConstructors = {
    
}
ControlFlow = [
    [Build_Frame, "FailSafe"],
    [Handle_Input, "FailSafe"],
]
Editor = {
    "Content": [],
    "X": WindowSettings["NaturalPadding"]/2,
    "Y":  WindowSettings["NaturalPadding"]/2,
    "Width": Resolution["Width"] - WindowSettings["NaturalPadding"],
    "Height": Resolution["Height"] - WindowSettings["NaturalPadding"],
}
if __name__ == '__main__':
    Entry()
