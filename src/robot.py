import pygame
import config
from bullet import Bullet
import math
import random
from map import Map
from sounds import Sounds
from camera import Camera
from power_up import Powerup

# Constants
ice_acceleration: float = 2
sand_acceleration: float = 1 / 2

# Recharge-rate (how much power will be recharged every frame)
recharge_rate: float = 0.1

# Time with powerups
ram_time: int = 300
indestructible_time: int = 300


class Robot:
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        hitbox_radius: int,
        direction: float,
        color: tuple[int, int, int],
        speed: float,
        speed_alpha: float,
        is_player: bool,
        robot_type: str = "",
    ):
        self.screen = screen
        self.x = x  # x-coordiante of center
        self.y = y  # y-coordinate of center
        self.hitbox_radius = hitbox_radius  # radius of the hitbox
        self.alpha = direction % 360  # direction of the robot in degree
        self.color = color  # color of the robot
        if robot_type == "Tank":
            self.v = speed * 0.8
            self.v_alpha = speed_alpha * 0.6
            self.speed = speed * 0.8
            self.speed_alpha = speed_alpha * 0.6
        else:
            self.v = speed  # current acceleration for moving
            self.v_alpha = speed_alpha  # current acceleration for turning
            self.speed = speed  # speed for moving
            self.speed_alpha = speed_alpha  # speed for turning
        self.hp = 100  # current livepoints of the robot
        self.last_shot_time = 100  # time of last shot
        self.shot_break_duration = 1500  # min duration of break between shots
        self.power = 100  # current power for attacks
        self.recharge_rate = recharge_rate
        self.moving = False  # if robot is currently moving
        self.is_player = is_player  # if robot is player (not enemy)
        self.last_wall_hit_time = 0  # time of last wall hit sound
        self.times_without_sand = 0
        # how often there was no sand in touched_textures in a row
        # while the robot was on sand
        self.times_without_bush = 0
        # how often there was no bus in touched_textures in a row
        # while the robot was in a bush
        self.time_left_with_powerup = 0  # variable for powerups with limited time
        self.ram_pause = 0  # variable to avoid instant death with ram collision
        self.powerup = None  # current Powerup
        self.sounds = Sounds()  # loading the sounds

        self.in_bush = False  # Whether the robot is currently standing in a bush tile
        self.bush_tiles = (
            []
        )  # List of bush tile positions robot is currently overlapping
        self.robot_type = robot_type
        self.frames_without_turning = 8

    # Lets the player move the robot on map
    def update_player(
        self,
        robots: list["Robot"],
        game_map: Map,
        walls: list[pygame.Rect],
        bullets: list[Bullet],
        camera: Camera,
        powerups: list[Powerup],
    ) -> None:
        # Check for effect
        self.exist(game_map, robots, bullets, powerups)

        if self.robot_type == "Tank":
            keys = pygame.key.get_pressed()
            # rotate
            self.alpha += (keys[pygame.K_d] - keys[pygame.K_a]) * self.v_alpha
            self.alpha = self.alpha % 360

            # move
            alpha_rad = math.radians(self.alpha)
            x = 0
            y = 0
            if keys[pygame.K_w]:  # forward
                x = math.cos(alpha_rad) * self.v
                y = math.sin(alpha_rad) * self.v
            if keys[pygame.K_s]:  # backwards
                x = -1 * math.cos(alpha_rad) * self.v
                y = -1 * math.sin(alpha_rad) * self.v
            self.move_if_no_walls(x, y, walls, robots, game_map)

            # sound
            currently_moving = (
                keys[pygame.K_d]
                or keys[pygame.K_a]
                or keys[pygame.K_w]
                or keys[pygame.K_s]
            )
            if currently_moving and not self.moving:
                self.sounds.play_sound("drive_sound")
                self.moving = True
            if not currently_moving and self.moving:
                self.sounds.stop_loop("drive_sound")
                self.moving = False

            # shoot
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mouse_world_x, mouse_world_y = camera.screen_to_world(
                        mouse_x, mouse_y
                    )
                    dx = mouse_world_x - self.x
                    dy = mouse_world_y - self.y
                    shooting_angle = math.degrees(math.atan2(dy, dx)) % 360
                    diff = (shooting_angle - self.alpha + 180) % 360 - 180
                    alpha = self.alpha
                    if diff >= 0:
                        alpha += min(45, diff)
                    else:
                        alpha += max(-45, diff)
                    self.shoot(alpha, bullets, camera, walls, robots, game_map)

        else:  # Spider and back-up robot
            # Update player direction based on mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_world_x, mouse_world_y = camera.screen_to_world(mouse_x, mouse_y)
            dx = mouse_world_x - self.x
            dy = mouse_world_y - self.y
            new_direction_rad = math.atan2(dy, dx)
            new_direction_deg = math.degrees(new_direction_rad) % 360
            diff = (new_direction_deg - self.alpha + 180) % 360 - 180
            if abs(diff) > self.v_alpha:  # to avoid jittering
                turning = True
                if diff > 0:
                    self.alpha += self.v_alpha
                else:
                    self.alpha += self.v_alpha * (-1)
            else:
                self.alpha = new_direction_deg
                turning = False
            # check that alpha is always between 0 and 360 degrees
            self.alpha %= 360

            # Update player position based on key inputs
            keys = pygame.key.get_pressed()

            x = (keys[pygame.K_d] - keys[pygame.K_a]) * self.v
            y = (keys[pygame.K_s] - keys[pygame.K_w]) * self.v
            self.move_if_no_walls(x, y, walls, robots, game_map)

            # sound for moving
            currently_moving = (
                keys[pygame.K_d]
                or keys[pygame.K_a]
                or keys[pygame.K_s]
                or keys[pygame.K_w]
                or turning
            )
            if currently_moving and not self.moving:
                if self.robot_type == "Spider":
                    self.sounds.play_sound("spider_sound")
                else:
                    self.sounds.play_sound("drive_sound")
                self.moving = True
            if not currently_moving and self.moving:
                if self.robot_type == "Spider":
                    self.sounds.stop_loop("spider_sound")
                else:
                    self.sounds.stop_loop("drive_sound")
                self.moving = False

            # check, if user used a key for shooting
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.shoot(self.alpha, bullets, camera, walls, robots, game_map)

    # Lets a robot follow another robot
    def update_enemy(
        self,
        goal: "Robot | None",
        robots: list["Robot"],
        game_map: Map,
        walls: list[pygame.Rect],
        bullets: list[Bullet],
        camera: Camera,
        powerups: list[Powerup],
    ) -> None:
        # Check for effect
        self.exist(game_map, robots, bullets, powerups)

        # Check for goal
        if not goal:
            self.go_hide(game_map, walls, robots)
            return None

        # calculate goal direction
        x_to_goal = goal.x - self.x
        y_to_goal = goal.y - self.y

        if self.robot_type == "Tank":
            # Adjust rotation to face the goal
            rad_to_goal = math.atan2(y_to_goal, x_to_goal)
            angle_to_goal = math.degrees(rad_to_goal) % 360
            angle_diff = (angle_to_goal - self.alpha + 180) % 360 - 180
            if self.frames_without_turning == 0:
                if abs(angle_diff) < self.v_alpha:
                    self.alpha = angle_to_goal
                else:
                    self.alpha += math.copysign(self.v_alpha, angle_diff)
                self.alpha = self.alpha % 360
                self.frames_without_turning = 8
            else:
                self.frames_without_turning -= 1

            # Move towards a goal position
            alpha_rad = math.radians(self.alpha)
            forward_x = math.cos(alpha_rad)  # x-part of direction
            forward_y = math.sin(alpha_rad)  # y-part of direction
            dot = x_to_goal * forward_x + y_to_goal * forward_y  # dot product
            if dot == 0:
                direction = 0  # dont move (90 degree angle to goal)
            elif dot > 0:
                direction = 1  # move forward
            else:
                direction = -1  # move backward
            x = forward_x * self.v * direction
            y = forward_y * self.v * direction
            self.move_if_no_walls(x, y, walls, robots, game_map, check_for_lava=True)

            # shoot, if goal is in 45° range
            if abs(angle_diff) < 45:
                self.shoot(angle_to_goal, bullets, camera, walls, robots, game_map)

        else:  # spider and back-up robot
            # Adjust rotation to face the goal
            rad_to_goal = math.atan2(y_to_goal, x_to_goal)
            angle_to_goal = math.degrees(rad_to_goal) % 360
            angle_diff = (angle_to_goal - self.alpha + 180) % 360 - 180
            if abs(angle_diff) < self.v_alpha:
                self.alpha = angle_to_goal
            else:
                self.alpha += math.copysign(self.v_alpha, angle_diff)
            self.alpha = self.alpha % 360

            # Move towards a goal position
            x = math.copysign(self.v, x_to_goal)
            y = math.copysign(self.v, y_to_goal)
            self.move_if_no_walls(x, y, walls, robots, game_map, check_for_lava=True)

            # shoot if angle to goal is under 10°
            if abs(angle_diff) < 10:
                self.shoot(self.alpha, bullets, camera, walls, robots, game_map)

        # avoid being in range of other robots
        self.move_if_in_range(robots, walls, game_map)

        # # check, if robot NPC is moving
        self.moving = (
            abs(goal.x - self.x) > 0.5
            or abs(goal.y - self.y) > 0.5
            or abs(angle_to_goal - self.alpha) > 1
        )

    # React to collisions with other robots
    def robot_collision(
        self, robot: "Robot", robots: list["Robot"], walls: list[pygame.Rect]
    ) -> None:
        rad_to_goal = math.atan2(robot.y - self.y, robot.x - self.x)
        angle_to_goal = (math.degrees(rad_to_goal) + 180) % 360
        angle_away = angle_to_goal
        x = 10 * math.cos(angle_away * math.pi / 180)
        y = 10 * math.sin(angle_away * math.pi / 180)
        xnew = self.x + x
        ynew = self.y + y
        newRect = pygame.Rect(
            xnew - self.hitbox_radius,
            ynew - self.hitbox_radius,
            self.hitbox_radius * 2,
            self.hitbox_radius * 2,
        )
        if self.powerup == "ram" and self.ram_pause == 0:
            robot.hp -= 5
            self.ram_pause = 50
        # moves robot to direct wanted path if no wall
        if newRect.collidelist(walls) == -1:
            self.x = xnew
            self.y = ynew
            (dist, robot) = self.robot_dist(robots)[0]
            if dist <= 0:
                self.x -= x
                self.y -= y

    # Detect distances to other robots
    def robot_dist(self, robots: list["Robot"]) -> list[tuple[float, "Robot"]]:
        dist_robot: list[tuple[float, Robot]] = []
        for robot in robots:
            if robot != self:
                x_to_robot = robot.x - self.x
                y_to_robot = robot.y - self.y
                dist = (
                    math.sqrt((x_to_robot) ** 2 + (y_to_robot) ** 2)
                    - self.hitbox_radius * 0.4
                    - robot.hitbox_radius * 0.4
                )
                dist_robot.append((dist, robot))
        dist_robot = sorted(dist_robot, key=lambda x: x[0])
        return dist_robot

    def get_hitbox(self, x: float | None = None, y: float | None = None) -> pygame.Rect:
        """
        Returns the robot's hitbox
        If no arguments then return the hitbox at the current position
        If x and y are given return the hitbox at the given position
        """
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        return pygame.Rect(
            x - self.hitbox_radius * 0.4,
            y - self.hitbox_radius * 0.35,
            self.hitbox_radius * 0.75,
            self.hitbox_radius * 0.75,
        )

    # Get the list of tiles touched by the robot
    def touched_tiles(self) -> list[tuple[int, int]]:

        x_bounds = [
            self.get_hitbox().left // config.TILE_SIZE,
            (self.get_hitbox().right - 1) // config.TILE_SIZE,
        ]
        y_bounds = [
            self.get_hitbox().top // config.TILE_SIZE,
            (self.get_hitbox().bottom - 1) // config.TILE_SIZE,
        ]
        touching_tiles = []
        for i in range(x_bounds[0], x_bounds[1] + 1):
            for j in range(y_bounds[0], y_bounds[1] + 1):
                touching_tiles.append((i, j))
        return touching_tiles

    # Get the textures of the tiles touched by the robot
    def touched_textures(self, game_map: Map) -> set[str]:
        touched_textures = set()
        for [i, j] in self.touched_tiles():
            touched_textures.add(game_map.get_tile_type(i, j))
        return touched_textures

    # Effect for robot from map
    def map_effects(self, game_map: Map, robots: list["Robot"]) -> None:
        touched_textures = self.touched_textures(game_map)
        # stop sand and bush sounds, when robot is no longer on sand/bush
        if "sand" not in touched_textures or not self.moving:
            self.times_without_sand += 1
            if self.times_without_sand > 50:  # avoid stopping the sound unintentionally
                self.sounds.stop_loop("sand_sound")
                self.times_without_sand = 0
        if "bush" not in touched_textures or not self.moving:
            self.times_without_bush += 1
            if self.times_without_bush > 50:  # avoid stopping the sound unintentionally
                self.sounds.stop_loop("bush_sound")
                self.times_without_bush = 0
        if "ice" in touched_textures:
            self.v = self.speed * ice_acceleration
            self.v_alpha = self.speed_alpha * ice_acceleration
            if self.powerup == "ram":
                self.v *= 2
            if self.is_player and self.moving:
                self.sounds.play_sound("ice_sound")
        elif "sand" in touched_textures:
            self.v = self.speed * sand_acceleration
            self.v_alpha = self.speed_alpha * sand_acceleration
            if self.powerup == "ram":
                self.v *= 2
            if self.is_player and self.moving:
                self.sounds.play_sound("sand_sound")
        elif "wall" in touched_textures:
            pass
        else:
            self.v = self.speed
            self.v_alpha = self.speed_alpha
            if self.powerup == "ram":
                self.v *= 2
        if "lava" in touched_textures:
            self.get_spawn_position(game_map, robots)
            self.hp -= 40
            if self.is_player:
                self.sounds.play_sound("lava_sound")
        if "bush" in touched_textures:
            self.in_bush = True
            self.bush_tiles = []
            for [i, j] in self.touched_tiles():
                if game_map.get_tile_type(i, j) == "bush":
                    self.bush_tiles.append((i, j))
            if self.is_player and self.moving:
                self.sounds.play_sound("bush_sound")

        else:
            self.in_bush = False
            self.bush_tiles = []

    # Get random spawn position
    def get_spawn_position(
        self, game_map: Map, robots: list["Robot"]
    ) -> tuple[int, int]:
        # Get random position
        position_x = random.randint(
            2 * config.TILE_SIZE + self.hitbox_radius,
            (config.COLUMNS - 2) * config.TILE_SIZE,
        )
        position_y = random.randint(
            2 * config.TILE_SIZE + self.hitbox_radius,
            (config.ROWS - 2) * config.TILE_SIZE,
        )
        # Check for distance to other robots
        self.x = position_x
        self.y = position_y
        max_dist = math.hypot(
            config.TILE_SIZE * (config.ROWS - 2),
            config.TILE_SIZE * (config.COLUMNS - 2),
        )
        min_dist = max_dist / (len(robots) + 1)
        if self.robot_dist(robots)[0][0] > min_dist:
            # Check for tiles to avoid walls, lava and bush
            touched_textures = self.touched_textures(game_map)
            if (
                ("lava" not in touched_textures)
                and ("wall" not in touched_textures)
                and ("bush" not in touched_textures)
            ):
                return (position_x, position_y)
        # Try again
        return self.get_spawn_position(game_map, robots)

    # moves robot if new position not in wall
    def move_if_no_walls(
        self,
        x: float,
        y: float,
        walls: list[pygame.Rect],
        robots: list["Robot"],
        game_map: Map,
        check_for_lava: bool = False,
    ) -> None:
        xnew = self.x + x
        ynew = self.y + y
        # moves robot to direct wanted path if no wall
        hitbox = self.get_hitbox(xnew, ynew)
        if hitbox.collidelist(walls) == -1:
            self.x = xnew
            self.y = ynew
            if check_for_lava:
                touched_textures = self.touched_textures(game_map)
                if "lava" in touched_textures:
                    if self.robot_type == "Tank":  # avoid that tank moves diagonally
                        self.x -= x
                        self.y -= y
                    else:
                        self.y -= y
                        touched_textures = self.touched_textures(game_map)
                        if "lava" in touched_textures:
                            self.x -= x
                            self.y += y
                            if "lava" in touched_textures:
                                self.y -= y
                else:
                    (dist, robot) = self.robot_dist(robots)[0]
                    if dist <= 0:
                        self.x -= x
                        self.y -= y
                        self.robot_collision(robot, robots, walls)
                check_for_lava = False
            else:
                (dist, robot) = self.robot_dist(robots)[0]
                if dist <= 0:
                    self.x -= x
                    self.y -= y
                    self.robot_collision(robot, robots, walls)
        # to avoid not moving at all when goal is behind wall
        else:
            current_time = pygame.time.get_ticks()
            # avoid playing the wall_hit sound too often when going along a wall
            if self.is_player and (current_time - self.last_wall_hit_time > 3000):
                self.sounds.play_sound("wall_hit_sound")
                self.last_wall_hit_time = current_time
            if self.robot_type != "Tank":  # tank cant move sideways along a wall
                # check and move if only in x direction is no wall
                xnew = self.x + x
                ynew = self.y
                hitbox = self.get_hitbox(xnew, ynew)
                if hitbox.collidelist(walls) == -1:
                    self.x = xnew
                    self.y = ynew
                    (dist, robot) = self.robot_dist(robots)[0]
                    if dist <= 0:
                        self.x -= x
                        self.robot_collision(robot, robots, walls)
                else:
                    # check and move if only in y direction is no wall
                    xnew = self.x
                    ynew = self.y + y
                    hitbox = self.get_hitbox(xnew, ynew)
                    if hitbox.collidelist(walls) == -1:
                        self.x = xnew
                        self.y = ynew
                        (dist, robot) = self.robot_dist(robots)[0]
                        if dist <= 0:
                            self.y -= y
                            self.robot_collision(robot, robots, walls)

    def shoot(
        self,
        alpha,
        bullets: list[Bullet],
        camera: Camera,
        walls: list[pygame.Rect],
        robots: list["Robot"],
        game_map: Map,
    ) -> None:
        current_time = pygame.time.get_ticks()
        # make sure there is a break between the shots
        if current_time - self.last_shot_time < self.shot_break_duration:
            return None
        # make sure there is enough power
        if self.power <= 20:
            return None
        # shoot, if there is enough time and power

        alpha_rad = math.radians(self.alpha)
        offset = self.hitbox_radius * 0.2  # start the bullet closer to center
        start_x = self.x + offset * math.cos(alpha_rad)  # start outsinde of the robot
        start_y = self.y + offset * math.sin(alpha_rad)
        if self.robot_type == "Tank":
            velocity = 25 * camera.zoom
            reach = 800
        else:  # Spider and back-up robot
            velocity = 20 * camera.zoom
            reach = 600
        bullet = Bullet(
            int(start_x),
            int(start_y),
            alpha,
            int(7 * camera.zoom),
            (0, 0, 0),
            self,
            velocity,
            reach,
        )  # create bullet
        # recoil
        direction_rad = math.radians(self.alpha)
        x = self.v * -math.cos(direction_rad) * 2
        y = self.v * -math.sin(direction_rad) * 2
        self.move_if_no_walls(x, y, walls, robots, game_map)
        self.last_shot_time = current_time  # update time of last shot
        self.power -= 20  # update power
        bullets.append(bullet)
        if self.is_player:
            self.sounds.play_sound("shot_sound")

    # checks and react if robot is shot
    def getting_shot(self, bullets: list[Bullet]) -> None:
        for bullet in bullets:
            if self is bullet.shooter:  # except for robot which shot the bullet
                continue
            dist_x = abs(bullet.x - self.x)
            dist_y = abs(bullet.y - self.y)
            dist = math.sqrt(dist_x**2 + dist_y**2)
            max_dist = bullet.radius + self.hitbox_radius * 0.35
            if dist < max_dist:
                bullet.alive = False
                if self.powerup != "indestructible":
                    if bullet.shooter.robot_type == "Tank":
                        self.hp = self.hp - 30
                    else:
                        self.hp = self.hp - 15  # robot is spider or back-up robot
                    if self.is_player:
                        self.sounds.play_sound("player_hit_sound")

    # helper-function to get list of robots with probability corresponding to its distance
    def dist_to_prob(
        self, dist_robot: list[tuple[float, "Robot"]]
    ) -> list[tuple[float, "Robot"]]:
        prob_robot: list[tuple[float, "Robot"]] = []
        total_dist: float = sum(d for d, r in dist_robot)
        for dist, robot in dist_robot:
            # preventing divison with 0
            if dist == 0:
                prob: float = 10**9
            else:
                prob: float = total_dist / dist

            prob_robot.append((prob, robot))
        return prob_robot

    # helper-function to get list of robots with corresponding distance
    def get_robot_with_distance_prob(
        self, game_map: Map, robots: list["Robot"]
    ) -> "None | Robot":
        potential_goals: list["Robot"] = []
        for robot in robots:
            if (
                not all("bush" == tile for tile in robot.touched_textures(game_map))
            ) and robot is not self:
                potential_goals.append(robot)
        if len(potential_goals) > 0:
            dist_robot: list[tuple[float, "Robot"]] = self.robot_dist(potential_goals)
            prob_robot: list[tuple[float, "Robot"]] = self.dist_to_prob(dist_robot)

            # avoiding: 'ValueError: Total of weights must be greater than zero'
            # by removing robots with zero probability before calling random.choices
            prob_robot = [(p, r) for p, r in prob_robot if p > 0]

            robot: "Robot" = random.choices(
                [r for p, r in prob_robot], weights=[p for p, r in prob_robot], k=1
            )[0]
            return robot
        return None

    # Avoid if in range of other robots
    def move_if_in_range(
        self, robots: list["Robot"], walls: list[pygame.Rect], game_map: Map
    ) -> None:
        for robot in robots:
            if robot == self:
                continue
            rad_to_robot = math.atan2(robot.y - self.y, robot.x - self.x)
            angle_to_robot = (math.degrees(rad_to_robot) + 180) % 360
            angle_diff = abs(abs(angle_to_robot) - robot.alpha) % 360
            in_range = False
            if robot.robot_type == "Tank":
                if (angle_diff <= 45) or (angle_diff >= 315):
                    in_range = True
            else:
                if (angle_diff <= 10) or (angle_diff >= 350):
                    in_range = True
            if in_range:  # in range of robot
                x_to_goal = robot.x - self.x
                y_to_goal = robot.y - self.y
                if self.robot_type == "Tank":
                    rad_alpha = math.radians(self.alpha)
                    forward_vector = (math.cos(rad_alpha), math.sin(rad_alpha))

                    # dot product to determine if robot is in front, back or at the side
                    dot = x_to_goal * forward_vector[0] + y_to_goal * forward_vector[1]
                    if abs(dot) > 0.5:
                        # move away
                        x = -math.copysign(self.v, dot) * forward_vector[0]
                        y = -math.copysign(self.v, dot) * forward_vector[1]
                    else:
                        x, y = 0, 0  # robot is at the side
                else:
                    if abs(y_to_goal) <= 0.5:
                        x = math.copysign(0, y_to_goal)
                    else:
                        x = math.copysign(self.v, y_to_goal)
                    if abs(x_to_goal) <= 0.5:
                        y = math.copysign(self.v, x_to_goal * -1)
                    else:
                        y = math.copysign(0, x_to_goal * -1)
                self.move_if_no_walls(x, y, walls, robots, game_map)  # move to side

    # Robot does nothing (but still experience effects of map and bullets)
    def exist(
        self,
        game_map: Map,
        robots: list["Robot"],
        bullets: list[Bullet],
        powerups: list[Powerup],
    ) -> None:
        # Check for effects and bullets
        self.map_effects(game_map, robots)
        self.getting_shot(bullets)
        self.getting_powerup(powerups)

        # recharge power
        if self.power < 100:
            self.power += self.recharge_rate

        # set time left with powerup
        if self.time_left_with_powerup > 0:
            self.time_left_with_powerup -= 1
            if self.ram_pause != 0:
                self.ram_pause -= 1
            if self.time_left_with_powerup == 0:
                # Set back
                self.powerup = None
                self.v = self.speed
                self.v_alpha = self.speed_alpha

    def go_hide(
        self, game_map: Map, walls: list[pygame.Rect], robots: list["Robot"]
    ) -> None:
        # Already in bush
        if all("bush" == tile for tile in self.touched_textures(game_map)):
            return None
        # Search for nearest Bush
        bush_tiles = []
        for i in range(0, config.COLUMNS):
            for j in range(0, config.ROWS):
                if game_map.get_tile_type(i, j) == "bush":
                    bush_tiles.append((i, j))
        sorted_bush_tiles = []
        for i, j in bush_tiles:
            tile_x = i * config.TILE_SIZE
            tile_y = j * config.TILE_SIZE
            # distance from robot to middle of tile
            dist = math.sqrt((tile_x - self.x) ** 2 + (tile_y - self.y) ** 2)
            sorted_bush_tiles.append((i, j, dist))
        # sort by incresing distance
        sorted_bush_tiles = sorted(sorted_bush_tiles, key=lambda tile: tile[2])
        nearest_bush_middle = None
        for i, j, d in sorted_bush_tiles:
            xn = 1
            yn = 1
            while (2 * self.get_hitbox().width) >= (xn * config.TILE_SIZE):
                if i + xn <= config.COLUMNS and (i + xn, j) in bush_tiles:
                    xn += 1
                else:
                    break
            while (2 * self.get_hitbox().height) >= (yn * config.TILE_SIZE):
                if j + yn <= config.ROWS and all(
                    list(((i + n, j + yn) in bush_tiles) for n in range(xn))
                ):
                    yn += 1
                else:
                    break
            if (
                2 * self.get_hitbox().width < xn * config.TILE_SIZE
                and 2 * self.get_hitbox().height < yn * config.TILE_SIZE
            ):
                # get middle
                x = (i + (xn - 1)) * config.TILE_SIZE
                y = (j + (yn - 1)) * config.TILE_SIZE
                nearest_bush_middle = (x, y)
                break
        if not nearest_bush_middle:
            return None
        # Adjust rotation to face the goal
        rad_to_goal = math.atan2(
            nearest_bush_middle[1] - self.y, nearest_bush_middle[0] - self.x
        )
        angle_to_goal = (math.degrees(rad_to_goal) + 180) % 360

        # Invert direction if shortest rotation is the other way
        if angle_to_goal < self.alpha:
            if abs(angle_to_goal - self.alpha) > 180:
                angle_to_goal *= -1
        else:
            if abs(angle_to_goal - self.alpha) < 180:
                angle_to_goal *= -1
        self.alpha += math.copysign(self.v_alpha, angle_to_goal)
        self.alpha = self.alpha % 360

        # go to bush
        if self.robot_type == "Tank":
            rad_alpha = math.radians(self.alpha)
            forward_vector = (math.cos(rad_alpha), math.sin(rad_alpha))
            dx = nearest_bush_middle[0] - self.x
            dy = nearest_bush_middle[1] - self.y
            dot = (
                dx * forward_vector[0] + dy * forward_vector[1]
            )  # dot product to determine if bush is in front, back or at the side
            if abs(dot) > 0.5:
                # move forwards or backwards (depending on dot)
                x = math.copysign(self.v, dot) * forward_vector[0]
                y = math.copysign(self.v, dot) * forward_vector[1]
            else:
                # dont move (bush is sideways)
                x, y = 0, 0
        else:
            x = math.copysign(self.v, nearest_bush_middle[0] - self.x)
            y = math.copysign(self.v, nearest_bush_middle[1] - self.y)

        self.move_if_no_walls(x, y, walls, robots, game_map, check_for_lava=True)

    # checks and react if robot is touching a powerup
    def getting_powerup(self, powerups: list[Powerup]) -> None:
        robot_box = pygame.Rect(
            int(self.x),
            int(self.y),
            int(self.hitbox_radius * 2),
            int(self.hitbox_radius * 2),
        )
        for powerup in powerups:
            if powerup.rect.colliderect(robot_box):
                powerup.alive = False
                if powerup.type == "ram":
                    self.powerup = "ram"
                    self.time_left_with_powerup = ram_time
                    self.v *= 2
                    self.v_alpha *= 2
                    if self.is_player:
                        self.sounds.play_sound("powerup_sound")
                if powerup.type == "health_boost":
                    self.hp = min(100, self.hp + 50)
                    if self.is_player:
                        self.sounds.play_sound("powerup_sound")
                if powerup.type == "power_boost":
                    self.power = min(100, self.power + 50)
                    if self.is_player:
                        self.sounds.play_sound("powerup_sound")
                if powerup.type == "indestructible":
                    self.powerup = "indestructible"
                    self.time_left_with_powerup = indestructible_time
                    if self.is_player:
                        self.sounds.play_sound("powerup_sound")
