import pygame


class Scrollbar:
    def __init__(
        self, text_height, text_space, slider_color, hover_color=None
    ):
        """
        text_height: Texttiefe (int)
        text_space: pygame.Rect (x, y, width, height)
        current_height: aktueller Zustand in Pixels (int)
        slider_color: Hintergrundfarbe (Tuple)
        hover_color: Hintergrundfarbe bei Hover (optional)
        """
        self.slider_rect = pygame.Rect(text_space.right-25, text_space.top, 25 , text_space.height*text_space.height/text_height)
        self.space_rect = text_space
        self.text_height = text_height
        self.current_height = 0
        self.slider_color = slider_color
        self.hover_color = hover_color if hover_color else slider_color

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.slider_color,
            self.slider_rect,
            border_radius=int(min(self.slider_rect.height, self.slider_rect.width) / 2),
        )
        mouse_pos = pygame.mouse.get_pos()
        if self.slider_rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.slider_color
        pygame.draw.rect(screen, color, self.slider_rect)

    def update(self, pixels):
        new_height = self.space_rect.top + self.current_height + self.space_rect.height*pixels/self.text_height
        if new_height < self.space_rect.top:
            self.current_height = 0
        elif new_height > self.space_rect.bottom - self.slider_rect.height:
            self.current_height = self.space_rect.height - self.slider_rect.height
        else:
            self.current_height += pixels
        self.slider_rect = pygame.Rect(self.slider_rect.left, self.space_rect.top + self.current_height, self.slider_rect.width, self.slider_rect.height)
