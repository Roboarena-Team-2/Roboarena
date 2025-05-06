import pygame
import math

class Robot:
    def __init__(self, screen, x, y, radius, direction, color):
        self.screen = screen
        self.x = x # x-coordiante of center
        self.y = y # y-coordinate of center
        self.r = radius # radius of circle
        self.alpha = direction # direction of the robot
        self.color = color # color of the robot

    def draw_robot(self):
        # draw robot (circle)
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

        # calculate values for eyes
        eye_radius = self.r * 0.1 # radius of the eyes
        eye_offset_deg = 30  # deviation of angle of the eyes from direction
        eye_offset_rad = math.radians(eye_offset_deg) # convert to radian
        eye_distance = self.r * 0.6 # distance from center of the robot

        alpha_rad = math.radians(self.alpha)

        left_eye_x = self.x + eye_distance * math.cos(alpha_rad - eye_offset_rad)
        left_eye_y = self.y + eye_distance * math.sin(alpha_rad - eye_offset_rad)
        right_eye_x = self.x + eye_distance * math.cos(alpha_rad + eye_offset_rad)
        right_eye_y = self.y + eye_distance * math.sin(alpha_rad + eye_offset_rad)

        # draw eyes
        pygame.draw.circle(self.screen, (0, 0, 0), (left_eye_x, left_eye_y), eye_radius)
        pygame.draw.circle(self.screen, (0, 0, 0), (right_eye_x, right_eye_y), eye_radius)