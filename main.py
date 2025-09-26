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
font24 = pygame.font.Font("assets/fonts/font.ttf", 24)
font48 = pygame.font.Font("assets/fonts/font.ttf", 48)

# Load Sounds
swing_sfx = pygame.mixer.Sound("assets/sounds/swing.mp3")

# Load Textures
icon = pygame.image.load("assets/textures/icon.png")
ball_img = pygame.image.load("assets/textures/ball.png")
ball_shadow_img = pygame.image.load("assets/textures/ball_shadow.png")
bg_img = pygame.image.load("assets/textures/bg.png")
arrow_img = pygame.image.load("assets/textures/arrow.png")

pygame.display.set_icon(icon)

# Game Variables
game_state = 1  # 0 - title, 1 - game, 2 - end
friction = .015
ball_width = 16


# ------------------------
# Classes
# ------------------------

class Ball:
    def __init__(self, x, y):
        self.init_pos = [x, y]
        self.pos = [x, y]
        self.velo = [0, 0]
    
    def draw(self):
        window.blit(ball_shadow_img, (self.pos[0], self.pos[1] + 4))
        window.blit(ball_img, (self.pos[0], self.pos[1]))
        
    def update(self):
        self.change_velocity()
        self.check_for_collision(0, 0, window_w, window_h)
        self.change_position()
        
    # Getters/Setters
    
    def is_moving(self):
        return self.get_speed() > 0        
        
    def get_speed(self):
        xvelo, yvelo = self.velo
        # Returns hypotenuse of the velocity vectors
        return math.sqrt((xvelo*xvelo)+(yvelo*yvelo))
    
    def get_next_velocity(self):
        xvelo, yvelo = self.velo[0], self.velo[1]
        speed = math.sqrt((xvelo*xvelo)+(yvelo*yvelo))
        
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
        
        return xvelo, yvelo
    
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
        
        # Get Current Position
        xpos, ypos = self.pos[0], self.pos[1]
        xvelo, yvelo = self.velo[0], self.velo[1]
        
        # Predicts Next Position
        center_line = w/2
        velos = self.get_next_velocity()
        next_x = velos[0] + xpos
        next_y = velos[1] + ypos
        
        # Check for collision with outer wall
        if (xpos + ball_width < w) and (next_x + ball_width > w):
            xvelo = -xvelo
        elif (xpos > x) and (next_x < x):
            xvelo = -xvelo          
            
        if (ypos + ball_width < h) and (next_y + ball_width > h):
            yvelo = -yvelo
        elif (ypos > y) and (next_y < y):
            yvelo = -yvelo
            
        
        # If next position is over center wall, flip velo
        if(xpos + ball_width < center_line and next_x > center_line - ball_width) or (xpos > center_line and next_x < center_line):
            xvelo = -xvelo
        
        
        self.set_position(xpos, ypos)
        self.set_velocity(xvelo, yvelo)


def play():
    global game_state
    global friction
    global balls
    global stroke_count
    global level
    global initMousePos
    global mouse_pressed
    
    # ------------------------
    # Initialize Game Objects/Variables
    # ------------------------
    
    initMousePos = [0, 0]
    endMousePos = [0, 0]
    mouse_pressed = False
    
    stroke_count = 0
    level = 1
    
    
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
                mouse_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                endMousePos = pygame.mouse.get_pos()
                if not balls[0].is_moving():
                    balls[0].hit_ball(initMousePos, endMousePos)
                    balls[1].hit_ball(initMousePos, endMousePos)
                    stroke_count = stroke_count + 1
                mouse_pressed = False
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
    
    if mouse_pressed == True and not balls[0].is_moving():
        draw_arrow()
    
    draw_stroke_count()
    draw_hole_count()
    
def draw_arrow():
    currentMousePos = pygame.mouse.get_pos()
    dx = currentMousePos[0] - initMousePos[0]
    dy = currentMousePos[1] - initMousePos[1]
    
    angle = math.atan2(dx, dy)
    angle = math.degrees(angle)
    pivot = (arrow_img.get_width() / 2, arrow_img.get_height())

    rotate_arrow(balls[0].pos[0], balls[0].pos[1], pivot, angle)
    rotate_arrow(balls[1].pos[0], balls[1].pos[1], pivot, angle)
    

def rotate_arrow( xpos, ypos, pivot, angle):
    
    image_rect = arrow_img.get_rect(topleft=(0, 0))
    
    # Calculate the pivot vector (relative to image) and rotate image/vector
    pivot_vector = pygame.math.Vector2(pivot) - image_rect.center
    rotated_image = pygame.transform.rotate(arrow_img, angle)
    rotated_rect = rotated_image.get_rect()
    rotated_pivot = pivot_vector.rotate(-angle)
    rotated_rect.center = (xpos + 8 - rotated_pivot.x, ypos + 8 - rotated_pivot.y)
    window.blit(rotated_image, rotated_rect)

def draw_stroke_count():
    
    draw_rectangle((window_w/2) - 96, 0, 192, 32, 128, bblr=5, bbrr=5)
    draw_shadowed_text(font24, "STROKES: " + str(stroke_count), window_w/2, 19, 0, 0, 0)
    draw_shadowed_text(font24, "STROKES: " + str(stroke_count), window_w/2, 16, 255, 255, 255)
    
def draw_hole_count():
    
    # LEFT SIDE
    draw_rectangle(96, window_h - 32, 128, 32, 128, btlr=5, btrr=5)
    draw_shadowed_text(font24, "HOLE: " + str(level), window_w/4, window_h - 13, 0, 0, 0)
    draw_shadowed_text(font24, "HOLE: " + str(level), window_w/4, window_h - 16, 255, 255, 255)
    
    # RIGHT SIDE
    draw_rectangle(window_w - 128 - 96, window_h - 32, 128, 32, 128, btlr=5, btrr=5)
    draw_shadowed_text(font24, "HOLE: " + str(level + 1), 3 * (window_w/4), window_h - 13, 0, 0, 0)
    draw_shadowed_text(font24, "HOLE: " + str(level + 1), 3 * (window_w/4), window_h - 16, 255, 255, 255)

def draw_rectangle(x, y, w, h, a, btlr=0, btrr=0, bblr=0, bbrr=0):
    # Create Temporary Surface to Allow Transparent Rectangles
    temp_surf = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(temp_surf, (0, 0, 0, a), (0, 0, w, h), border_top_left_radius=btlr, border_top_right_radius=btrr, border_bottom_left_radius=bblr, border_bottom_right_radius=bbrr)
    window.blit(temp_surf, (x, y))

def draw_shadowed_text(font: pygame.font.Font, words: str, x, y, r, g, b):
    text = font.render(words, True, (r, g, b))
    text_location = text.get_rect(center=(x, y))
    window.blit(text, text_location)

    
def update_objects():
    balls[0].update()
    balls[1].update()


if __name__ == "__main__":
    play()
    