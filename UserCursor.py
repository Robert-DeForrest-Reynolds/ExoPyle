class UserCursor:
    def __init__(Self) -> None:
        # To make the cursor, we are literally just drawing a line
        Self.X = 0
        Self.Y = 0
        Self.Width = Font.size("A")[0]
        Self.Height = Font.size("A")[1]
        Self.Index = 0

    def Draw(Self) -> None:
        Self.Body = pygame.draw.rect(Screen, "purple", (Self.X, Self.Y, Self.Width, Self.Height))

    def Return_Rect(Self) -> pygame.Rect:
        return (Self.X, Self.Y, Self.Width, Self.Height)

    def UpdateWidth(Self, Character):
        Self.Width = Font.size(Character)[0]