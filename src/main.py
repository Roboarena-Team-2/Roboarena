import pygame
import sys

# Initialisierung
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)

# Konstanten
WIDTH, HEIGHT = 800, 600
FPS = 30
STRAHL_SPEED = 4
FARBE_HINTERGRUND = (0, 0, 0)
FARBE_WAND = (200, 0, 0)
FARBE_STRAHL = (0, 255, 255)
FARBE_SPUR = (100, 200, 200)
FARBE_SPUR_WIN = (0, 255, 0)
FARBE_SPUR_GAMEOVER = (180, 180, 180)

# Spiel-Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hack Minigame")
font = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()

# Spielzustand (Anfangswerte)
game_state = "start"
direction = [0, -1]
trail = []
leben = 3
start_pos = (746, HEIGHT - 44)

# Spielfigur + Ziel
strahl = pygame.Rect(*start_pos, 10, 10)
ziel_chip = pygame.Rect(730, 107, 50, 40)

# Wände
walls = [
    pygame.Rect(0, 70, 800, 20), pygame.Rect(0, 510, 700, 20), pygame.Rect(0, 70, 20, 460),
    pygame.Rect(600, 598, 200, 10), pygame.Rect(795, 200, 20, 460), pygame.Rect(780, 70, 20, 460),
    pygame.Rect(500, 150, 160, 200), pygame.Rect(300, 102, 3, 13), pygame.Rect(300, 124, 3, 15),
    pygame.Rect(540, 88, 3, 15), pygame.Rect(540, 137, 3, 15), pygame.Rect(259, 116, 400, 7),
    pygame.Rect(50, 150, 600, 70), pygame.Rect(50, 150, 20, 120), pygame.Rect(70, 200, 150, 20),
    pygame.Rect(380, 250, 100, 160), pygame.Rect(85, 250, 100, 160), pygame.Rect(0, 300, 100, 160),
    pygame.Rect(0, 500, 700, 100), pygame.Rect(200, 220, 160, 100), pygame.Rect(220, 300, 120, 20),
    pygame.Rect(320, 200, 20, 120), pygame.Rect(340, 200, 180, 20), pygame.Rect(500, 220, 20, 140),
    pygame.Rect(520, 340, 140, 20), pygame.Rect(620, 240, 20, 100), pygame.Rect(640, 240, 115, 20),
    pygame.Rect(766, 240, 20, 200), pygame.Rect(85, 237, 100, 100),
    pygame.Rect(100, 350, 300, 60), pygame.Rect(100, 400, 580, 20), pygame.Rect(100, 400, 20, 70),
    pygame.Rect(300, 420, 20, 90), pygame.Rect(0, 400, 700, 120), pygame.Rect(680, 420, 20, 90)
]


# Hilfsfunktionen
def zeichne_text(text_str, farbe, y_offset=0, shadow=True):
    text = font.render(text_str, True, farbe)
    if shadow:
        shadow_txt = font.render(text_str, True, (0, 0, 0))
        screen.blit(shadow_txt, (WIDTH // 2 - text.get_width() // 2 + 2, HEIGHT // 2 + 2 + y_offset))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + y_offset))


def zeichne_spur(farbe):
    for segment in trail:
        pygame.draw.rect(screen, farbe, segment)


def zeichne_welt():
    screen.fill(FARBE_HINTERGRUND)
    for wall in walls:
        pygame.draw.rect(screen, FARBE_WAND, wall)
    pygame.draw.rect(screen, (255, 255, 255), ziel_chip)
    pygame.draw.rect(screen, (180, 180, 180), (ziel_chip.x, ziel_chip.y, 44, 40))
    pygame.draw.rect(screen, (180, 180, 180), (730, 560, 40, 35))
    pygame.draw.rect(screen, (255, 255, 255), (730, 596, 40, 10))


def reset_strahl():
    global strahl, direction
    strahl.x, strahl.y = start_pos
    direction = [0, -1]


# Spiel-Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_state == "start":
                    game_state = "playing"
                elif game_state == "gameover":
                    leben = 3
                    trail.clear()
                    reset_strahl()
                    game_state = "playing"
            elif event.key == pygame.K_ESCAPE:
                running = False
            elif game_state == "playing":
                if event.key == pygame.K_UP:
                    direction = [0, -1]
                elif event.key == pygame.K_DOWN:
                    direction = [0, 1]
                elif event.key == pygame.K_LEFT:
                    direction = [-1, 0]
                elif event.key == pygame.K_RIGHT:
                    direction = [1, 0]

    zeichne_welt()

    if game_state == "start":
        zeichne_text("Drücke ENTER zum Starten", (0, 255, 0))

    elif game_state == "playing":
        strahl.x += direction[0] * STRAHL_SPEED
        strahl.y += direction[1] * STRAHL_SPEED

        trail.append(pygame.Rect(strahl.x + 2, strahl.y + 2, 6, 6))
        zeichne_spur(FARBE_SPUR)
        pygame.draw.rect(screen, FARBE_STRAHL, strahl)

        for wall in walls:
            if strahl.colliderect(wall):
                leben -= 1
                if leben <= 0:
                    game_state = "gameover"
                else:
                    trail.clear()
                    reset_strahl()
                break

        if strahl.colliderect(ziel_chip):
            game_state = "win"

        screen.blit(font.render(f"Leben: {leben}", True, (255, 255, 255)), (20, 20))

    elif game_state == "gameover":
        zeichne_spur(FARBE_SPUR_GAMEOVER)
        zeichne_text("Game Over!", (255, 0, 0))
        zeichne_text("Drücke ENTER für Neustart", (255, 255, 255), 60)

    elif game_state == "win":
        zeichne_spur(FARBE_SPUR_WIN)
        zeichne_text("Erfolg! Ziel erreicht!", (255, 255, 255))

    pygame.display.flip()
    clock.tick(FPS)

# Aufräumen
pygame.quit()
sys.exit()
