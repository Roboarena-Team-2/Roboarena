import pygame
import math
import config
from robot import Robot

# Bar colors for different UI elements
POWER_BAR_COLOR: tuple[int, int, int] = (0, 170, 210)
LIFE_BAR_COLORS: dict[str, tuple[int, int, int]] = {
    "green": (0, 180, 0),
    "yellow": (200, 160, 0),
    "red": (210, 0, 0),
}
BAR_BACKGROUND_DIM = 120


class RobotRenderer:
    def __init__(self, camera_surface):
        self.camera_surface = camera_surface
        # -- Animation system explanation --

        # self.animations stores animation frames for each robot type
        # ( "Spider", "Tank",..)

        # This allows different robot types to load their own frame sets

        # self.frame_indices stores the current animation frame index
        # for each robot instance

        # Multiple robots of the same type may be animated independently
        # -> each needs their own index

        # self.timers stores a timer for each robot instance
        # This controls when to advance the animation frame (based on frame_duration)

        # We use dictionaries (robot -> value) so that:
        # -> each robot has its own independent animation state (frame + timer)

        self.animations: dict[str, list[pygame.Surface]] = {}
        self.frame_indices: dict[object, int] = {}
        self.timers: dict[object, float] = {}
        self.frame_duration = 0.3  # seconds per frame

        # Load animation frames for each robot type
        self.load_robot_type("Spider")
        self.load_robot_type("Tank")

    def load_robot_type(self, robot_type: str):
        if robot_type == "Tank":
            # Load body spritesheet
            body_path = "../resources/Tank/body_spritesheet.png"
            body_sheet = pygame.image.load(body_path).convert_alpha()
            frame_width = body_sheet.get_width()
            frame_height = body_sheet.get_height() // 36
            body_frames = []
            for row in range(36):
                rect = pygame.Rect(0, row * frame_height, frame_width, frame_height)
                frame = body_sheet.subsurface(rect)
                body_frames.append(frame)
            self.animations["Tank_body"] = body_frames

            # Load head spritesheet
            head_path = "../resources/Tank/head_spritesheet.png"
            head_sheet = pygame.image.load(head_path).convert_alpha()
            head_width = head_sheet.get_width()
            head_height = head_sheet.get_height() // 36
            head_frames = []
            for row in range(36):
                rect = pygame.Rect(0, row * head_height, head_width, head_height)
                frame = head_sheet.subsurface(rect)
                head_frames.append(frame)
            self.animations["Tank_head"] = head_frames

            # fallback
            self.animations["Tank"] = body_frames

        else:  # Spider
            spritesheet_path = (
                f"../resources/{robot_type}/{robot_type.lower()}_spritesheet.png"
            )
            spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
            frame_width = spritesheet.get_width() // 4
            frame_height = spritesheet.get_height() // 36
            frames = []
            for row in range(36):  # direction
                for col in range(4):  # animation frame
                    x = col * frame_width
                    y = row * frame_height
                    rect = pygame.Rect(x, y, frame_width, frame_height)
                    frame = spritesheet.subsurface(rect)
                    frames.append(frame)
            self.animations[robot_type] = frames

    def update_animation(self, robot, dt):
        # Update animation based on time + movement
        if robot not in self.frame_indices:
            self.frame_indices[robot] = 0
            self.timers[robot] = 0.0

        if robot.moving:
            self.timers[robot] += dt
            if self.timers[robot] >= self.frame_duration:
                self.timers[robot] = 0.0
                if robot.robot_type == "Spider":
                    self.frame_indices[robot] = (self.frame_indices[robot] + 1) % 4
                else:
                    self.frame_indices[robot] = (self.frame_indices[robot] + 1) % len(
                        self.animations[robot.robot_type]
                    )
        else:
            # Spider resets to frame 0 when not moving
            if robot.robot_type == "Spider":
                self.frame_indices[robot] = 0
            # Tank keeps last frame

    def draw_soft_shadow(self, robot, camera):
        # draw circle shadow below robot
        radius = robot.hitbox_radius * camera.zoom * 0.32
        shadow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surface, (0, 0, 0, 60), (radius, radius), radius)

        # compute shadow offset
        if robot.robot_type == "Tank":
            shadow_pos = camera.apply(robot.x, robot.y + robot.hitbox_radius * 0.15)
        else:
            shadow_pos = camera.apply(robot.x, robot.y + robot.hitbox_radius * 0.1)
        rect = shadow_surface.get_rect(center=shadow_pos)

        self.camera_surface.blit(shadow_surface, rect)

    def draw_text_with_outline(
        self, font, text, x, y, color=(255, 255, 255), outline_color=(0, 0, 0)
    ):
        offsets = [  # outline in 8 directions
            (-1, -1),
            (0, -1),
            (1, -1),
            (-1, 0),
            (1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
        ]

        # draw black outline first
        for offset_x, offset_y in offsets:
            outline = font.render(text, True, outline_color)
            self.camera_surface.blit(outline, (x + offset_x, y + offset_y))
        # Draw main text
        main_text = font.render(text, True, color)
        self.camera_surface.blit(main_text, (x, y))

    def draw_circle_alpha(self, color, center, radius):
        target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.circle(shape_surf, color, (radius, radius), radius)
        self.camera_surface.blit(shape_surf, target_rect)

    def draw(self, robot: Robot, camera, dt):
        """Renders the robot sprite (or default shape), eyes,
        life count and power bar using the camera system"""

        self.update_animation(robot, dt)
        self.draw_soft_shadow(robot, camera)

        if robot.robot_type in self.animations:
            # Get current animation frame based on class type
            if robot.robot_type == "Spider":
                direction_index = int(-robot.alpha / 10) % 36
                animation_index = self.frame_indices[robot] % 4
                index = direction_index * 4 + animation_index

            elif robot.robot_type == "Tank":
                direction_index = (int(-robot.alpha / 10) - int(45)) % 36
                index = direction_index

                # Target angle for Head
                if robot.is_player:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    world_x = mouse_x / camera.zoom + camera.offset_x
                    world_y = mouse_y / camera.zoom + camera.offset_y
                    dx = world_x - robot.x
                    dy = world_y - robot.y
                elif hasattr(robot, "target") and robot.target:
                    dx = robot.target.x - robot.x
                    dy = robot.target.y - robot.y
                else:
                    dx = math.cos(math.radians(robot.alpha))
                    dy = math.sin(math.radians(robot.alpha))

                desired_angle = math.degrees(math.atan2(dy, dx)) % 360
                angle_diff = (desired_angle - robot.alpha + 540) % 360 - 180

                # Head initialisation
                if not hasattr(robot, "head_angle"):
                    robot.head_angle = robot.alpha

                # Head angle restriction
                target_head_angle = (robot.alpha + max(-30, min(30, angle_diff))) % 360

                # Interpolate to the head angle
                delta = (target_head_angle - robot.head_angle + 540) % 360 - 180
                max_step = 10
                robot.head_angle = (
                    robot.head_angle + max(-max_step, min(max_step, delta))
                ) % 360
                head_angle = robot.head_angle

                # Head-Index for animation
                direction_index_Head = (int(-head_angle / 10) + 45) % 36

            scale_factor = 2.0
            scaled_size = int(robot.hitbox_radius * camera.zoom * scale_factor)

            if robot.robot_type == "Tank":
                # draw body
                body_frame = self.animations["Tank_body"][index]
                body_scaled = pygame.transform.smoothscale(
                    body_frame, (scaled_size, scaled_size)
                )
                body_rect = body_scaled.get_rect(center=camera.apply(robot.x, robot.y))
                self.camera_surface.blit(body_scaled, body_rect)

                # draw head
                head_frame = self.animations["Tank_head"][direction_index_Head]
                head_scale = 0.8
                head_size = int(scaled_size * head_scale)
                head_scaled = pygame.transform.smoothscale(
                    head_frame, (head_size, head_size)
                )

                # base angle
                head_rad = math.radians(head_angle)

                # Position starts at robot.x, robot.y
                x = robot.x
                y = robot.y

                # Offset in look direction
                look_shift = 0.2 * robot.hitbox_radius
                x += look_shift * math.cos(head_rad)
                y += look_shift * math.sin(head_rad)

                # Offset back in body direction
                body_rad = math.radians(robot.alpha)
                back_shift = 0.15 * robot.hitbox_radius
                x -= back_shift * math.cos(body_rad)
                y -= back_shift * math.sin(body_rad)

                # orthogonal offset
                ortho_rad = body_rad - math.pi / 2
                side_shift = 0
                x += side_shift * math.cos(ortho_rad)
                y += side_shift * math.sin(ortho_rad)

                # Screen position & draw
                screen_x, screen_y = camera.apply(x, y)
                head_rect = head_scaled.get_rect(center=(screen_x, screen_y))
                self.camera_surface.blit(head_scaled, head_rect)

                # draw laser from head (only for player)
                if robot.is_player:
                    laser_len = config.TILE_SIZE * 6
                    laser_offset = 0.2 * robot.hitbox_radius
                    laser_angle = head_rad - math.radians(5)

                    sx = x + math.cos(laser_angle) * laser_offset
                    sy = y + math.sin(laser_angle) * laser_offset
                    ex = x + math.cos(laser_angle) * (laser_len + laser_offset)
                    ey = y + math.sin(laser_angle) * (laser_len + laser_offset)

                    start = camera.apply(sx, sy)
                    end = camera.apply(ex, ey)
                    laser_surf = pygame.Surface(
                        self.camera_surface.get_size(), pygame.SRCALPHA
                    )
                    pygame.draw.line(laser_surf, (180, 0, 0, 50), start, end, 4)
                    self.camera_surface.blit(laser_surf, (0, 0))

            else:
                frame = self.animations[robot.robot_type][index]
                scaled_image = pygame.transform.smoothscale(
                    frame, (scaled_size, scaled_size)
                )
                rect = scaled_image.get_rect(center=camera.apply(robot.x, robot.y))
                self.camera_surface.blit(scaled_image, rect)

        else:
            # Default body
            pygame.draw.circle(
                self.camera_surface,
                (255, 255, 255),
                camera.apply(robot.x, robot.y),
                robot.hitbox_radius,
            )

            # Eyes
            eye_radius = robot.hitbox_radius * 0.1
            eye_offset_deg = 30
            eye_offset_rad = math.radians(eye_offset_deg)
            alpha_rad = math.radians(robot.alpha)
            eye_distance = robot.hitbox_radius * 0.6
            left_eye = (
                robot.x + eye_distance * math.cos(alpha_rad - eye_offset_rad),
                robot.y + eye_distance * math.sin(alpha_rad - eye_offset_rad),
            )
            right_eye = (
                robot.x + eye_distance * math.cos(alpha_rad + eye_offset_rad),
                robot.y + eye_distance * math.sin(alpha_rad + eye_offset_rad),
            )
            pygame.draw.circle(
                self.camera_surface, (0, 0, 0), camera.apply(*left_eye), eye_radius
            )
            pygame.draw.circle(
                self.camera_surface, (0, 0, 0), camera.apply(*right_eye), eye_radius
            )

        if robot.powerup == "indestructible":
            self.draw_circle_alpha(
                (75, 166, 232, 120),
                camera.apply(robot.x, robot.y),
                robot.hitbox_radius * 0.8,
            )

        if robot.powerup == "ram":
            self.draw_circle_alpha(
                (245, 55, 55, 120),
                camera.apply(robot.x, robot.y),
                robot.hitbox_radius * 0.8,
            )

        # Power bar
        power_height = robot.hitbox_radius * 0.15
        power_width = robot.hitbox_radius
        power_x, power_y = camera.apply(
            robot.x - 38 / camera.zoom,
            robot.y + (robot.hitbox_radius * 0.5 * (-camera.zoom)) + 130,
        )
        fill_width = power_width * (robot.power / 100)

        # background color (with minimum dim)
        power_ratio = robot.power / 100
        raw_dim = int((1 - power_ratio) * BAR_BACKGROUND_DIM / 2)
        dim = max(raw_dim, 50)
        r, g, b = POWER_BAR_COLOR
        bg_color_power = (max(r - dim, 0), max(g - dim, 0), max(b - dim, 0))
        bg_power_rect = pygame.Rect(power_x, power_y, power_width, power_height)

        # Draw background bar
        if not robot.in_bush:
            pygame.draw.rect(self.camera_surface, bg_color_power, bg_power_rect)

        # Draw outline for background bar
        bg_outline_color = (
            min(bg_color_power[0] + 30, 255),
            min(bg_color_power[1] + 30, 255),
            min(bg_color_power[2] + 30, 255),
        )
        if not robot.in_bush:
            pygame.draw.rect(
                self.camera_surface,
                bg_outline_color,
                bg_power_rect,
                robot.hitbox_radius // 25,
            )

        # Draw fill bar
        if not robot.in_bush:
            pygame.draw.rect(
                self.camera_surface,
                POWER_BAR_COLOR,
                pygame.Rect(power_x, power_y, fill_width, power_height),
            )

        # Draw outline for fill bar
        r, g, b = POWER_BAR_COLOR
        highlight_color = (min(r + 40, 255), min(g + 40, 255), min(b + 40, 255))
        if not robot.in_bush:
            pygame.draw.rect(
                self.camera_surface,
                highlight_color,
                pygame.Rect(power_x, power_y, fill_width, power_height),
                robot.hitbox_radius // 25,
            )

        # Draw power value text
        font = pygame.font.SysFont("Arial", int(power_height * 1.5), bold=True)
        text = str(int(robot.power))
        power_number = font.render(text, True, (255, 255, 255))
        p_nrect = power_number.get_rect()
        power_text_x = power_x + (power_width - p_nrect.width) // 2
        power_text_y = power_y + (power_height - p_nrect.height) // 2

        if config.SHOW_STATS:
            if not robot.in_bush:
                self.draw_text_with_outline(font, text, power_text_x, power_text_y)

        # Draw power icon (lightning)
        icon_power = pygame.transform.scale(
            config.ICONS["power"], (int(power_height + 4), int(power_height + 4))
        ).convert_alpha()
        icon_x = power_x - icon_power.get_width() - 5
        icon_y = power_y
        if not robot.in_bush:
            self.camera_surface.blit(icon_power, (icon_x, icon_y))

        # --- Life bar (above power bar) ---
        max_life_height = power_height  # same height as power bar
        max_life_widht = power_width  # same width as power bar
        fill_life_width = max_life_widht * (robot.hp / 100)
        life_x = power_x
        bar_spacing = robot.hitbox_radius * 0.2  # vertical offset
        life_y = power_y - bar_spacing

        # Choose fill color based on HP
        if robot.hp >= 50:
            bar_color = LIFE_BAR_COLORS["green"]
        elif robot.hp >= 20:
            bar_color = LIFE_BAR_COLORS["yellow"]
        else:
            bar_color = LIFE_BAR_COLORS["red"]

        # Background color (darker based on hp)
        hp_ratio = robot.hp / 100
        raw_dim_factor = int((1 - hp_ratio) * BAR_BACKGROUND_DIM * 1)
        dim_factor = max(raw_dim_factor, 90)
        r, g, b = bar_color
        bg_color_rgb = (
            max(r - dim_factor, 0),
            max(g - dim_factor, 0),
            max(b - dim_factor, 0),
        )
        bg_rect = pygame.Rect(life_x, life_y, max_life_widht, max_life_height)

        # Draw background
        if not robot.in_bush:
            pygame.draw.rect(self.camera_surface, bg_color_rgb, bg_rect)

        # Draw outline for background bar
        bg_outline_color = (
            min(bg_color_rgb[0] + 30, 255),
            min(bg_color_rgb[1] + 50, 255),
            min(bg_color_rgb[2] + 30, 255),
        )
        if not robot.in_bush:
            pygame.draw.rect(
                self.camera_surface,
                bg_outline_color,
                bg_rect,
                robot.hitbox_radius // 20,
            )

        # Draw fill bar
        if not robot.in_bush:
            pygame.draw.rect(
                self.camera_surface,
                bar_color,
                pygame.Rect(life_x, life_y, fill_life_width, max_life_height),
            )

        # Draw outline for fill bar
        r, g, b = bar_color
        highlight_color = (min(r + 30, 255), min(g + 30, 255), min(b + 40, 255))

        if not robot.in_bush:
            pygame.draw.rect(
                self.camera_surface,
                highlight_color,
                pygame.Rect(life_x, life_y, fill_life_width, max_life_height),
                robot.hitbox_radius // 25,
            )

        # Draw text (HP number)
        life_text = str(int(robot.hp))
        l_nrect = font.render(
            life_text, True, (0, 0, 0)
        ).get_rect()  # use same font as power bar
        text_x = life_x + (max_life_widht - l_nrect.width) // 2
        text_y = life_y + (max_life_height - l_nrect.height) // 2

        # Only show HP text if SHOW_STATS is active
        if config.SHOW_STATS:
            if not robot.in_bush:
                self.draw_text_with_outline(font, life_text, text_x, text_y)

        # Draw life icon (heart)
        icon_size = max_life_height
        icon_heart = pygame.transform.scale(
            config.ICONS["heart"], (int(icon_size + 3), int(icon_size + 3))
        ).convert_alpha()
        icon_x = life_x - icon_heart.get_width() - 5
        icon_y = life_y
        if not robot.in_bush:
            self.camera_surface.blit(icon_heart, (icon_x, icon_y))

        # Draw Explosion for shooting
        fire_height = robot.hitbox_radius * 0.13
        fire_width = robot.hitbox_radius * 0.15

        # compute head and body direction
        head_angle = robot.head_angle if hasattr(robot, "head_angle") else robot.alpha
        head_rad = math.radians(head_angle - 5)  # shift by -5 degrees
        body_rad = math.radians(robot.alpha)

        # adjust fire position
        look_shift = 0.52 * robot.hitbox_radius
        back_shift = 0.15 * robot.hitbox_radius

        fire_x = (
            robot.x
            + look_shift * math.cos(head_rad)
            - back_shift * math.cos(body_rad)
            - ((fire_width / 2) / camera.zoom)
        )
        fire_y = (
            robot.y
            + look_shift * math.sin(head_rad)
            - back_shift * math.sin(body_rad)
            - ((fire_height / 2) / camera.zoom)
        )
        fire_x, fire_y = camera.apply(fire_x, fire_y)

        icon_size = fire_height
        icon_fire = pygame.transform.scale(
            config.ICONS["explosion"], (int(icon_size + 3), int(icon_size + 3))
        ).convert_alpha()
        icon_fire = pygame.transform.rotate(icon_fire, -robot.alpha - 90)

        current_time = pygame.time.get_ticks()
        if current_time - robot.last_shot_time < 30:
            self.camera_surface.blit(icon_fire, (fire_x, fire_y))

        # Draw Player-Nametag above player
        if robot.is_player:
            # Calculate screen position slightly above the robot
            x_offset = -23 / camera.zoom  # scale with zoom
            y_offset = -robot.hitbox_radius * 0.6
            name_x, name_y = camera.apply(robot.x + x_offset, robot.y + y_offset)

            font = pygame.font.SysFont("Roboto", 18, bold=True)

            # Draw name with outline
            self.draw_text_with_outline(font, "PLAYER", name_x, name_y)
