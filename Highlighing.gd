extends TextEdit

var TypeColor = Color("4396bc")
var KeywordColor = Color("b54a4d")
var FunctionColor = Color("#3cc373")
var ValueColor = Color("#3cc373")
var ObjectColor = Color("#d89827")
var SymbolColor = Color("#dfe9e8")
var ImportColor = Color("#663399")
var StringColor = Color("#b9c03f")
var CommentColor = Color("#ace1af")
var OperatorColor = Color("#e15875")

# Called when the node enters the scene tree for the first time.
func _ready():
	print("Test")
	syntax_highlighter = CodeHighlighter.new()
	syntax_highlighter.function_color = FunctionColor
	syntax_highlighter.symbol_color = OperatorColor
	syntax_highlighter.number_color = ValueColor
	syntax_highlighter.add_keyword_color("Int", TypeColor)
	syntax_highlighter.add_keyword_color("Float", TypeColor)
	syntax_highlighter.add_keyword_color("String", TypeColor)
	syntax_highlighter.add_keyword_color("Bln", TypeColor)
	syntax_highlighter.add_keyword_color("Dict", TypeColor)
	syntax_highlighter.add_keyword_color("List", TypeColor)
	syntax_highlighter.add_keyword_color("File", TypeColor)

	syntax_highlighter.add_keyword_color("Obj", ObjectColor)
	syntax_highlighter.member_variable_color = ObjectColor
	syntax_highlighter.add_keyword_color("True", ObjectColor)
	syntax_highlighter.add_keyword_color("False", ObjectColor)

	syntax_highlighter.add_keyword_color("Import", ImportColor)

	syntax_highlighter.add_keyword_color("Fnc", KeywordColor)
	syntax_highlighter.add_keyword_color("For", KeywordColor)
	syntax_highlighter.add_keyword_color("In", KeywordColor)
	syntax_highlighter.add_keyword_color("If", KeywordColor)
	syntax_highlighter.add_keyword_color("Or", KeywordColor)
	syntax_highlighter.add_keyword_color("Else", KeywordColor)
	syntax_highlighter.add_keyword_color("Rtn", KeywordColor)
	syntax_highlighter.add_keyword_color("While", KeywordColor)
	syntax_highlighter.add_keyword_color("Break", KeywordColor)

	syntax_highlighter.add_color_region("\"", "\"", StringColor)

	syntax_highlighter.add_color_region("/", "/", CommentColor)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
