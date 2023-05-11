import pygame
from enum import Enum

class Player:

    class Directions(Enum):
        LEFT = 1
        RIGHT = 2

    def __init__(self, image, speed):
        self.speed = speed
        self.image = image