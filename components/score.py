class Score:
    
    def __init__(self, font, color) -> None:
        self.value = 0
        self.font = font
        self.color = color

    def display(self, game_window) -> None:
        surface = self.font.render(str(self.value), True, self.color)
        game_window.blit(
            surface,
            surface.get_rect()
        )

    def update(self) -> None:
        self.value += 10