import sys
dont_write_bytecode = True

import pygame
import pygame.freetype

pygame.init()

Resolution = (800, 800)

Screen = pygame.display.set_mode(Resolution)

Alive = True

Font = pygame.font.SysFont(None, 24)


class UserCursor:
    def __init__(Self) -> None:
        # To make the cursor, we are literally just drawing a line
        Self.X: int = 0
        Self.Y: int = 0
        Self.Width: int = Font.size("A")[0]
        Self.Height: int = Font.size("A")[1]
        Self.Index: int = 0

    def Draw(Self) -> None:
        Self.Body = pygame.draw.rect(Screen, "purple", (Self.X, Self.Y, Self.Width, Self.Height))

    def Return_Rect(Self) -> pygame.Rect:
        return (Self.X, Self.Y, Self.Width, Self.Height)

    def UpdateWidth(Self, Character) -> None:
        Self.Width = Font.size(Character)[0]
        

class Text:
    def __init__(Self) -> None:
        Self.Contents = ""
        Self.X: int = 10
        Self.Y: int = 10
        Self.Width: int = 800
        Self.Height: int = 800

    def Render(Self) -> None:
        Self.OutputText: pygame.Surface = Font.render(Self.Contents, (10, 10), "green", None)
        Screen.blit(Self.OutputText, (0, 0))

Cursor = UserCursor()
TextEditor = Text()

while Alive:
    Screen.fill("black")
    UserInput = None


    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            Alive = False
        if Event.type == pygame.KEYDOWN:
            if Event.unicode == "":
                if Event.key == pygame.K_LEFT:
                    if (Cursor.Index - 1) >= 0:
                        Cursor.Index -= 1
                        Cursor.X = Font.size(TextEditor.Contents[:Cursor.Index])[0]
                        Cursor.UpdateWidth(TextEditor.Contents[Cursor.Index])
                if Event.key == pygame.K_RIGHT:
                    if (Cursor.Index + 1) < len(TextEditor.Contents):
                        Cursor.Index += 1
                        Cursor.X = Font.size(TextEditor.Contents[:Cursor.Index])[0]
                        Cursor.UpdateWidth(TextEditor.Contents[Cursor.Index])
            elif Event.unicode == "\x08":
                TextEditor.Contents = TextEditor.Contents.rstrip(TextEditor.Contents[-1])
                Cursor.X = Font.size(TextEditor.Contents)[0]
                Cursor.Index -= 1
            else:
                UserInput = Event.unicode
                TextEditor.Contents = TextEditor.Contents[:Cursor.Index] + UserInput + TextEditor.Contents[Cursor.Index:]
                Cursor.X = Font.size(TextEditor.Contents[:Cursor.Index])[0]
                if Cursor.X >= 800:
                    Cursor.Y += Font.size("A")[1]
                Cursor.Index += 1

    Cursor.Draw()
    TextEditor.Render()

    pygame.display.flip()

