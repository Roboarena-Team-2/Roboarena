import pygame
import sys
import config
from map import Map
from map_renderer import MapRenderer
from robot import Robot
from bullet import Bullet
from button import Button
from slider import Slider
from scrollbar import Scrollbar
from sounds import Sounds
from camera import Camera
from robot_renderer import RobotRenderer
from power_up import Powerup
import random

# Initialisation
pygame.init()

# Get current screen resolution
info = pygame.display.Info()
max_width: int = info.current_w
max_height: int = info.current_h

# Calculate TILE_SIZE based on screen resolution and zoom
base_tile_size = min(max_width // config.COLUMNS, max_height // config.ROWS)

# Apply zoom
config.TILE_SIZE = int(base_tile_size * 2)

# Create window (not fullscreen)
window_width: int = base_tile_size * config.COLUMNS
window_height: int = base_tile_size * config.ROWS

screen: pygame.Surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Roboarena")
clock = pygame.time.Clock()


# Debug info
print(f"Monitor: {max_width}x{max_height}")
print(f"Fenster: {window_width}x{window_height}")
print(f"TILE_SIZE: {config.TILE_SIZE}")

# Player and game variables
type: str = random.choice(["Tank", "Spider"])
language: str = "English"
config.update_language("English")
volume: int = 100
texts = config.texts
difficulty: str = "medium"
highscore: int = 0
highestkills: int = 0
robot_size = int(config.TILE_SIZE * 1.1)
# Map data
current_map = "test-level.txt"
random_map = False
seed = 1


def draw_text(
    surface, text, x, y, font_size, color=(255, 255, 255), font_name=None, center=False
):
    font = pygame.font.SysFont(font_name, font_size)
    text_surface = font.render(text, False, color)
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, y))
    if center:
        surface.blit(text_surface, text_rect)
    else:
        surface.blit(text_surface, (x, y))


def difficulty_easy(camera, game_map) -> list[Robot]:
    game_map.player_count = 3
    spawn_positions = game_map.generate_spawn_positions()

    speed = 3 * camera.zoom
    turnspeed = 4 * camera.zoom
    robots: list[Robot] = []
    for i in range(game_map.player_count):
        if i == 0:
            robots.append(
                Robot(
                    camera.surface,
                    spawn_positions[i][0],
                    spawn_positions[i][1],
                    robot_size,
                    float(random.randint(0, 359)),
                    4 * camera.zoom,
                    5 * camera.zoom,
                    True,
                    type,
                )
            )
        else:
            robots.append(
                Robot(
                    camera.surface,
                    spawn_positions[i][0],
                    spawn_positions[i][1],
                    robot_size,
                    float(random.randint(0, 359)),
                    speed,
                    turnspeed,
                    False,
                    random.choice(("Spider", "Tank")),
                )
            )
    for robot in robots:
        robot.shot_break_duration = 2000
        robot.recharge_rate = 0.05
    return robots


def difficulty_medium(camera, game_map) -> list[Robot]:
    game_map.player_count = 4
    spawn_positions = game_map.generate_spawn_positions()
    speed = 4 * camera.zoom
    turnspeed = 5 * camera.zoom
    robots: list[Robot] = []
    for i in range(game_map.player_count):
        if i == 0:
            robots.append(
                Robot(
                    camera.surface,
                    spawn_positions[i][0],
                    spawn_positions[i][1],
                    robot_size,
                    float(random.randint(0, 359)),
                    4.5 * camera.zoom,
                    5.5 * camera.zoom,
                    True,
                    type,
                )
            )
        else:
            robots.append(
                Robot(
                    camera.surface,
                    spawn_positions[i][0],
                    spawn_positions[i][1],
                    robot_size,
                    float(random.randint(0, 359)),
                    speed,
                    turnspeed,
                    False,
                    random.choice(("Spider", "Tank")),
                )
            )
    for robot in robots:
        robot.shot_break_duration = 1500
        robot.recharge_rate = 0.1
    return robots


