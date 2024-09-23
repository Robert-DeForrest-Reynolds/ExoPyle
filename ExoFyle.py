from raylibpy import *
from typing import Callable
from os import listdir
from os.path import join



"""
 _____                  _____ 
( ___ )----------------( ___ )
 |   |                  |   | 
 |   |       API        |   | 
 |___|                  |___| 
(_____)----------------(_____)
"""
class Error:
    def __init__(_, Signature:Callable, ErrorString:str, Warning=False) -> None:
        if Warning == False:
            Output(f"Error: {ErrorString} FROM: {Signature}")
            exit()
        else:
            Output(f"Warning: {ErrorString} FROM: {Signature}")


class Call:
    def __init__(_, Function:Callable, ArgumentKeys:list=None) -> None:
        _.Function:Callable = Function
        _.ArgumentKeys:list = ArgumentKeys

    def Call(_) -> Callable:
        if _.ArgumentKeys == None:
            _.Lambda:Callable = lambda: _.Function()
        else:
            _.LambdaArguments = [Get(Argument) for Argument in _.ArgumentKeys]
            _.Lambda:Callable = lambda: _.Function(*_.LambdaArguments)
        return _.Lambda()

    
def Get(GlobalName:str) -> object | Error:
    Variable = ApplicationConfig["Globals"].get(GlobalName, None)
    if Variable == None:
        return Error(Get, f"Could not find {GlobalName}")
    return Variable


def Output(Message:str):
    print(Message) # I'm tired of looking for random fucking print statements.
                   # If I ctrl-f and find more than one print, I will fucking piledrive you. <3


def Set_Background_Color() -> Callable | Error:
    global Background
    if None in [Background["Red"], Background["Blue"], Background["Green"], Background["Alpha"]]:
        Background["Color"] = Color(Background["DefaultRed"], Background["DefaultBlue"], Background["DefaultGreen"], Background["DefaultAlpha"])
    else:
        Background["Color"] = Color(Background["Red"], Background["Blue"], Background["Green"], Background["Alpha"])
    return Set_Background_Color



"""
 _____                  _____ 
( ___ )----------------( ___ )
 |   |                  |   | 
 |   |  Frame Building  |   | 
 |___|                  |___| 
(_____)----------------(_____)
"""
def Add_To_Render_Cycle(ComponentBuilder:Callable) -> Callable | Error:
    GUI.append(ComponentBuilder)
    return Add_To_Render_Cycle

def Build_Frame() -> Callable | Error:
    begin_drawing()
    Set_Background_Color()
    clear_background(Background["Color"])
    Component_Builder:Callable
    for Component_Builder in GUI:
        Component_Builder()
    end_drawing()
    return Build_Frame



"""
 _____                  _____ 
( ___ )----------------( ___ )
 |   |                  |   | 
 |   |  State Handling  |   | 
 |___|                  |___| 
(_____)----------------(_____)
"""
def Handle_State() -> Callable | Error:
    global ApplicationConfig
    State: Call = ApplicationConfig["CurrentState"]
    State.Call()
    return Handle_State


def Change_State(StateKey:int) -> Callable | Error:
    global ApplicationConfig
    ApplicationConfig["StateAsString"] = StateAsString[StateKey]
    ApplicationConfig["CurrentState"] = StateMapping[StateKey]
    return Change_State


def Handle_Control_Flow(ControlFlow:list) -> Callable | Error:
    Function: Call
    for Function in ControlFlow:
        Function.Call()
    return Handle_Control_Flow


def Handle_Key_Press(InputTree:list) -> Callable | Error:
    Key: int
    Function:Call
    KeyChord:int
    for Key, Function, KeyChord in InputTree:
        if is_key_pressed(Key):
            if KeyChord != None:
                if is_key_down(KeyChord) == False:
                    return Error(Handle_Key_Press, f"Command Requires KeyChord {KeyChord}", Warning=True)
            Function.Call()
            return Handle_Key_Press



"""
 _____                  _____ 
( ___ )----------------( ___ )
 |   |                  |   | 
 |   |       Entry      |   | 
 |___|                  |___| 
(_____)----------------(_____)
"""
def Initialize():
    ApplicationConfig["Globals"] = globals()
    set_trace_log_level(LOG_ERROR)
    Set_Background_Color()
    Load_All_Packages()
    set_config_flags(FLAG_BORDERLESS_WINDOWED_MODE | FLAG_WINDOW_UNDECORATED)
    init_window(Resolution["Width"], Resolution["Height"], Window["Title"])
    set_target_fps(Window["FPS"])
    set_window_size(Resolution["Width"], Resolution["Height"])


def Entry():
    Initialize()
    while ApplicationConfig["Alive"]:
        Handle_Control_Flow(Get("CoreControlFlow"))
    close_window()



"""
 _____                  _____ 
( ___ )----------------( ___ )
 |   |                  |   | 
 |   |     Packages     |   | 
 |___|                  |___| 
(_____)----------------(_____)
"""
InvalidInstructions = [
    "Entry()",
    "Exit()",
]


def Is_Legal_Script(UserInstruction:str) -> bool | Error:
    global InvalidInstructions
    for Instruction in InvalidInstructions:
        if Instruction in UserInstruction:
            Error("Illegal Script", Warning=True)
            return False
    return True


def Load_All_Packages():
    Output("Loading Packages")
    PackageDirectory = "Packages"
    for PackageFile in listdir(PackageDirectory):
        with open(join(PackageDirectory, PackageFile), 'r') as PackageFile:
            PackageFileInstructions = [Line for Line in PackageFile.readlines()]
            ScriptContent = [Instruction for Instruction in PackageFileInstructions]
            Instructions = "\n".join(ScriptContent).replace("from Source.ExoFyle import *\n", "")
            if Is_Legal_Script(Instructions) == True:
                Output(f"Successfully importing: {PackageFile.name}")
                exec(Instructions, globals())
                ApplicationConfig["Globals"] = globals()



