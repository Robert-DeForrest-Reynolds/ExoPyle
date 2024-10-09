#ifndef STRUCTURES_H
#define STRUCTURES_H
#include "Constants.h"
#include <Raylib.h>


// Configuration structures
typedef struct Resolution {
    int Width;
    int Height;
} Resolution;

typedef struct Background{
    int DefaultRed, DefaultBlue, DefaultGreen, DefaultAlpha;
    int Red, Blue, Green, Alpha;
    Color Color;
} Background;

typedef struct ApplicationConfig{
    int Alive;
    char StateAsString[MAX_LINE_LENGTH];
    void (*CurrentState)();
    char Buffer[MAX_LINE_LENGTH];
} ApplicationConfig;

typedef struct Editor{
    int Exposed;
    char Content[MAX_LINES][MAX_LINE_LENGTH];
    int CurrentLine;
    int FontSize;
    char CurrentFileName[MAX_LINE_LENGTH];
    float X, Y, Width, Height;
} Editor;

#endif