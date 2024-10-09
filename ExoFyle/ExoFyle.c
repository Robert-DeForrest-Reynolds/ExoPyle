#include <stdio.h>
#include <stdlib.h>
#include <raylib.h>
#include "Constants.h"
#include "Structures.h"

Resolution ActiveResolution = {800, 600};
Background ActiveBackground = {34, 34, 34, 255, 0, 0, 0, 0, WHITE};
ApplicationConfig Config = {1, "Normal", NULL, ""};
Editor ExoFyle = {0, {"Test"}, 1, 16, "", 10, 10, 780, 580};

void Output(const char *Message) {
    printf("%s\n", Message);
}

void HandleKeyPress() {
    if (IsKeyPressed(KEY_Q)) {
        exit(0);
    }
}

void SetBackgroundColor() {
    if (ActiveBackground.Red == 0 && ActiveBackground.Blue == 0 && ActiveBackground.Green == 0 && ActiveBackground.Alpha == 0) {
        ActiveBackground.Color = (Color){ActiveBackground.DefaultRed, ActiveBackground.DefaultBlue, ActiveBackground.DefaultGreen, ActiveBackground.DefaultAlpha};
    } else {
        ActiveBackground.Color = (Color){ActiveBackground.Red, ActiveBackground.Blue, ActiveBackground.Green, ActiveBackground.Alpha};
    }
}

void BuildFrame() {
    BeginDrawing();
    SetBackgroundColor();
    ClearBackground(ActiveBackground.Color);
    // BuildEditor();
    EndDrawing();
}

void Initialize() {
    SetTraceLogLevel(LOG_ERROR);
    SetBackgroundColor();
    SetConfigFlags(FLAG_BORDERLESS_WINDOWED_MODE | FLAG_WINDOW_UNDECORATED);
    InitWindow(ActiveResolution.Width, ActiveResolution.Height, "ExoFyle");
    SetTargetFPS(60);
}

void Entry() {
    Initialize();
    while (Config.Alive) {
        BuildFrame();
        HandleKeyPress();
    }
    CloseWindow();
}

int main(void){
    Output("Welcome to the thunderdome.");
    Entry();
    return 0;
}