"""
 _____                  _____ 
( ___ )----------------( ___ )
 |   |                  |   | 
 |   |   Configuration  |   | 
 |___|                  |___| 
(_____)----------------(_____)
"""
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

ApplicationConfig = {
    "DeveloperMode":False,
    "Alive":True,
    "StateAsString":"Normal",
    "CurrentState": Call(Handle_Control_Flow, ["NormalModeControlFlow"]),
    "Buffer":"",
    "Globals":{},
}

Window = {
    "Title": "ExoFyle",
    "FPS": 60,
    "NaturalPadding":10,
}

StateAsString = {
    0:"Normal",
    1:"Insert",
    2:"Prompt",
    3:"FileNameInput"
}
GUI = []

StateMapping = {
    0: Call(Handle_Control_Flow, ["NormalModeControlFlow"]),
    1: Call(Handle_Control_Flow, ["InsertModeControlFlow"]),
    2: Call(Handle_Control_Flow, ["PromptModeControlFlow"]),
}

KeyChordRoots = {
    "Leader": KEY_SPACE,
}

CoreControlFlow = [
    Call(Build_Frame),
    Call(Handle_State),
]

NormalModeControlFlow = [
    Call(Handle_Key_Press, ["NormalModeInputTree"])
]

InsertModeInputTree = [
    [KEY_ESCAPE, Call(Change_State, [0])],
]

PromptModeInputTree = [
    [KEY_ESCAPE, Call(Change_State, [0])],
]

FileNameModeInputTree = [
    [KEY_ESCAPE, Call(Change_State, [0])],
]

NormalModeInputTree = [
    [KEY_Q, Call(exit), KeyChordRoots["Leader"]],
    [KEY_I, Call(Add_To_Render_Cycle, ["Build_Editor"]), None],
]

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
    KEY_ZERO: '0',
    KEY_ONE: '1',
    KEY_TWO: '2',
    KEY_THREE: '3',
    KEY_FOUR: '4',
    KEY_FIVE: '5',
    KEY_SIX: '6',
    KEY_SEVEN: '7',
    KEY_EIGHT: '8',
    KEY_NINE: '9',
    KEY_SPACE: ' ',
    KEY_PERIOD: '.',
    KEY_COMMA: ',',
    KEY_APOSTROPHE: "'",
    KEY_SEMICOLON: ';',
    KEY_SLASH: '/',
    KEY_BACKSLASH: '\\',
    KEY_LEFT_BRACKET: '[',
    KEY_RIGHT_BRACKET: ']',
    KEY_MINUS: '-',
    KEY_EQUAL: '=',
    KEY_ENTER: '\n',
    KEY_TAB: '\t',
    KEY_GRAVE: '`',
}
KeyChordMaps = {
    KEY_NINE: "(",
    KEY_ZERO: ")",
    KEY_ONE: "!",
    KEY_TWO: "@",
    KEY_THREE: "#",
    KEY_FOUR: "$",
    KEY_FIVE: "%",
    KEY_SIX: "^",
    KEY_SEVEN: "&",
    KEY_EIGHT: "*",
    KEY_EQUAL: "+",
    KEY_MINUS: "_",
    KEY_LEFT_BRACKET: "{",
    KEY_RIGHT_BRACKET: "}",
    KEY_BACKSLASH: "|",
    KEY_SEMICOLON: ":",
    KEY_APOSTROPHE: '"',
    KEY_COMMA: "<",
    KEY_PERIOD: ">",
    KEY_SLASH: "?",
    KEY_GRAVE: "~",
    KEY_A: "A",
    KEY_B: "B",
    KEY_C: "C",
    KEY_D: "D",
    KEY_E: "E",
    KEY_F: "F",
    KEY_G: "G",
    KEY_H: "H",
    KEY_I: "I",
    KEY_J: "J",
    KEY_K: "K",
    KEY_L: "L",
    KEY_M: "M",
    KEY_N: "N",
    KEY_O: "O",
    KEY_P: "P",
    KEY_Q: "Q",
    KEY_R: "R",
    KEY_S: "S",
    KEY_T: "T",
    KEY_U: "U",
    KEY_V: "V",
    KEY_W: "W",
    KEY_X: "X",
    KEY_Y: "Y",
    KEY_Z: "Z",
}



"""
 _____                  _____ 
( ___ )----------------( ___ )
 |   |                  |   | 
 |   |     Additives    |   | 
 |___|                  |___| 
(_____)----------------(_____)
"""
Editor = {
    "Exposed": False,
    "Content": [""],
    "CurrentLine": 0,
    "FontSize": 16,
    "CurrentFileName": None,
    "X": Window["NaturalPadding"]/2,
    "Y":  Window["NaturalPadding"]/2,
    "Width": Resolution["Width"] - Window["NaturalPadding"],
    "Height": Resolution["Height"] - Window["NaturalPadding"],
    "Resizable": True,
    "Position":"Relative",
}


def Build_Editor() -> None | Error:
    EditorRectangle = Rectangle(Editor["X"], Editor["Y"], Editor["Width"], Editor["Height"])
    LineSpace:int = 10
    Line:str
    for Line in Editor["Content"]:
        draw_text(Line, 10, LineSpace, Editor["FontSize"], RAYWHITE)
        LineSpace += 20
    draw_rectangle_rounded_lines(EditorRectangle, 0.025, 10, 2, Color(50, 255, 50, 255))



if __name__ == "__main__":
    Output("Welcome to the thunderdome bitches.")
    Entry()