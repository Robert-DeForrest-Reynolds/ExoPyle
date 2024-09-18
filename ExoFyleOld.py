from raylibpy import *
from typing import List, Dict, Callable
from os import listdir as List_Directory, sep
from os.path import join
from sys import exit as Exit
from asyncio import run, sleep


class Error:
    def __init__(Self, ErrorString:str) -> None: Self.ErrorString = ErrorString


def Get(VariableName:str): return globals().get(VariableName, None)


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
    draw_text(ApplicationConfig["StateAsString"], InterfaceDataCopy["X"], InterfaceDataCopy["Y"], InterfaceDataCopy["FontSize"], RAYWHITE)


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
    if ApplicationConfig["CurrentState"] == InsertModeControlFlow: return
    if Editor["Exposed"] == False:
        Editor["Exposed"] = True
        CoreControlFlow[0] = [lambda: Build_Frame(EditorUserInterface), "FailSafe"]
    else:
        Editor["Exposed"] = False
        CoreControlFlow[0] = [lambda: Build_Frame(HomeUserInterface), "FailSafe"]


def Load_All_Packages() -> None | Error:
    print("Loading Packages")
    if ApplicationConfig["DeveloperMode"] == True:
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
    ApplicationConfig["StateAsString"] = StateAsString[StateKey]
    ApplicationConfig["CurrentState"] = StateMapping[StateKey]


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
    ApplicationConfig["CurrentState"]()


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
    for Function, FailType in CoreControlFlow:
        print(Function)
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
    while ApplicationConfig["Alive"]:
        if Handle_Error(Handle_Control_Flow, Handle_Control_Flow(), "FailSafe") == False: break
    Handle_Error(Cleanup, Cleanup(), "FailFast")


if __name__ == '__main__':
    from sys import argv as Arguments
    if len(Arguments) >= 2 and Arguments[1] == "D": ApplicationConfig["DeveloperMode"] = True
    Entry()