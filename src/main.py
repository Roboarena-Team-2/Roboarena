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

# Player variables
type: str = "Tank"
language: str = "English"
volume: int = 100
texts = config.texts


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
                difficulty()
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


def difficulty():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)

    easy_button = Button(
        rect=(screen.get_width() // 2 - 425, 300, 250, 50),
        text=texts["easy_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    medium_button = Button(
        rect=(screen.get_width() // 2 - 125, 300, 250, 50),
        text=texts["medium_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    hard_button = Button(
        rect=(screen.get_width() // 2 + 175, 300, 250, 50),
        text=texts["hard_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

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

        draw_text(screen, texts["difficulty_text"], 0, 150, 80, center=True)

        draw_text(screen, texts["normal_mode_text"], 0, 250, 50, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if easy_button.is_clicked(event):
                pass
            if medium_button.is_clicked(event):
                pass
            if hard_button.is_clicked(event):
                pass
            if back_button.is_clicked(event):
                return

        easy_button.draw(screen)
        medium_button.draw(screen)
        hard_button.draw(screen)
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
    )

    spider_button = Button(
        rect=(screen.get_width() // 2 + 50, 300, 250, 50),
        text=texts["spider_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    back_button = Button(
        rect=(screen.get_width() // 2 - 125, 570, 250, 50),
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
            if spider_button.is_clicked(event):
                type = "Spider"
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

    start_button = Button(
        rect=(screen.get_width() // 2 - 125, 400, 250, 50),
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
    )

    level2_button = Button(
        rect=(screen.get_width() // 2 + 25, 300, 250, 50),
        text=texts["map2_text"],
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    back_button = Button(
        rect=(screen.get_width() // 2 - 125, 570, 250, 50),
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
                game_loop()
            if level1_button.is_clicked(event):
                game_loop("test-level.txt")
            if level2_button.is_clicked(event):
                game_loop("test-level2.txt")
            if back_button.is_clicked(event):
                return

        start_button.draw(screen)
        level1_button.draw(screen)
        level2_button.draw(screen)
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
            screen.get_width() * 0.2, 200, screen.get_width() * 0.8, 300
        ),
        slider_color=(200, 50, 50),
        hover_color=(255, 80, 80),
    )

    back_button = Button(
        rect=(screen.get_width() // 2 - 125, 550, 250, 50),
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
        
        for j, icon in enumerate([icon_fire,icon_health,icon_power,icon_shield]):
            if (instructions_top + (17 + 2*j) * 35 - scrollheight >= instructions_top) and (
                (17 + 2*j) * 35 + instructions_top - scrollheight < instructions_bottom
            ):
                screen.blit(icon, (220, instructions_top + (17+2*j) * 35 - scrollheight))

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
        map_file = "test-level.txt"

    # Map setup
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
    spawn_positions = game_map.generate_spawn_positions()
    robot_size = int(config.TILE_SIZE * 1.3)
    player = Robot(
        camera.surface,
        *spawn_positions[0],
        robot_size,
        0,
        (255, 255, 255),
        4 * camera.zoom,
        6 * camera.zoom,
        True,
        type,
    )
    enemy1 = Robot(
        camera.surface,
        *spawn_positions[1],
        robot_size,
        0,
        (0, 100, 190),
        4 * camera.zoom,
        6 * camera.zoom,
        False,
        "Spider",
    )
    enemy2 = Robot(
        camera.surface,
        *spawn_positions[2],
        robot_size,
        50,
        (255, 50, 120),
        4 * camera.zoom,
        6 * camera.zoom,
        False,
        "Spider",
    )
    enemy3 = Robot(
        camera.surface,
        *spawn_positions[3],
        robot_size,
        50,
        (0, 250, 0),
        4 * camera.zoom,
        6 * camera.zoom,
        False,
        "Tank",
    )
    robots: list[Robot] = [player, enemy1, enemy2, enemy3]

    # Bullet and movement setup
    bullets: list[Bullet] = []
    powerups: list[Powerup] = []
    powerup_types: list[str] = [
        "ram",
        "power_boost",
        "health_boost",
        "indestructible",
    ]
    powerup_tick: int = 8000
    enemy_behaviour_tick: int = 0
    start_tick = pygame.time.get_ticks()

    # show countdown before game starts
    countdown(screen, camera, map_renderer, robot_renderer, robots, player)

    running = True

    # run game
    while running:
        dt = clock.tick(60) / 300  # animation speed
        camera.follow_dynamic_center(robots, player)

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
                    gameover(camera, map_renderer, robot_renderer, robots, player)
            else:  # enemies
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
                    robots.remove(robot)
                    if len(robots) <= 1:
                        # render everything one last time, so that you can see,
                        # that all enemies are gone
                        camera.follow_dynamic_center(robots, player)
                        camera.surface.fill((0, 0, 0))
                        map_renderer.draw_map(camera)

                        for robot in robots:
                            robot_renderer.draw(robot, camera, 0)

                        screen.blit(camera.surface, (0, 0))
                        pygame.display.flip()
                        victory(camera, map_renderer, robot_renderer, robots, player)

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
            powerup_tick += 8000  # 8 sec
            random_powerup_type = random.choice(powerup_types)
            powerups.append(Powerup(random_powerup_type, game_map))

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


def gameover(camera, map_renderer, robot_renderer, robots, player):
    sounds = Sounds(volume / 100)
    sounds.stop_all_sounds()
    sounds.play_sound("gameover_sound")

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                elif event.key == pygame.K_RETURN:
                    game_loop()

        pygame.display.flip()
        clock.tick(60)


def victory(camera, map_renderer, robot_renderer, robots, player):

    sounds = Sounds(volume / 100)
    sounds.stop_all_sounds()
    sounds.play_sound("win_sound")

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
                    game_loop()

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
