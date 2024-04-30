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

# colors
gray = (80, 80, 80)
green = (0,150, 0)
red = (200, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 232, 0)

# road and edge markers
road_rect = (100, 0, road_width, window_height)
left_edge_marker_rect = (95, 0, marker_width, window_height)
right_edge_marker_rect = (395, 0, marker_width, window_height)

# road and marker sizes
road_width = 300
marker_width = 10
marker_height = 50

# for animating movement of the lane markers
lane_marker_move_y = 0

# game settings
is_game_over = False
speed = 2
score = 0

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

# game loop
running = True
while running:
    
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
        # move the player's car using the left/right arrow keys
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player_car.rect.center[0] > lane1:
                player_car.rect.x -= 100
            elif event.key == K_RIGHT and player_car.rect.center[0] < lane3:
                player_car.rect.x += 100
                
            # check if there's a side swipe collision after changing lanes
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player_car, vehicle):
                    is_game_over = True
                    # place the player's car next to other vehicle
                    # and determine where to position the crash image
                    if event.key == K_LEFT:
                        player_car.rect.left = vehicle.rect.right
                        crash_rect.center = [player_car.rect.left, (player_car.rect.center[1] + vehicle.rect.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        player_car.rect.right = vehicle.rect.left
                        crash_rect.center = [player_car.rect.right, (player_car.rect.center[1] + vehicle.rect.center[1]) / 2]
            
    # draw the grass
    screen.fill(green)
    
    # draw the road
    pygame.draw.rect(screen, gray, road_rect)
    
    # draw the edge markers
    pygame.draw.rect(screen, yellow, left_edge_marker_rect)
    pygame.draw.rect(screen, yellow, right_edge_marker_rect)
    
    # draw the lane markers
    for y in range(marker_height * -2, window_height, marker_height * 2):
        pygame.draw.rect(screen, white, (lane1 + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (lane2 + 45, y + lane_marker_move_y, marker_width, marker_height))
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0
        
    # draw the player's car
    player_group.draw(screen)
    
    
