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
bg_img = pygame.image.load("assets/textures/bg.png")

# Game Variables
game_state = 1  # 0 - title, 1 - game, 2 - end
friction = .015


# ------------------------
# Classes
# ------------------------

class Ball:
    def __init__(self, x, y):
        self.init_pos = [x, y]
        self.pos = [x, y]
        self.velo = [0, 0]
    
    def draw(self):
        window.blit(ball_img, (self.pos[0], self.pos[1]))
        
    def update(self):
        self.change_velocity()
        self.check_for_collision(0, 0, window_w, window_h)
        self.change_position()
        
    # Getters/Setters
    def get_speed(self):
        xvelo, yvelo = self.velo
        # Returns hypotenuse of the velocity vectors
        return math.sqrt((xvelo*xvelo)+(yvelo*yvelo))
    
    def set_position(self, x, y):
        self.pos = [x, y]
    
    def set_velocity(self, x, y):
        self.velo = [x, y]
        
    def reset(self):
        # Resets the ball to original position with no velocity
        self.set_velocity(0,0)
        self.set_position(self.init_pos[0], self.init_pos[1])
        
    # Movement Methods
    
    def change_position(self):
        # Applies current velocity to position
        xpos, ypos = self.pos[0], self.pos[1]
        xpos = xpos + self.velo[0]
        ypos = ypos + self.velo[1]
        self.set_position(xpos, ypos)

    def change_velocity(self):
        xvelo, yvelo = self.velo[0], self.velo[1]
        speed = self.get_speed()

        # Uses speed to apply friction evenly to whole velocity vector

        if (speed > 0):
            xdir = xvelo / speed
            ydir = yvelo / speed

            speed = speed - friction
            if (speed < 0):
                speed = 0
            

            xvelo = xdir * speed
            yvelo = ydir * speed
        else:
            xvelo, yvelo = 0, 0
    

        self.set_velocity(xvelo, yvelo)
        
    def hit_ball(self, initialMousePos, endMousePos):
        xvelo = -(endMousePos[0] - initialMousePos[0]) / 50
        yvelo = -(endMousePos[1] - initialMousePos[1]) / 50
        self.set_velocity(xvelo, yvelo)
        pygame.mixer.Sound.play(swing_sfx)
        
    def check_for_collision(self, x, y, w, h):
        xpos, ypos = self.pos[0], self.pos[1]
        xvelo, yvelo = self.velo[0], self.velo[1]
        if (xpos > w):
            xvelo = -xvelo
            xpos = w - 1
        elif (xpos < x):
            xvelo = -xvelo
            xpos = x + 1
        if (ypos > h):
            yvelo = -yvelo
            ypos = h - 1
        elif (ypos < y):
            yvelo = -yvelo
            ypos = y + 1
        
        self.set_position(xpos, ypos)
        self.set_velocity(xvelo, yvelo)


def play():
    global game_state
    global friction
    global balls
    
    # ------------------------
    # Initialize Game Objects/Variables
    # ------------------------
    
    initMousePos = [0, 0]
    endMousePos = [0, 0]
    
    balls = [Ball(160, 360), Ball(480, 360)]
    
    # Game Loop
    while game_state == 1:
        # Gameplay
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                initMousePos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                endMousePos = pygame.mouse.get_pos()
                balls[0].hit_ball(initMousePos, endMousePos)
                balls[1].hit_ball(initMousePos, endMousePos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    balls[0].reset()
                    balls[1].reset()
                
                
        # ------------------------
        # 
        # ------------------------
        
        #Update Objects
        update_objects()
        
        # Draw Objects
        draw_objects()
        # Update window
        pygame.display.update()
            

def draw_objects():
    # Clear the screen
    window.blit(bg_img, (0, 0))
    
    balls[0].draw()
    balls[1].draw()
    
def update_objects():
    balls[0].update()
    balls[1].update()


if __name__ == "__main__":
    play()
    