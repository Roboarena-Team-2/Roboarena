import pygame
import math
import numpy as np
import config

BOUNDS_X = [0, config.WIDTH]
BOUNDS_Y = [0, config.HEIGHT]

a_max = 1
a_alpha_max = 1

class Robot:
    def __init__(self, screen, x, y, radius, direction, color, a, a_alpha):
        self.screen = screen
        self.x = x  # x-coordiante of center
        self.y = y  # y-coordinate of center
        self.r = radius  # radius of circle
        self.alpha = direction  # direction of the robot
        self.color = color  # color of the robot
        self.a = a  # current acceleration for moving
        self.a_alpha = a_alpha  # current acceleration for turning
        self.a_max = a_max  # maximal acceleration for moving    (constant in program)
        self.a_alpha_max = a_alpha_max  # maximal acceleration for turning     (constant in program)
        self.v = 1  # speed for moving
        self.v_alpha = 1  # speed for turning

    def draw_robot(self):
        # draw robot (circle)
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

        # calculate values for eyes
        eye_radius = self.r * 0.1  # radius of the eyes
        eye_offset_deg = 30   # deviation of angle of the eyes from direction
        eye_offset_rad = math.radians(eye_offset_deg)  # convert to radian
        eye_distance = self.r * 0.6  # distance from center of the robot

        alpha_rad = math.radians(self.alpha)

        left_eye_x = self.x + (
            eye_distance * math.cos(alpha_rad - eye_offset_rad))
        left_eye_y = self.y + (
            eye_distance * math.sin(alpha_rad - eye_offset_rad))
        right_eye_x = self.x + (
            eye_distance * math.cos(alpha_rad + eye_offset_rad))
        right_eye_y = self.y + (
            eye_distance * math.sin(alpha_rad + eye_offset_rad))

        # draw eyes
        pygame.draw.circle(self.screen, (0, 0, 0),
                           (left_eye_x, left_eye_y), eye_radius)
        pygame.draw.circle(self.screen, (0, 0, 0),
                           (right_eye_x, right_eye_y), eye_radius)
        

    def update_player(self):
        self.draw_robot()

        keys = pygame.key.get_pressed()

        self.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.v
        self.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.v
        self.alpha += (keys[pygame.K_d] - keys[pygame.K_a]) * self.v_alpha

        self.x = max(BOUNDS_X[0], min(self.x, BOUNDS_X[1] - self.r))
        self.y = max(BOUNDS_Y[0], min(self.y, BOUNDS_Y[1] - self.r))


    def update_enemy(self, player):
        x_to_goal = player.x-self.x
        y_to_goal = player.y-self.y
        self.x += math.copysign(self.v, x_to_goal)  / 3
        self.y += math.copysign(self.v, y_to_goal)  / 3
        angle_to_player = math.degrees(math.atan2(y_to_goal,x_to_goal))+180%360
        if(angle_to_player<self.alpha):
            if(abs(angle_to_player-self.alpha)>180):
                angle_to_player *= -1
        else:
            if(abs(angle_to_player-self.alpha)<180):
                angle_to_player *= -1
        self.alpha += math.copysign(self.v_alpha, angle_to_player)
        self.draw_robot()

    def move_circle(self,point,r,angle):
        self.x = point[0] + r * math.cos(angle*math.pi/180)
        self.y = point[1] + r * math.sin(angle*math.pi/180)
        self.alpha = angle + 90
        self.draw_robot()
