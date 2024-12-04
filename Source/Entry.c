#include "Include/raylib.h"

// Test editor
// Command palette? Shift-Alt maybe?
// New File, Open File, Save File,
// Syntax highlighting

const int ScreenWidth = 600;
const int ScreenHeight = 600;

void Draw_Text_Frame(){
    int HeightPadding = 10;
    int WidthPadding = 10;
    int X = WidthPadding;
    int Y = HeightPadding;
    int Width = ScreenWidth - WidthPadding * 2;
    int Height = ScreenHeight - HeightPadding * 2;
    DrawRectangleLines(X, Y, Width, Height, BLACK);
}

int main(){

    InitWindow(ScreenWidth, ScreenHeight, "ExoFyle");

    SetTargetFPS(60);

    while(!WindowShouldClose()){
        BeginDrawing();
        ClearBackground(RAYWHITE);
        Draw_Text_Frame();
        EndDrawing();
    }

    CloseWindow();

    return 0;
}