# Yo, I just need to state now, I'm really not a fan of wildcard imports, but you think I'm going to going through every function?
# I feel like this is a very Pythonic way of pointing out that .h files suck duck feet.
# Moving on, I guess

from raylibpy import *

from typing import List, Dict, Callable
from os import listdir as List_Directory, sep
from os.path import join
from sys import exit as Exit
from asyncio import run, sleep


class Error:
    def __init__(Self, ErrorString:str) -> None: Self.ErrorString = ErrorString


def Set_Background_Color() -> None | Error:
    if None in [Background["Red"], Background["Blue"], Background["Green"], Background["Alpha"]]:
        Background["Color"] = Color(Background["DefaultRed"], Background["DefaultBlue"], Background["DefaultGreen"])
    else:
        Background["Color"] = Color(Background["Red"], Background["Blue"], Background["Green"])


def Insert_User_Interface(Interface:Dict, ContentKey, InterfaceComponent):
    Interface.update({ContentKey:InterfaceComponent})


def Remove_User_Interface(Interface, ContentKey):
    Interface.pop(ContentKey)


def Build_FileName_Prompt() -> None | Error:
    PromptRectangle = Rectangle(FileNamePrompt["X"], FileNamePrompt["Y"], FileNamePrompt["Width"], FileNamePrompt["Height"])
    draw_rectangle_rounded_lines(PromptRectangle, 0.025, 10, 2, Color(50, 255, 50, 255))
    draw_rectangle(FileNamePrompt["X"], FileNamePrompt["Y"], FileNamePrompt["Width"], FileNamePrompt["Height"], Color(255, 0, 0, 0))
    draw_text(FileNamePrompt["Content"], FileNamePrompt["X"], FileNamePrompt["Y"], FileNamePrompt["FontSize"], RAYWHITE)


def Build_InfoBar(InterfaceDataCopy) -> None | Error:
    draw_text(Application["StateAsString"], InterfaceDataCopy["X"], InterfaceDataCopy["Y"], InterfaceDataCopy["FontSize"], RAYWHITE)


def Build_Prompt(InterfaceDataCopy) -> None | Error:
    draw_text(Prompt["Content"], InterfaceDataCopy["X"], InterfaceDataCopy["Y"], InterfaceDataCopy["FontSize"], RAYWHITE)


def Build_Editor(InterfaceDataCopy) -> None | Error:
    EditorRectangle = Rectangle(InterfaceDataCopy["X"], InterfaceDataCopy["Y"], InterfaceDataCopy["Width"], InterfaceDataCopy["Height"])
    LineSpace:int = 10
    Line:str
    for Line in Editor["Content"]:
        draw_text(Line, 10, LineSpace, InterfaceDataCopy["FontSize"], RAYWHITE)
        LineSpace += 20
    draw_rectangle_rounded_lines(EditorRectangle, 0.025, 10, 2, Color(50, 255, 50, 255))


def Toggle_Editor() -> None | Error:
    if Application["CurrentState"] == InsertModeControlFlow: return
    if Editor["Exposed"] == False:
        Editor["Exposed"] = True
        ControlFlow[0] = [lambda: Build_Frame(EditorUserInterface), "FailSafe"]
    else:
        Editor["Exposed"] = False
        ControlFlow[0] = [lambda: Build_Frame(HomeUserInterface), "FailSafe"]


def Load_All_Packages() -> None | Error:
    print("Loading Packages")
    if Application["DeveloperMode"] == True:
        PackageDirectory = join("C", sep, "ExoFyle", "Packages")
    else:
        
        PackageDirectory = "Packages"
    for PackageFile in List_Directory(PackageDirectory):
        with open(join(PackageDirectory, PackageFile), 'r') as PackageFile:
            PackageFileInstructions = [Line for Line in PackageFile.readlines()]
            ScriptContent = [Instruction for Instruction in PackageFileInstructions]
            Instructions = "\n".join(ScriptContent).replace("from Source.ExoFyle import *\n", "")
            if Handle_Error(Is_Legal_Script(Instructions)) == False: exec(Instructions)


