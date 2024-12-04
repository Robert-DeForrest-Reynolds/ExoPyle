SourceFiles = $(wildcard Source/*.c)\

Include = Source/Include
Library = Source/Library


Build:
	clang $(SourceFiles) -o ExoFyle -I$(Include) -L$(Library) -lraylib -lgdi32 -lwinmm
build: Build

Debug:
	clang $(SourceFiles) -o ExoFyle -I$(Include) -L$(Library) -lraylib -lgdi32 -lwinmm -Wno-deprecated-non-prototype -DDEBUG=1 -Wswitch
debug: Debug

Release:
	clang $(SourceFiles) -o ExoFyle -I$(Include) -L$(Library) -lraylib -lgdi32 -lwinmm
release: Release

Test:
	clang $(SourceFiles) -o ExoFyle -I$(Include) -L$(Library) -lraylib -lgdi32 -lwinmm -DDEBUG=1
	@echo ""
	./ExoFyle
test: Test
	