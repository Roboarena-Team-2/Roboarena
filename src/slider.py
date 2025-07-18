import pygame


class Slider:
    def __init__(
        self, rect, current_percentage, slider_color, circle_color, hover_color=None
    ):
        """
        rect: pygame.Rect oder Tupel (x, y, width, height)
        current_x: aktueller Zustand in Prozent (int)
        slider_color: Hintergrundfarbe (Tuple)
        circle_color: Textfarbe (Tuple)
        hover_color: Hintergrundfarbe bei Hover (optional)
        """
        self.rect = pygame.Rect(rect)
        self.percentage = current_percentage
        self.slider_color = slider_color
        self.circle_color = circle_color
        self.hover_color = hover_color if hover_color else circle_color
        self.x = self.rect.left + self.percentage * self.rect.width / 100
        self.circle_radius = self.rect.height
        self.circle_rect = pygame.Rect(
            self.x - self.circle_radius,
            self.rect.centery - self.circle_radius,
            self.circle_radius * 2,
            self.circle_radius * 2,
        )

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.slider_color,
            self.rect,
            border_radius=int(min(self.rect.height, self.rect.width) / 2),
        )
        mouse_pos = pygame.mouse.get_pos()
        if self.circle_rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.circle_color
        pygame.draw.circle(
            screen, color, (self.x, self.rect.centery), self.circle_radius
        )

    def update(self, percentage):
        new_percentage = self.percentage + percentage
        if new_percentage < 0:
            self.percentage = 0
        elif new_percentage > 100:
            self.percentage = 100
        else:
            self.percentage += percentage
        self.x = self.rect.left + self.percentage * self.rect.width / 100
        self.circle_radius = self.rect.height
        self.circle_rect = pygame.Rect(
            self.x - self.circle_radius,
            self.rect.centery - self.circle_radius,
            self.circle_radius * 2,
            self.circle_radius * 2,
        )
