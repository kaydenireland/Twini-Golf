import pygame
import math
import sys


pygame.init()


# ------------------------
# Variable Initialization
# ------------------------

# Window Setup
window_w = 640
window_h = 480

window = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption('Twini-Golf')

# Load Font
font = pygame.font.Font("assets/fonts/font.ttf", 48)

# Load Sounds
swing_sfx = pygame.mixer.Sound("assets/sounds/swing.mp3")

# Load Textures
ball_img = pygame.image.load("assets/textures/ball.png")

# Game Variables
game_state = 1  # 0 - title, 1 - game, 2 - end
friction = 3


# ------------------------
# Classes
# ------------------------

class Ball:
    def __init__(self, x, y):
        self.init_pos = [x, y]
        self.pos = [x, y]
        self.velo = [x, y]
    
    def draw(self):
        window.blit(ball_img, (self.pos[0], self.pos[1]))
        
    # Getters/Setters
    def get_speed(self):
        xvelo, yvelo = self.velo
        # Returns hypotenuse of the velocity vectors
        return math.sqrt((xvelo*xvelo)+(yvelo*yvelo))
    
    def set_position(self, x, y):
        self.pos = [x, y]
    
    def set_velocity(self, x, y):
        self.velo = [x, y]
        
    # Movement Methods




def play():
    global game_state;
    global friction;
    
    
    while game_state == 1:
        # Gameplay
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



if __name__ == "__main__":
    play()
    