def Build_Frame(InterfaceType:Dict) -> None | Error:
    begin_drawing()
    clear_background(Background["Color"])
    Rendered = []
    Index:int
    InterfaceData:Dict
    InterfaceBuilder:Callable
    FailType:str
    for Index, (InterfaceData, InterfaceBuilder, FailType) in enumerate(InterfaceType.values()):
        RenderedCount = len(Rendered)
        InterfaceDataCopy = {Key:Value for Key, Value in InterfaceData.items()}
        if InterfaceData["Resizable"] == True:
            if len(InterfaceType.values()) > 1:
                FutureInterface:List
                for FutureInterface in [Value for Value in InterfaceType.values()][Index+1:]:
                    FutureInterfaceData:Dict = FutureInterface[0]
                    InterfaceDataCopy["Height"] -= FutureInterfaceData["Height"]
        if InterfaceDataCopy["Y"] == None:
            InterfaceDataCopy["Y"] = Window["NaturalPadding"]
            if RenderedCount > 0:
                for RenderedInterface in Rendered:
                    if RenderedInterface["Y"] > InterfaceDataCopy["Y"]:
                        InterfaceDataCopy["Y"] -= RenderedInterface["Height"]
                    else:
                        InterfaceDataCopy["Y"] += RenderedInterface["Height"]
        elif InterfaceDataCopy["Y"] == -1:
            InterfaceDataCopy["Y"] = Resolution["Height"] - InterfaceDataCopy["Height"]
        if InterfaceDataCopy["Position"] == "Absolute":
            Rectangle = Handle_Error(InterfaceBuilder, InterfaceBuilder(), FailType)
        else:
            Rectangle = Handle_Error(InterfaceBuilder, InterfaceBuilder(InterfaceDataCopy), FailType)
        if Rectangle == False:
            return Error("Failed to build frame because of broken content constructor.")
        Rendered.append(InterfaceDataCopy)
    end_drawing()


def Change_State(StateKey:int) -> None | Error:
    if StateKey == 1 and Editor["Exposed"] == False: return
    Application["StateAsString"] = StateAsString[StateKey]
    Application["CurrentState"] = StateMapping[StateKey]


def Submit_Command() -> None | Error:
    Prompt["Content"] = ""


async def Backspace_Cooldown():
    Editor["Backspace"] = 0
    await sleep(0.1)
    Editor["Backspace"] = 1


def Input_SingleLine_Key(UserInterface, InputTree) -> None | Error:
    if is_key_down(KEY_BACKSPACE):
        if UserInterface["Backspace"] == 0:return
        if UserInterface["Content"] != "":
            run(Backspace_Cooldown())
            UserInterface["Content"] = Editor["Content"][:-1]
        return None
    Key = get_key_pressed()
    if Key in KeyMap.keys():
        UserInterface["Content"] += KeyMap[Key]
    else:
        Handle_Key_Press(InputTree)


def Input_MultiLine_Key(InputTree) -> None | Error:
    if is_key_down(KEY_BACKSPACE):
        if Editor["Backspace"] == 0:return
        if Editor["Content"][Editor["CurrentLine"]] != "":
            run(Backspace_Cooldown())
            Editor["Content"][Editor["CurrentLine"]] = Editor["Content"][Editor["CurrentLine"]][:-1]
            LineSize = measure_text(Editor["Content"][Editor["CurrentLine"]], Editor["FontSize"])
        return None
    Key = get_key_pressed()
    if Key == KEY_LEFT_SHIFT or Key == KEY_RIGHT_SHIFT:return None
    if Key in KeyMap.keys():
        if is_key_down(KEY_LEFT_SHIFT) or is_key_down(KEY_RIGHT_SHIFT):
            if Key in KeyChordMaps:
                Key = KeyChordMaps[Key]
        else:
            Key = KeyMap[Key]
        Editor["Content"][Editor["CurrentLine"]] += Key
        LineSize = measure_text(Editor["Content"][Editor["CurrentLine"]], Editor["FontSize"])
        if LineSize >= Editor["Width"] - 20:
            Editor["Content"].append("")
            Editor["CurrentLine"] += 1
        elif LineSize <= 0:
            Editor["Content"] = Editor["Content"][:-1]
            Editor["CurrentLine"] -= 1
    else:
        Handle_Key_Press(InputTree)


