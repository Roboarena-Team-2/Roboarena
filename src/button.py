import pygame


class Button:
    def __init__(
        self,
        rect,
        text,
        font,
        bg_color,
        text_color,
        hover_color=None,
        selected=False,
        selected_color=None,
        tooltip_text=None,  # <-- NEU
        tooltip_font=None,  # <-- NEU
        tooltip_bg=(50, 50, 50),  # Standard-Hintergrund
        tooltip_text_color=(255, 255, 255),
    ):
        """
        rect: pygame.Rect oder Tupel (x, y, width, height)
        text: Button-Beschriftung
        font: pygame.font.Font-Objekt
        bg_color: Hintergrundfarbe (Tuple)
        text_color: Textfarbe (Tuple)
        hover_color: Hintergrundfarbe bei Hover (optional)
        """
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color if hover_color else bg_color
        self.selected = selected
        self.selected_color = selected_color if selected_color else bg_color

        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

        self.tooltip_text = tooltip_text
        self.tooltip_font = tooltip_font if tooltip_font else font
        self.tooltip_bg = tooltip_bg
        self.tooltip_text_color = tooltip_text_color

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.selected:
            color = self.selected_color
        elif self.rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.bg_color

        pygame.draw.rect(screen, color, self.rect)
        screen.blit(self.text_surface, self.text_rect)

        if self.tooltip_text and self.rect.collidepoint(mouse_pos):
            self.draw_tooltip(screen)

    def draw_tooltip(self, screen):
        lines = self.tooltip_text.split("\n")
        padding = 6
        line_surfaces = [
            self.tooltip_font.render(line, True, self.tooltip_text_color)
            for line in lines
        ]
        line_heights = [surf.get_height() for surf in line_surfaces]
        max_width = max(surf.get_width() for surf in line_surfaces)

        # Tooltip-Größe berechnen
        total_height = (
            sum(line_heights) + padding * 2 + (len(lines) - 1) * 2
        )  # zusätzlicher Zeilenabstand

        tooltip_rect = pygame.Rect(0, 0, max_width + padding * 2, total_height)
        tooltip_rect.midbottom = self.rect.midtop
        tooltip_rect.y -= 10  # Abstand über dem Button

        # Hintergrund zeichnen
        pygame.draw.rect(screen, self.tooltip_bg, tooltip_rect, border_radius=4)

        # Zeilen zeichnen
        y = tooltip_rect.y + padding
        for surf in line_surfaces:
            x = tooltip_rect.x + (tooltip_rect.width - surf.get_width()) // 2
            screen.blit(surf, (x, y))
            y += surf.get_height() + 2  # Zeilenabstand

    def is_clicked(self, event):
        """
        Prüft, ob der Button per Maus geklickt wurde.
        event: pygame.event.Event-Objekt
        Rückgabe: True, wenn geklickt, sonst False
        """
        if (
            event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
        ):  # Linke Maustaste
            if self.rect.collidepoint(event.pos):
                return True
        return False
