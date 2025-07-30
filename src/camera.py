import pygame


class Camera:
    def __init__(
        self,
        camera_surface_width: int,
        camera_surface_height: int,
        map_pixel_width: int,
        map_pixel_height: int,
    ):
        self.zoom: float = 1.3  # Current zoom level
        self.camera_surface_width = camera_surface_width
        self.camera_surface_height = camera_surface_height
        self.map_pixel_width = map_pixel_width  # Total map width in pixels
        self.map_pixel_height = map_pixel_height  # Total map height in pixels
        self.offset_x = 0
        self.offset_y = 0
        self.center_x = 0  # Camera center X in world coords
        self.center_y = 0  # Camera center Y in world coords
        self.surface = pygame.Surface(
            (self.camera_surface_width, self.camera_surface_height)
        )

    def follow_dynamic_center(self, robots: list, player):
        """
        Follow the center between all robots (including the player),
        and zoom based on the largest distance between any two robots.
        """
        all_robots = robots + [player]

        # Calculate center position
        sum_x = sum(bot.x for bot in all_robots)
        sum_y = sum(bot.y for bot in all_robots)
        cx = sum_x / len(all_robots)
        cy = sum_y / len(all_robots)

        # follow center
        if self.center_x == 0 and self.center_y == 0:
            self.center_x = cx
            self.center_y = cy
        self.center_x += (cx - self.center_x) * 0.1
        self.center_y += (cy - self.center_y) * 0.1

        # Compute Offset based on center + zoom
        half_width = self.camera_surface_width / (2 * self.zoom)
        half_height = self.camera_surface_height / (2 * self.zoom)
        self.offset_x = int(self.center_x - half_width)
        self.offset_y = int(self.center_y - half_height)

        # Calculate max distance between any two robots
        max_dist = 0
        for i in range(len(all_robots)):
            for j in range(i + 1, len(all_robots)):
                a = all_robots[i]
                b = all_robots[j]
                dx = abs(a.x - b.x)
                dy = abs(a.y - b.y)
                weighted = dx + dy * 2.5  # y weighted more
                max_dist = max(max_dist, weighted)

        # Adjust zoom based on max_dist
        min_dist = 100
        max_dist_cap = 2500
        zoom_near = 1.2
        zoom_far = 0.5

        # Normalized value in range [0, 1]
        t = (max_dist - min_dist) / (max_dist_cap - min_dist)
        t = max(0.0, min(t, 1.0))
        target_zoom = zoom_near * (1 - t) + zoom_far * t
        self.zoom += (target_zoom - self.zoom) * 0.1

        # Clamp camera to map boundaries
        max_x = self.map_pixel_width - self.camera_surface_width / self.zoom
        max_y = self.map_pixel_height - self.camera_surface_height / self.zoom
        self.offset_x = max(0, min(self.offset_x, int(max_x)))
        self.offset_y = max(0, min(self.offset_y, int(max_y)))

    def apply(self, x: int, y: int) -> tuple[int, int]:
        """Converts world coordinates to screen coordinates"""
        screen_x = (x - self.offset_x) * self.zoom
        screen_y = (y - self.offset_y) * self.zoom
        return int(screen_x), int(screen_y)

    def screen_to_world(self, screen_x: int, screen_y: int) -> tuple[float, float]:
        """Converts screen coordinates back to world coordinates"""
        world_x = screen_x / self.zoom + self.offset_x
        world_y = screen_y / self.zoom + self.offset_y
        return world_x, world_y