def Handle_Mode_Control_Flow(ControlFlow:List[List], InputTree) -> None | Error:
    Function:Callable
    FailType:str
    for Function, FailType in ControlFlow:
        Handle_Error(Function, Function(InputTree), FailType)
    return ControlFlow


def Handle_Key_Press(InputTree) -> None | Error | int:
    Key: int
    Function:Callable
    KeyChord:int
    for Key, Function, KeyChord in InputTree:
        if is_key_pressed(Key):
            if KeyChord != None:
                if is_key_down(KeyChord) == False: return Error(f"Command Requires KeyChord {KeyChord}")
            Function()


def Handle_Input() -> None | Error:
    Application["CurrentState"]()


# Handle error is to be used for core control flow error checking.
# Anything outside of the core control flow is to be manage with None | Error return.
# This is to abstract away the handling of the core control flow from the user space.
# Only the developers should have to worry about the core breaking, how, and why.
# Users should user the Error return value that will be caught during the core contorl flow
#                   FailSafe = don't crash | FailFast = crash
# If a build is released with core bugs, it is on the developer to investigate, not the user.
def Handle_Error(FunctionSignature, FunctionReturn, FunctionFailType) -> bool:
    try:
        if type(FunctionReturn) == Error:
            print(f"Error from {FunctionSignature}: {FunctionReturn.ErrorString}")
            if FunctionFailType == "FailFast":
                Exit()
        return True
    except Exception as SomeException:
        print(f"Yo, I don't know even know what you broke:\n{SomeException}")
        return False


def Is_Legal_Script(UserInstruction:str) -> None | Error:
    for Instruction in InvalidInstructions:
        if Instruction in UserInstruction: return Error("Illegal Script")


def Save_File() -> None | Error:
    if Editor["Exposed"] == False: return None
    if Editor["CurrentFileName"] == None:
        EditorUserInterface.update({"FileNamePrompt":[FileNamePrompt, Build_FileName_Prompt, "FailFast"]})
        Change_State(3)


def Open_File() -> None | Error:
    pass


def Handle_Control_Flow() -> None | Error:
    for Function, FailType in ControlFlow:
        if Handle_Error(Function, Function(), FailType) == False:
            return Error(f"Control flow interrupted by {Function} error")


def Initialize() -> None | Error:
    set_trace_log_level(LOG_ERROR)
    print("Welcome to the thunderdome bitches.")
    Set_Background_Color()
    Load_All_Packages()
    set_config_flags(FLAG_BORDERLESS_WINDOWED_MODE | FLAG_WINDOW_UNDECORATED)
    init_window(Resolution["Width"], Resolution["Height"], Window["Title"])
    set_target_fps(Window["FPS"])
    set_window_size(Resolution["Width"], Resolution["Height"])


def Cleanup() -> None | Error:
    close_window()


def Entry():
    Handle_Error(Initialize, Initialize(), "FailFast")
    while Application["Alive"]:
        if Handle_Error(Handle_Control_Flow, Handle_Control_Flow(), "FailSafe") == False: break
    Handle_Error(Cleanup, Cleanup(), "FailFast")


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
Application = {
    "DeveloperMode":False,
    "Alive":True,
    "StateAsString":"Normal",
    "CurrentState":lambda: Handle_Mode_Control_Flow(NormalModeControlFlow, NormalModeInputTree),
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
    0:lambda: Handle_Mode_Control_Flow(NormalModeControlFlow, NormalModeInputTree),
    1:lambda: Handle_Mode_Control_Flow(InsertModeControlFlow, InsertModeInputTree),
    2:lambda: Handle_Mode_Control_Flow(PromptModeControlFlow, InsertModeInputTree),
    3:lambda: Handle_Mode_Control_Flow(FileNameModeControlFlow, FileNameModeInputTree),
}


