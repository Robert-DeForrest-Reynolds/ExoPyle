from raylibpy import *
from typing import List, Dict, Callable
from sys import exit as Exit


"""
 _____                                         _____ 
( ___ )---------------------------------------( ___ )
 |   |                                         |   | 
 |   |    #######                              |   | 
 |   |    #       #    # ##### #####  #   #    |   | 
 |   |    #       ##   #   #   #    #  # #     |   | 
 |   |    #####   # #  #   #   #    #   #      |   | 
 |   |    #       #  # #   #   #####    #      |   | 
 |   |    #       #   ##   #   #   #    #      |   | 
 |   |    ####### #    #   #   #    #   #      |   | 
 |___|                                         |___| 
(_____)---------------------------------------(_____)
"""


def Initialize():
    set_trace_log_level(LOG_ERROR)
    print("Welcome to the thunderdome bitches.")
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
 _____                                                                _____ 
( ___ )--------------------------------------------------------------( ___ )
 |   |                                                                |   | 
 |   |    ######                                                      |   | 
 |   |    #     #   ##    ####  #    #   ##    ####  ######  ####     |   | 
 |   |    #     #  #  #  #    # #   #   #  #  #    # #      #         |   | 
 |   |    ######  #    # #      ####   #    # #      #####   ####     |   | 
 |   |    #       ###### #      #  #   ###### #  ### #           #    |   | 
 |   |    #       #    # #    # #   #  #    # #    # #      #    #    |   | 
 |   |    #       #    #  ####  #    # #    #  ####  ######  ####     |   | 
 |___|                                                                |___| 
(_____)--------------------------------------------------------------(_____)
"""


def Load_All_Packages():
    print("Loading Packages")


"""
 _____                           _____ 
( ___ )-------------------------( ___ )
 |   |                           |   | 
 |   |       #    ######  ###    |   | 
 |   |      # #   #     #  #     |   | 
 |   |     #   #  #     #  #     |   | 
 |   |    #     # ######   #     |   | 
 |   |    ####### #        #     |   | 
 |   |    #     # #        #     |   | 
 |   |    #     # #       ###    |   | 
 |___|                           |___| 
(_____)-------------------------(_____)
"""


class Error:
    def __init__(_, Signature:Callable, ErrorString:str, Warning=False) -> None:
        if Warning == False:
            print(f"Error: {ErrorString} FROM: {Signature}")
            exit()
        else:
            print(f"Warning: {ErrorString} FROM: {Signature}")


class Call:
    def __init__(_, Function:Callable, ArgumentKeys:list=None) -> None:
        _.Function:Callable = Function
        _.ArgumentKeys:list = ArgumentKeys

    def Call(_) -> None:
        if _.ArgumentKeys == None:
            _.Lambda:Callable = lambda: _.Function()
        else:
            _.LambdaArguments = [Get(Argument) for Argument in _.ArgumentKeys]
            _.Lambda:Callable = lambda: _.Function(*_.LambdaArguments)
        _.Lambda()

    
def Get(GlobalName:str) -> any | Error:
    Variable = globals().get(GlobalName, None)
    if Variable == None:
        return Error(Get, f"Could not find {GlobalName}")
    return globals().get(GlobalName, None)


def Set_Background_Color() -> Callable | Error:
    if None in [Background["Red"], Background["Blue"], Background["Green"], Background["Alpha"]]:
        Background["Color"] = Color(Background["DefaultRed"], Background["DefaultBlue"], Background["DefaultGreen"])
    else:
        Background["Color"] = Color(Background["Red"], Background["Blue"], Background["Green"])
    return Set_Background_Color


def Build_Frame() -> Callable | Error:
    begin_drawing()
    clear_background(Background["Color"])
    end_drawing()
    return Build_Frame


def Handle_Key_Press(InputTree) -> Callable | Error:
    Key: int
    Function:Call
    KeyChord:int
    for Key, Function, KeyChord in InputTree:
        if is_key_pressed(Key):
            if KeyChord != None:
                if is_key_down(KeyChord) == False: return Error(Handle_Key_Press, f"Command Requires KeyChord {KeyChord}", Warning=True)
            Function.Call()
        return Handle_Key_Press


def Handle_Control_Flow(ControlFlow:List) -> Callable | Error:
    Function: Call
    for Function in ControlFlow:
        Function.Call()
    return Handle_Control_Flow


def Handle_State() -> Callable | Error:
    State: Call = ApplicationConfig["CurrentState"]
    State.Call()
    return Handle_State


def Change_State(StateKey:int) -> Callable | Error:
    ApplicationConfig["StateAsString"] = StateAsString[StateKey]
    ApplicationConfig["CurrentState"] = StateMapping[StateKey]
    return Change_State


"""
 _____                                                                                        _____ 
( ___ )--------------------------------------------------------------------------------------( ___ )
 |   |                                                                                        |   | 
 |   |     #####                                                                              |   | 
 |   |    #     #  ####  #    # ###### #  ####  #    # #####    ##   ##### #  ####  #    #    |   | 
 |   |    #       #    # ##   # #      # #    # #    # #    #  #  #    #   # #    # ##   #    |   | 
 |   |    #       #    # # #  # #####  # #      #    # #    # #    #   #   # #    # # #  #    |   | 
 |   |    #       #    # #  # # #      # #  ### #    # #####  ######   #   # #    # #  # #    |   | 
 |   |    #     # #    # #   ## #      # #    # #    # #   #  #    #   #   # #    # #   ##    |   | 
 |   |     #####   ####  #    # #      #  ####   ####  #    # #    #   #   #  ####  #    #    |   | 
 |___|                                                                                        |___| 
(_____)--------------------------------------------------------------------------------------(_____)
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

StateMapping = {
    0: Call(Handle_Control_Flow, ["NormalModeControlFlow"]),
    1: Call(Handle_Control_Flow, ["InsertModeControlFlow"]),
    2: Call(Handle_Control_Flow, ["PromptModeControlFlow"]),
    3: Call(Handle_Control_Flow, ["FileNameModeControlFlow"]),
}

KeyChordRoots = {
    "Leader": KEY_SPACE
}

NormalModeInputTree = [
    [KEY_Q, Call(Exit), KeyChordRoots["Leader"]],
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

CoreControlFlow = [
    Call(Build_Frame),
    Call(Handle_State),
]

NormalModeControlFlow = [
    Call(Handle_Key_Press, ["NormalModeInputTree"])
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


if __name__ == "__main__":
    Entry()