def difficulty_hard(camera, game_map) -> list[Robot]:
    game_map.player_count = 5
    spawn_positions = game_map.generate_spawn_positions()
    speed = 5 * camera.zoom
    turnspeed = 6 * camera.zoom
    robots: list[Robot] = []
    for i in range(game_map.player_count):
        if i == 0:
            robots.append(
                Robot(
                    camera.surface,
                    spawn_positions[i][0],
                    spawn_positions[i][1],
                    robot_size,
                    float(random.randint(0, 359)),
                    speed,
                    turnspeed,
                    True,
                    type,
                )
            )
        else:
            robots.append(
                Robot(
                    camera.surface,
                    spawn_positions[i][0],
                    spawn_positions[i][1],
                    robot_size,
                    float(random.randint(0, 359)),
                    speed,
                    turnspeed,
                    False,
                    random.choice(("Spider", "Tank")),
                )
            )
    for robot in robots:
        robot.shot_break_duration = 1000
        robot.recharge_rate = 0.2
    return robots


def difficulty_survival_faster(camera, game_map) -> list[Robot]:
    game_map.player_count = 3
    spawn_positions = game_map.generate_spawn_positions()
    speed = 1 * camera.zoom
    turnspeed = 1 * camera.zoom
    robots: list[Robot] = []
    for i in range(game_map.player_count):
        if i == 0:
            robots.append(
                Robot(
                    camera.surface,
                    spawn_positions[i][0],
                    spawn_positions[i][1],
                    robot_size,
                    float(random.randint(0, 359)),
                    4 * camera.zoom,
                    5 * camera.zoom,
                    True,
                    type,
                )
            )
        else:
            robots.append(
                Robot(
                    camera.surface,
                    spawn_positions[i][0],
                    spawn_positions[i][1],
                    robot_size,
                    float(random.randint(0, 359)),
                    speed,
                    turnspeed,
                    False,
                    random.choice(("Spider", "Tank")),
                )
            )
    for robot in robots:
        robot.shot_break_duration = 1000
        robot.recharge_rate = 0.2
    return robots


def difficulty_survival_more(camera, game_map) -> list[Robot]:
    game_map.player_count = 2
    spawn_positions = game_map.generate_spawn_positions()
    speed = 2 * camera.zoom
    turnspeed = 2 * camera.zoom
    robots: list[Robot] = []
    for i in range(game_map.player_count):
        if i == 0:
            robots.append(
                Robot(
                    camera.surface,
                    spawn_positions[i][0],
                    spawn_positions[i][1],
                    robot_size,
                    float(random.randint(0, 359)),
                    4 * camera.zoom,
                    5 * camera.zoom,
                    True,
                    type,
                )
            )
        else:
            robots.append(
                Robot(
                    camera.surface,
                    spawn_positions[i][0],
                    spawn_positions[i][1],
                    robot_size,
                    float(random.randint(0, 359)),
                    speed,
                    turnspeed,
                    False,
                    random.choice(("Spider", "Tank")),
                )
            )
    for robot in robots:
        robot.shot_break_duration = 1000
        robot.recharge_rate = 0.2
    return robots