KeyChordRoots = {
    "Leader": KEY_SPACE
}
NormalModeInputTree = [
    [KEY_R, Load_All_Packages, KeyChordRoots["Leader"]],
    [KEY_Q, Exit, KeyChordRoots["Leader"]],
    [KEY_E, Toggle_Editor, None],
    [KEY_S, Save_File, None],
    [KEY_O, Open_File, None],
    [KEY_I, lambda: Change_State(1), None],
    [KEY_P, lambda: Change_State(2), None],
]
InsertModeInputTree = [
    [KEY_ESCAPE, lambda: Change_State(0), None],
]
PromptModeInputTree = [
    [KEY_ESCAPE, lambda: Change_State(0), None],
    [KEY_ENTER, Submit_Command, None],
]
FileNameModeInputTree = [
    [KEY_ESCAPE, lambda: Change_State(0), None],
    [KEY_ENTER, Submit_Command, None],
]


ControlFlow = [
    [lambda: Build_Frame(HomeUserInterface), "FailSafe"],
    [Handle_Input, "FailSafe"],
]
InsertModeControlFlow = [
    [Input_MultiLine_Key, "FailSafe"]
]
NormalModeControlFlow = [
    [Handle_Key_Press, "FailSafe"]
]
PromptModeControlFlow = [
    [lambda: Input_SingleLine_Key(PromptModeControlFlow, PromptModeControlFlow), "FailSafe"]
]
FileNameModeControlFlow = [
    "",
    [lambda: Input_SingleLine_Key(FileNamePrompt, FileNameModeControlFlow), "FailSafe"]
]


FileNamePrompt = {
    "Exposed": False,
    "Content": "",
    "X": Resolution["Height"]/2 - Window["NaturalPadding"]/2,
    "Y":  Resolution["Width"]/2,
    "FontSize": 16,
    "Backspace": 1,
    "Width": 240,
    "Height": 20,
    "Resizable": False,
    "Position":"Absolute",
}
InfoBar = {
    "Exposed": True,
    "FontSize":16,
    "X": Window["NaturalPadding"]/2,
    "Y":  -1,
    "Width": Resolution["Width"] - Window["NaturalPadding"],
    "Height": 20,
    "Resizable": False,
    "Position":"Relative",
}
Prompt = {
    "Exposed": True,
    "Content": "",
    "FontSize":16,
    "Backspace": 1,
    "X": Window["NaturalPadding"]/2,
    "Y": None,
    "Width": Resolution["Width"] - Window["NaturalPadding"],
    "Height": 20,
    "Resizable": False,
    "Position":"Relative",
}
Editor = {
    "Exposed": False,
    "Content": [""],
    "CurrentLine": 0,
    "FontSize": 16,
    "Backspace": 1,
    "CurrentFileName": None,
    "X": Window["NaturalPadding"]/2,
    "Y":  Window["NaturalPadding"]/2,
    "Width": Resolution["Width"] - Window["NaturalPadding"],
    "Height": Resolution["Height"] - Window["NaturalPadding"],
    "Resizable": True,
    "Position":"Relative",
}


HomeUserInterface = {
    "Prompt": [Prompt, Build_Prompt, "FailFast"],
    "InfoBar": [InfoBar, Build_InfoBar, "FailFast"]
}
EditorUserInterface = {
    "Editor": [Editor, Build_Editor, "FailFast"],
    "Prompt": [Prompt, Build_Prompt, "FailFast"],
    "InfoBar": [InfoBar, Build_InfoBar, "FailFast"],
}
Rendered = []


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


if __name__ == '__main__':
    from sys import argv as Arguments
    if len(Arguments) >= 2 and Arguments[1] == "D": Application["DeveloperMode"] = True
    Entry()