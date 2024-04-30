import pygame
from pygame.locals import *
import random

pygame.init()

# create the window
window_width = 500
window_height = 500
window_size = (window_width, window_height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Car Racing Game')

# lane coordinates
lane1 = 150
lane2 = 250
lane3 = 350
lanes = [lane1, lane2, lane3]

# frame settings
clock = pygame.time.Clock()
fps = 120

# player's starting coordinates
player_x = 150
player_y = 400

class Vehicle(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # scale the image down so it's not wider than the lane
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (int(new_width), int(new_height)))
        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
class PlayerVehicle(Vehicle):
    
    def __init__(self, x, y):
        image = pygame.image.load('images/car.png')
        super().__init__(image, x, y)
        
# sprite groups
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

# create the player's car
player_car = PlayerVehicle(player_x, player_y)
player_group.add(player_car)

# load the vehicle images
vehicle_image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = []
for filename in vehicle_image_filenames:
    image = pygame.image.load('images/' + filename)
    vehicle_images.append(image)
    
# load the crash image
crash_image = pygame.image.load('images/crash.png')
crash_rect = crash_image.get_rect()