def main_menu():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)

    start_button = Button(
        rect=(screen.get_width() // 2 - 125, 250, 250, 50),
        text=texts["start_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    difficulty_button = Button(
        rect=(screen.get_width() // 2 - 125, 320, 250, 50),
        text=texts["difficulty_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    instructions_button = Button(
        rect=(screen.get_width() // 2 - 125, 390, 250, 50),
        text=texts["instructions_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    level_button = Button(
        rect=(screen.get_width() // 2 - 125, 460, 250, 50),
        text=texts["level_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    settings_button = Button(
        rect=(screen.get_width() // 2 - 125, 530, 250, 50),
        text=texts["settings_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    quit_button = Button(
        rect=(screen.get_width() // 2 - 125, 600, 250, 50),
        text=texts["quit_text"],
        font=font,
        bg_color=(200, 50, 50),
        text_color=(255, 255, 255),
        hover_color=(255, 80, 80),
    )

    running = True
    while running:
        screen.fill((30, 30, 30))

        title_font = pygame.font.SysFont(None, 80)
        title_surf = title_font.render(texts["main_menu_text"], True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(title_surf, title_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if start_button.is_clicked(event):
                class_selection()
            if difficulty_button.is_clicked(event):
                difficulty_selection()
            if instructions_button.is_clicked(event):
                instructions_menu()
            if level_button.is_clicked(event):
                level_selection()
            if settings_button.is_clicked(event):
                settings()
                main_menu()
                return
            if quit_button.is_clicked(event):
                pygame.quit()
                sys.exit()

        start_button.draw(screen)
        difficulty_button.draw(screen)
        instructions_button.draw(screen)
        level_button.draw(screen)
        settings_button.draw(screen)
        quit_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def pause_menu():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)

    continue_button = Button(
        rect=(screen.get_width() // 2 - 125, 230, 250, 50),
        text=texts["continue_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    menu_button = Button(
        rect=(screen.get_width() // 2 - 125, 300, 250, 50),
        text=texts["main_menu_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    settings_button = Button(
        rect=(screen.get_width() // 2 - 125, 370, 250, 50),
        text=texts["settings_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    instructions_button = Button(
        rect=(screen.get_width() // 2 - 125, 440, 250, 50),
        text=texts["instructions_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    quit_button = Button(
        rect=(screen.get_width() // 2 - 125, 510, 250, 50),
        text=texts["quit_text"],
        font=font,
        bg_color=(200, 50, 50),
        text_color=(255, 255, 255),
        hover_color=(255, 80, 80),
    )

    paused = True
    while paused:

        sounds = Sounds(volume / 100)
        sounds.stop_all_sounds()
        screen.fill((30, 30, 30))

        title_font = pygame.font.SysFont(None, 80)  # große Schrift
        title_surf = title_font.render(texts["paused_text"], True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(title_surf, title_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if continue_button.is_clicked(event):
                paused = False
            if menu_button.is_clicked(event):
                main_menu()
            if settings_button.is_clicked(event):
                settings()
                pause_menu()
                return
            if instructions_button.is_clicked(event):
                instructions_menu()
            if quit_button.is_clicked(event):
                pygame.quit()
                sys.exit()

        continue_button.draw(screen)
        menu_button.draw(screen)
        settings_button.draw(screen)
        instructions_button.draw(screen)
        quit_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def difficulty_selection():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)

    global difficulty

    easy_button = Button(
        rect=(screen.get_width() // 2 - 425, 300, 250, 50),
        text=texts["easy_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
        selected=difficulty == "easy",
        selected_color=(0, 100, 150),
    )

    medium_button = Button(
        rect=(screen.get_width() // 2 - 125, 300, 250, 50),
        text=texts["medium_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
        selected=difficulty == "medium",
        selected_color=(0, 100, 150),
    )

    hard_button = Button(
        rect=(screen.get_width() // 2 + 175, 300, 250, 50),
        text=texts["hard_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
        selected=difficulty == "hard",
        selected_color=(0, 100, 150),
    )

    survival1_button = Button(
        rect=(screen.get_width() // 2 - 225, 450, 200, 50),
        text="Survival1",
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
        selected=difficulty == "survival1",
        selected_color=(0, 100, 150),
    )

    survival2_button = Button(
        rect=(screen.get_width() // 2 + 25, 450, 200, 50),
        text="Survival2",
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
        selected=difficulty == "survival2",
        selected_color=(0, 100, 150),
    )

    back_button = Button(
        rect=(screen.get_width() // 2 - 125, 600, 250, 50),
        text=texts["back_text"],
        font=font,
        bg_color=(200, 50, 50),
        text_color=(255, 255, 255),
        hover_color=(255, 80, 80),
    )

    running = True
    while running:
        screen.fill((30, 30, 30))

        draw_text(screen, texts["difficulty_text"], 0, 150, 80, center=True)

        draw_text(screen, texts["normal_mode_text"], 0, 250, 50, center=True)

        draw_text(screen, texts["survival_mode_text"], 0, 400, 50, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if easy_button.is_clicked(event):
                difficulty = "easy"
                return options()  # noqa: F821
            if medium_button.is_clicked(event):
                difficulty = "medium"
                return options()  # noqa: F821
            if hard_button.is_clicked(event):
                difficulty = "hard"
                return options()  # noqa: F821
            if survival1_button.is_clicked(event):
                difficulty = "survival1"
                return options()  # noqa: F821
            if survival2_button.is_clicked(event):
                difficulty = "survival2"
                return options()  # noqa: F821
            if back_button.is_clicked(event):
                return

        easy_button.draw(screen)
        medium_button.draw(screen)
        hard_button.draw(screen)
        survival1_button.draw(screen)
        survival2_button.draw(screen)
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def class_selection():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)
    global type

    start_button = Button(
        rect=(screen.get_width() // 2 - 125, 400, 250, 50),
        text=texts["start_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    tank_button = Button(
        rect=(screen.get_width() // 2 - 300, 300, 250, 50),
        text=texts["tank_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
        selected=type == "Tank",
        selected_color=(0, 100, 150),
    )

    spider_button = Button(
        rect=(screen.get_width() // 2 + 50, 300, 250, 50),
        text=texts["spider_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
        selected=type == "Spider",
        selected_color=(0, 100, 150),
    )

    back_button = Button(
        rect=(screen.get_width() // 2 - 125, 600, 250, 50),
        text=texts["back_text"],
        font=font,
        bg_color=(200, 50, 50),
        text_color=(255, 255, 255),
        hover_color=(255, 80, 80),
    )

    running = True
    while running:
        screen.fill((30, 30, 30))

        draw_text(screen, texts["class_selection_text"], 0, 150, 80, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if start_button.is_clicked(event):
                game_loop()
            if tank_button.is_clicked(event):
                type = "Tank"
                return class_selection()
            if spider_button.is_clicked(event):
                type = "Spider"
                return class_selection()
            if back_button.is_clicked(event):
                return

        start_button.draw(screen)
        spider_button.draw(screen)
        tank_button.draw(screen)
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def level_selection():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)
    global random_map
    global current_map
    global seed

    start_button = Button(
        rect=(screen.get_width() // 2 - 125, 450, 250, 50),
        text=texts["start_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    level1_button = Button(
        rect=(screen.get_width() // 2 - 275, 300, 250, 50),
        text=texts["map1_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
        selected=current_map == "test-level.txt" and not random_map,
        selected_color=(0, 100, 150),
    )

    level2_button = Button(
        rect=(screen.get_width() // 2 + 25, 300, 250, 50),
        text=texts["map2_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
        selected=current_map == "test-level2.txt" and not random_map,
        selected_color=(0, 100, 150),
    )

    level3_button = Button(
        rect=(screen.get_width() // 2 - 250, 370, 200, 50),
        text=texts["lava_river"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
        selected=current_map == "lavariver.txt" and not random_map,
        selected_color=(0, 100, 150),
    )

    level4_button = Button(
        rect=(screen.get_width() // 2 + 50, 370, 200, 50),
        text=texts["four_elements"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
        selected=current_map == "fourelements.txt" and not random_map,
        selected_color=(0, 100, 150),
    )

    random_button = Button(
        rect=(screen.get_width() // 2 - 100, 520, 200, 50),
        text=texts["Random"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
        selected=random_map,
        selected_color=(0, 100, 150),
    )

    back_button = Button(
        rect=(screen.get_width() // 2 - 125, 600, 250, 50),
        text=texts["back_text"],
        font=font,
        bg_color=(200, 50, 50),
        text_color=(255, 255, 255),
        hover_color=(255, 80, 80),
    )

    running = True
    while running:
        screen.fill((30, 30, 30))

        draw_text(screen, texts["level_selection_text"], 0, 150, 80, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if start_button.is_clicked(event):
                game_loop(current_map)
            if level1_button.is_clicked(event):
                current_map = "test-level.txt"
                random_map = False
                return level_selection()
            if level2_button.is_clicked(event):
                current_map = "test-level2.txt"
                random_map = False
                return level_selection()
            if level3_button.is_clicked(event):
                current_map = "lavariver.txt"
                random_map = False
                return level_selection()
            if level4_button.is_clicked(event):
                current_map = "fourelements.txt"
                random_map = False
                return level_selection()
            if random_button.is_clicked(event):
                random_map = True
                seed = random.randint(0, 999999)
                return level_selection()
            if back_button.is_clicked(event):
                return

        start_button.draw(screen)
        level1_button.draw(screen)
        level2_button.draw(screen)
        level3_button.draw(screen)
        level4_button.draw(screen)
        random_button.draw(screen)
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def settings():
    global volume
    global texts
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)

    volume_slider = Slider(
        rect=(screen.get_width() // 2 - 100, 290, 200, 10),
        current_percentage=volume,
        slider_color=(20, 130, 200),
        circle_color=(200, 50, 50),
        hover_color=(255, 80, 80),
    )

    english_button = Button(
        rect=(screen.get_width() // 2 - 275, 390, 250, 50),
        text=texts["english_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    german_button = Button(
        rect=(screen.get_width() // 2 + 25, 390, 250, 50),
        text=texts["german_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    credits_button = Button(
        rect=(screen.get_width() // 2 - 125, 520, 250, 50),
        text=texts["show_credits_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    back_button = Button(
        rect=(screen.get_width() // 2 - 125, 600, 250, 50),
        text=texts["back_text"],
        font=font,
        bg_color=(200, 50, 50),
        text_color=(255, 255, 255),
        hover_color=(255, 80, 80),
    )

    active_slider = None

    running = True
    while running:
        screen.fill((30, 30, 30))

        draw_text(screen, texts["settings_text"], 0, 150, 80, center=True)

        draw_text(screen, texts["volume_text"], 0, 250, 50, center=True)

        draw_text(screen, texts["language_text"], 0, 350, 50, center=True)

        draw_text(screen, texts["credits_text"], 0, 490, 50, center=True)

        global language

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if volume_slider.circle_rect.collidepoint(event.pos):
                        active_slider = volume_slider.circle_rect

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    active_slider = None
                    volume = volume_slider.percentage

            if event.type == pygame.MOUSEMOTION:
                if active_slider:
                    volume_slider.update(
                        event.rel[0] / (volume_slider.rect.width / 100)
                    )

            if english_button.is_clicked(event):
                language = "English"
                texts = config.update_language(language)
                settings()
                return
            if german_button.is_clicked(event):
                language = "German"
                texts = config.update_language(language)
                settings()
                return
            if credits_button.is_clicked(event):
                game_credits()
            if back_button.is_clicked(event):
                return

        volume_slider.draw(screen)
        english_button.draw(screen)
        german_button.draw(screen)
        credits_button.draw(screen)
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def instructions_menu():
    font = pygame.font.SysFont(None, 40)

    instructions_scrollbar = Scrollbar(
        len(texts["instructions"]) * 45 - 600,
        text_space=pygame.Rect(
            screen.get_width() * 0.2, 200, screen.get_width() * 0.8, 350
        ),
        slider_color=(215, 215, 215),
        hover_color=(245, 245, 245),
    )

    back_button = Button(
        rect=(screen.get_width() // 2 - 125, 600, 250, 50),
        text=texts["back_text"],
        font=font,
        bg_color=(200, 50, 50),
        text_color=(255, 255, 255),
        hover_color=(255, 80, 80),
    )

    active_slider = None
    instructions_top = instructions_scrollbar.space_rect.top
    instructions_bottom = instructions_scrollbar.space_rect.bottom

    running = True
    while running:
        screen.fill((30, 30, 30))
        draw_text(screen, texts["instructions_text"], 0, 150, 80, center=True)
        scrollheight = (
            instructions_scrollbar.current_height
            * instructions_scrollbar.text_height
            / instructions_scrollbar.space_rect.height
        )

        for i, line in enumerate(texts["instructions"]):
            if (instructions_top + i * 35 - scrollheight >= instructions_top) and (
                i * 35 + instructions_top - scrollheight < instructions_bottom
            ):
                draw_text(
                    screen, line, 200, instructions_top + i * 35 - scrollheight, 40
                )

        # Powerups
        icon_fire = pygame.transform.scale(
            config.ICONS["explosion"],
            (
                30,
                30,
            ),
        ).convert_alpha()
        icon_health = pygame.transform.scale(
            config.ICONS["heart"],
            (
                30,
                30,
            ),
        ).convert_alpha()
        icon_power = pygame.transform.scale(
            config.ICONS["power"],
            (
                30,
                30,
            ),
        ).convert_alpha()
        icon_shield = pygame.transform.scale(
            config.ICONS["shield"],
            (
                30,
                30,
            ),
        ).convert_alpha()

        for j, icon in enumerate([icon_fire, icon_health, icon_power, icon_shield]):
            if (
                instructions_top + (31 + 2 * j) * 35 - scrollheight >= instructions_top
            ) and (
                (31 + 2 * j) * 35 + instructions_top - scrollheight
                < instructions_bottom
            ):
                screen.blit(
                    icon, (220, instructions_top + (31 + 2 * j) * 35 - scrollheight)
                )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if instructions_scrollbar.slider_rect.collidepoint(event.pos):
                        active_slider = instructions_scrollbar.slider_rect

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    active_slider = None

            if event.type == pygame.MOUSEMOTION:
                if active_slider:
                    instructions_scrollbar.update(event.rel[1])
            if back_button.is_clicked(event):
                return

        back_button.draw(screen)
        instructions_scrollbar.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def countdown(surface, camera, map_renderer, robot_renderer, robots, player):
    font = pygame.font.SysFont(None, 150)
    countdown_numbers = ["3", "2", "1", texts["go_text"]]

    sounds = Sounds(volume / 100)
    sounds.play_sound("countdown_sound")

    # player can see whole arena during countdown
    camera.zoom = 0.5

    for count in countdown_numbers:
        camera.surface.fill((0, 0, 0))
        map_renderer.draw_map(camera)

        for robot in robots:
            robot_renderer.draw(robot, camera, 0)

        text_surface = font.render(count, False, (255, 255, 255))
        text_rect = text_surface.get_rect(
            center=(surface.get_width() // 2, surface.get_height() // 2)
        )
        surface.blit(camera.surface, (0, 0))
        surface.blit(text_surface, text_rect)
        pygame.display.flip()

        # wait one second
        pygame.time.delay(1000)


def game_loop(map_file: str | None = None):
    if map_file is None:
        map_file = current_map

    # Map setup
    if random_map:
        game_map = Map(random_map=True, seed=seed)
    else:
        game_map = Map(map_file)
    map_data = game_map.get_map_data()
    map_width_px = len(map_data[0]) * config.TILE_SIZE
    map_height_px = len(map_data) * config.TILE_SIZE

    # Camera setup
    camera_width = window_width
    camera_height = window_height
    camera = Camera(camera_width, camera_height, map_width_px, map_height_px)

    map_renderer = MapRenderer(camera.surface, config.TEXTURES)
    map_renderer.draw_map_picture(game_map.get_map_data())
    walls: list[pygame.Rect] = game_map.walls()

    # Robot setup
    robot_renderer = RobotRenderer(camera.surface)
    if difficulty == "easy":
        robots = difficulty_easy(camera, game_map)
    if difficulty == "medium":
        robots = difficulty_medium(camera, game_map)
    if difficulty == "hard":
        robots = difficulty_hard(camera, game_map)
    if difficulty == "survival1":
        robots = difficulty_survival_more(camera, game_map)
    if difficulty == "survival2":
        robots = difficulty_survival_faster(camera, game_map)
    player = robots[0]

    # Bullet and movement setup
    bullets: list[Bullet] = []
    powerups: list[Powerup] = []
    powerup_types: list[str] = [
        "ram",
        "power_boost",
        "health_boost",
        "indestructible",
    ]
    powerup_tick: int = 7000
    enemy_behaviour_tick: int = 0
    start_tick = pygame.time.get_ticks()
    increasing_speed_variable: float = 0.8
    enemy_base_speed: float = robots[1].speed
    kills: int = 0
    robot_tick: int = 15000
    robot_tick_increaser: int = 14000

    # show countdown before game starts
    countdown(screen, camera, map_renderer, robot_renderer, robots, player)

    running = True

    # run game
    while running:
        dt = clock.tick(60) / 300  # animation speed
        camera.follow_dynamic_center(robots, player)

        # Rotate Player by 10° steps using a/d
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # clock-wise
            player.rotation_frame = (player.rotation_frame + 10) % 360
        if keys[pygame.K_d]:  # counter-clock-wise
            player.rotation_frame = (player.rotation_frame - 10) % 360

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sounds = Sounds(volume / 100)
                sounds.stop_all_sounds()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu()

        # Drawing background
        camera.surface.fill((0, 0, 0))
        map_renderer.draw_map(camera)

        # Timing logic
        ticks = pygame.time.get_ticks()

        # Enemy behavior update every 3 seconds
        if ticks - start_tick > enemy_behaviour_tick:
            enemy_behaviour_tick += 3000  # 3 sec
            goals: list[Robot | None] = []
            for robot in robots:
                if robot is player:
                    continue
                goals.append(robot.get_robot_with_distance_prob(game_map, robots))
        for robot in robots:
            if robot is player:  # player
                player.update_player(robots, game_map, walls, bullets, camera, powerups)
                if player.hp <= 0:
                    player.hp = 0  # set to 0, so it does not show a negativ number
                    if difficulty == "survival1" or difficulty == "survival2":
                        score: int = int((ticks - start_tick) / 1000)

                    # render everything one last time, so that you can see, that hp is 0
                    camera.follow_dynamic_center(robots, player)
                    camera.surface.fill((0, 0, 0))
                    map_renderer.draw_map(camera)

                    for robot in robots:
                        robot_renderer.draw(robot, camera, 0)

                    screen.blit(camera.surface, (0, 0))
                    pygame.display.flip()

                    # short break, so that you can hear the sound of getting shot or lava
                    pygame.time.delay(900)

                    # call gameover function
                    if difficulty == "survival1" or difficulty == "survival2":
                        gameover(
                            camera,
                            map_renderer,
                            robot_renderer,
                            robots,
                            player,
                            score,
                            kills,
                        )
                    else:
                        gameover(camera, map_renderer, robot_renderer, robots, player)
            else:  # enemies
                if (difficulty == "survival1") or (difficulty == "survival2"):
                    robot.update_enemy(
                        player,
                        robots,
                        game_map,
                        walls,
                        bullets,
                        camera,
                        powerups,
                    )
                    if robot.hp < 100:
                        robot.hp = 0
                else:
                    robot.update_enemy(
                        goals[robots.index(robot) - 1],
                        robots,
                        game_map,
                        walls,
                        bullets,
                        camera,
                        powerups,
                    )
                if robot.hp <= 0:
                    kills += 1
                    robots.remove(robot)
                    if len(robots) <= 1:
                        if (difficulty != "survival1") and (difficulty != "survival2"):
                            # render everything one last time, so that you can see,
                            # that all enemies are gone
                            camera.follow_dynamic_center(robots, player)
                            camera.surface.fill((0, 0, 0))
                            map_renderer.draw_map(camera)

                            for robot in robots:
                                robot_renderer.draw(robot, camera, 0)

                            screen.blit(camera.surface, (0, 0))
                            pygame.display.flip()
                            victory(
                                camera, map_renderer, robot_renderer, robots, player
                            )

            # draw robot
            robot_renderer.draw(robot, camera, dt)

            # draw bush overlay effect (if robot is next to a bush)
            if robot.in_bush:
                for i, j in robot.bush_tiles:
                    texture = config.TEXTURES["bush"]
                    tile_size = int(config.TILE_SIZE * camera.zoom)
                    tile = pygame.transform.scale(texture, (tile_size, tile_size))

                    camera.surface.blit(
                        tile, camera.apply(i * config.TILE_SIZE, j * config.TILE_SIZE)
                    )

        # Bullet updates
        for bullet in bullets:
            bullet.update_bullet(game_map, camera)
            if not bullet.alive:
                bullets.remove(bullet)

        # Powerup appearing
        if ticks - start_tick > powerup_tick:
            powerup_tick += 7000  # 7 sec
            random_powerup_type = random.choice(powerup_types)
            powerups.append(Powerup(random_powerup_type, game_map))

        # Robots appearing for survival mode
        if difficulty == "survival1":  # more
            if ticks - start_tick > robot_tick:  # time for new robot
                robot_tick += robot_tick_increaser
                if robot_tick_increaser > 3500:
                    robot_tick_increaser -= 500
                robots.append(
                    Robot(
                        camera.surface,
                        -1000,
                        -1000,
                        player.hitbox_radius,
                        float(random.randint(0, 359)),
                        2,
                        2,
                        False,
                        random.choice(("Spider", "Tank")),
                    )
                )
                robots[len(robots) - 1].get_spawn_position(game_map, robots)
            if len(robots) < 2:  # currently no alive enemy
                robot_tick = ticks - start_tick + robot_tick_increaser
                if robot_tick_increaser > 3500:
                    robot_tick_increaser -= 500
                robots.append(
                    Robot(
                        camera.surface,
                        -1000,
                        -1000,
                        player.hitbox_radius,
                        float(random.randint(0, 359)),
                        2,
                        2,
                        False,
                        random.choice(("Spider", "Tank")),
                    )
                )
                robots[len(robots) - 1].get_spawn_position(game_map, robots)
        if difficulty == "survival2":  # faster
            if len(robots) < 3 and player.hp > 0:
                robots.append(
                    Robot(
                        camera.surface,
                        -1000,
                        -1000,
                        player.hitbox_radius,
                        float(random.randint(0, 359)),
                        enemy_base_speed + increasing_speed_variable,
                        enemy_base_speed + increasing_speed_variable,
                        False,
                        random.choice(("Spider", "Tank")),
                    )
                )
                robots[len(robots) - 1].get_spawn_position(game_map, robots)
                increasing_speed_variable += 0.8

        # Powerups updates
        for powerup in powerups:
            powerup.draw_powerup(camera)
            powerup.time_left -= 10
            if (not powerup.alive) or (powerup.time_left <= 0):
                powerups.remove(powerup)

        screen.blit(camera.surface, (0, 0))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


def gameover(camera, map_renderer, robot_renderer, robots, player, score=-1, kills=-1):
    sounds = Sounds(volume / 100)
    sounds.stop_all_sounds()
    sounds.play_sound("gameover_sound")

    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time <= 6000:
        if player:
            camera.follow_dynamic_center(robots, player)
        camera.surface.fill((0, 0, 0))
        map_renderer.draw_map(camera)

        for robot in robots:
            robot_renderer.draw(robot, camera, 0)

        draw_text(screen, "GAME OVER", 0, 200, 100, center=True)

        if difficulty == "survival1" or difficulty == "survival2":
            global highscore
            global highestkills
            if highscore < score:  # set new highscore
                highscore = score
            if highestkills < kills:
                highestkills = kills
            draw_text(screen, f"Highscore: {highscore}s", 0, 330, 70, center=True)
            draw_text(screen, f"Score: {score}s", 0, 400, 70, center=True)
            draw_text(screen, f"Highest Kills: {highestkills}", 0, 470, 70, center=True)
            draw_text(screen, f"Kills: {kills}", 0, 540, 70, center=True)

        pygame.display.flip()
        clock.tick(60)

    running = True
    while running:
        if player:
            camera.follow_dynamic_center(robots, player)
        camera.surface.fill((0, 0, 0))
        map_renderer.draw_map(camera)

        for robot in robots:
            robot_renderer.draw(robot, camera, 0)

        draw_text(screen, texts["gameover_text"], 0, 200, 100, center=True)

        for i, line in enumerate(texts["endgame_text"]):
            draw_text(screen, line, 0, 300 + i * 55, 50, center=True)

        if difficulty == "survival1" or difficulty == "survival2":
            draw_text(screen, f"Highscore: {highscore}s", 0, 330, 70, center=True)
            draw_text(screen, f"Score: {score}s", 0, 400, 70, center=True)
            draw_text(screen, f"Highest Kills: {highestkills}", 0, 470, 70, center=True)
            draw_text(screen, f"Kills: {kills}", 0, 540, 70, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                elif event.key == pygame.K_RETURN:
                    game_loop(current_map)

        pygame.display.flip()
        clock.tick(60)


def victory(camera, map_renderer, robot_renderer, robots, player):

    sounds = Sounds(volume / 100)
    sounds.stop_all_sounds()
    sounds.play_sound("win_sound")

    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time <= 4000:
        if player:
            camera.follow_dynamic_center(robots, player)
        camera.surface.fill((0, 0, 0))
        map_renderer.draw_map(camera)

        for robot in robots:
            robot_renderer.draw(robot, camera, 0)

        draw_text(screen, "VICTORY", 0, 200, 100, center=True)

        pygame.display.flip()
        clock.tick(60)

    running = True
    while running:
        if player:
            camera.follow_dynamic_center(robots, player)
        camera.surface.fill((0, 0, 0))
        map_renderer.draw_map(camera)

        for robot in robots:
            robot_renderer.draw(robot, camera, 0)

        draw_text(screen, texts["victory_text"], 0, 200, 100, center=True)

        for i, line in enumerate(texts["endgame_text"]):
            draw_text(screen, line, 0, 300 + i * 55, 50, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                elif event.key == pygame.K_RETURN:
                    game_loop(current_map)

        pygame.display.flip()
        clock.tick(60)


def game_credits():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)

    back_button = Button(
        rect=(screen.get_width() // 2 - 125, 510, 250, 50),
        text=texts["back_text"],
        font=font,
        bg_color=(200, 50, 50),
        text_color=(255, 255, 255),
        hover_color=(255, 80, 80),
    )

    running = True
    while running:
        screen.fill((30, 30, 30))

        draw_text(screen, texts["credits_text"], 0, 150, 80, center=True)

        for i, line in enumerate(texts["credits"]):
            draw_text(screen, line, 50, 200 + i * 35, 30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if back_button.is_clicked(event):
                return

        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


main_menu()
