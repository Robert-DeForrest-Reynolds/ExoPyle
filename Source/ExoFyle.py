# Yo, I just need to state now, I'm really not a fan of wildcard imports, but you think I'm going to going through every function?
# I feel like this is a very Pythonic way of pointing out that .h files suck duck feet.
# Moving on, I guess

from raylibpy import *

from os import listdir
from sys import exit as Exit

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

# API Related Functions #
def Set_Background_Color(): Background["Color"] = Color(Background["Red"], Background["Blue"], Background["Green"])


# Technically all of these are usable within in ExoFyle config files, and I'm not saying you should or shouldn', but uh, let's consider this a hazard sign#
def Load_All_Packages():
    for PackageFile in listdir("Source/PackageExamples"):
        with open("Source/PackageExamples/" + PackageFile, 'r') as PackageFile:
            PackageFileInstructions = [Line.strip() for Line in PackageFile.readlines()]
            Instructions = [Instruction for Instruction in PackageFileInstructions if Is_Valid_Instruction(Instruction) == True]
            for Instruction in Instructions: exec(Instruction)


def Is_Valid_Instruction(UserInstruction:str) -> bool:
    for Instruction in InvalidInstructions:
        if Instruction in UserInstruction:
            return False
    return True


def Entry():
    print("Welcome to the thunderdome bitches.")
    Set_Background_Color()
    init_window(Resolution["Width"], Resolution["Height"], WindowSettings["Title"])
    set_target_fps(WindowSettings["FPS"])
    Load_All_Packages()

    while not window_should_close():
        begin_drawing()
        if is_key_down(KEY_R):
            Load_All_Packages()
        clear_background(Background["Color"])
        end_drawing()

    close_window()


if __name__ == '__main__':
    Entry()