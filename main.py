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
font32 = pygame.font.Font("assets/fonts/font.ttf", 32)

# Load Sounds
swing_sfx = pygame.mixer.Sound("assets/sounds/swing.mp3")
charge_sfx = pygame.mixer.Sound("assets/sounds/charge.mp3")
hole_sfx = pygame.mixer.Sound("assets/sounds/hole.mp3")

# Load Textures
icon = pygame.image.load("assets/textures/icon.png")
title_logo = pygame.image.load("assets/textures/title_logo.png")
ball_img = pygame.image.load("assets/textures/ball.png")
hole_img = pygame.image.load("assets/textures/hole.png")
ball_shadow_img = pygame.image.load("assets/textures/ball_shadow.png")
bg_img = pygame.image.load("assets/textures/bg.png")
arrow_img = pygame.image.load("assets/textures/arrow.png")
meter_bg = pygame.image.load("assets/textures/powermeter_bg.png")
meter_fg = pygame.image.load("assets/textures/powermeter_fg.png")


pygame.display.set_icon(icon)

# Game Variables
game_state = 0  # 0 - title, 1 - game, 2 - end
friction = .015
fg_power_w, fg_power_h = meter_fg.get_size()
power_offset = 4
ball_width = 16
max_ball_speed = 400

title_pos = 88
title_amplitude = 8
title_speed = 2

charge_sfx_played = False


# ------------------------
# Classes
# ------------------------

class Hole:
    def __init__(self, x, y):
        self.pos = [x, y]
    
    def draw(self):
        window.blit(hole_img, (self.pos[0], self.pos[1]))
        
    def change_position(self, x, y):
        self.pos = [x, y]
        
    def update(self):
        # Checks if ball goes in hole
        
        for ball in balls:
            if not ball.finished:
                # Distance between ball and hole center
                dx = (ball.pos[0] + ball_width / 2) - (self.pos[0] + hole_img.get_width() / 2)
                dy = (ball.pos[1] + ball_width / 2) - (self.pos[1] + hole_img.get_height() / 2)
                dist = math.sqrt(dx * dx + dy * dy)

                # If close enough, mark ball as finished
                if dist < 8:  # tune this radius as needed
                    ball.finished = True
                    pygame.mixer.Sound.play(hole_sfx)
                    ball.set_velocity(0, 0)

class Ball:
    def __init__(self, x, y):
        self.init_pos = [x, y]
        self.pos = [x, y]
        self.velo = [0, 0]
        self.finished = False
    
    def draw(self):
        if not self.finished:
            window.blit(ball_shadow_img, (self.pos[0], self.pos[1] + 4))
            window.blit(ball_img, (self.pos[0], self.pos[1]))
        
    def update(self):
        if not self.finished:
            self.change_velocity()
            self.check_for_wall_collision(0, 0, window_w, window_h)
            self.change_position()
        
    # Getters/Setters
    
    def is_moving(self):
        return self.get_speed() > 0        
        
    def get_speed(self):
        xvelo, yvelo = self.velo
        # Returns hypotenuse of the velocity vectors
        return math.sqrt((xvelo*xvelo)+(yvelo*yvelo))
    
    def get_potential_speed(self, x, y):
        return math.sqrt((x*x)+(y*y))
    
    def get_next_velocity(self):
        xvelo, yvelo = self.velo[0], self.velo[1]
        speed = self.get_potential_speed(xvelo, yvelo)
        
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
        self.finished = False
        
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
        if not self.finished:
            xvelo = -(endMousePos[0] - initialMousePos[0]) / 50
            yvelo = -(endMousePos[1] - initialMousePos[1]) / 50
            self.set_velocity(xvelo, yvelo)
            pygame.mixer.Sound.play(swing_sfx)
        
    def check_for_wall_collision(self, x, y, w, h):
        
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
    global holes
    global completed
    global stroke_count
    global level
    global initMousePos
    global mouse_pressed
    global charge_sfx_played
    
    # ------------------------
    # Initialize Game Objects/Variables
    # ------------------------
    
    initMousePos = [0, 0]
    endMousePos = [0, 0]
    mouse_pressed = False
    
    stroke_count = 0
    level = 1
    
    
    balls = [Ball(160, 360), Ball(480, 360)]
    holes = [Hole(160, 64), Hole(496, 80)]
    
    # Title Screen
    while game_state == 0:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                game_state = 1
        
        # Draw Objects
        draw_objects()
        # Update window
        pygame.display.update()
        
    
    pygame.mixer.Sound.play(swing_sfx)
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
                if (not balls[0].is_moving() and (not balls[0].finished or not balls[1].finished)):
                    balls[0].hit_ball(initMousePos, endMousePos)
                    balls[1].hit_ball(initMousePos, endMousePos)
                    stroke_count = stroke_count + 1
                mouse_pressed = False
                charge_sfx_played = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    balls[0].reset()
                    balls[1].reset()
        
        #Update Objects
        update_objects()
        
        # Draw Objects
        draw_objects()
        # Update window
        pygame.display.update()


# ------------------------
# Draw Functions
# ------------------------      

def animate_title_logo():
    time_now = pygame.time.get_ticks() / 1000.0  # seconds since pygame.init
    offset = math.sin(time_now * title_speed) * title_amplitude
    window.blit(title_logo, (160, title_pos + offset))


def draw_objects():
    global charge_sfx_played
    # Clear the screen
    window.blit(bg_img, (0, 0))
    
    if game_state == 0:
        animate_title_logo()
        draw_rectangle(184, 328, 272, 48, 128, 5, 5, 5, 5)
        draw_shadowed_text(font32, "LEFT CLICK TO START", 320, 352)
    
    elif game_state == 1:
        
        holes[0].draw()
        holes[1].draw()
    
        balls[0].draw()
        balls[1].draw()
        
        
        if mouse_pressed == True and not balls[0].is_moving():
            draw_arrow()
            
            # Calculate speed continuously while dragging
            curMousePos = pygame.mouse.get_pos()
            x = initMousePos[0] - curMousePos[0]
            y = initMousePos[1] - curMousePos[1]
            speed = balls[0].get_potential_speed(x, y)
            draw_power_box(speed)
            
            if charge_sfx_played == False:
                charge_sfx_played = True
                pygame.mixer.Sound.play(charge_sfx)
        
        draw_stroke_count()
        draw_hole_count()
    
def draw_power_box(speed):
    scale = min(speed / max_ball_speed, 1.0)
    
    new_height = (fg_power_h * scale)
    
    scaled_texture = pygame.transform.smoothscale(meter_fg, (fg_power_w, new_height))
    
    for ball in balls:
        if not ball.finished:
            xpos, ypos = ball.pos[0], ball.pos[1]
            xpos = xpos + 40
            ypos = ypos - 32
            
            window.blit(meter_bg, (xpos, ypos))
            window.blit(scaled_texture, (xpos + power_offset, ypos + power_offset + fg_power_h - new_height))
        
        
    
def draw_arrow():
    currentMousePos = pygame.mouse.get_pos()
    dx = currentMousePos[0] - initMousePos[0]
    dy = currentMousePos[1] - initMousePos[1]
    
    angle = math.atan2(dx, dy)
    angle = math.degrees(angle)
    pivot = (arrow_img.get_width() / 2, arrow_img.get_height())

    if not balls[0].finished:
        rotate_arrow(balls[0].pos[0], balls[0].pos[1], pivot, angle)
    if not balls[1].finished:
        rotate_arrow(balls[1].pos[0], balls[1].pos[1], pivot, angle)

def rotate_arrow(xpos, ypos, pivot, angle):
    
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
    draw_shadowed_text(font24, "STROKES: " + str(stroke_count), window_w/2, 16)
    
def draw_hole_count():
    
    # LEFT SIDE
    draw_rectangle(96, window_h - 32, 128, 32, 128, btlr=5, btrr=5)
    draw_shadowed_text(font24, "HOLE: " + str(level), window_w/4, window_h - 16)
    
    # RIGHT SIDE
    draw_rectangle(window_w - 128 - 96, window_h - 32, 128, 32, 128, btlr=5, btrr=5)
    draw_shadowed_text(font24, "HOLE: " + str(level + 1), 3 * (window_w/4), window_h - 16)

def draw_rectangle(x, y, w, h, a, btlr=0, btrr=0, bblr=0, bbrr=0):
    # Create Temporary Surface to Allow Transparent Rectangles
    temp_surf = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(temp_surf, (0, 0, 0, a), (0, 0, w, h), border_top_left_radius=btlr, border_top_right_radius=btrr, border_bottom_left_radius=bblr, border_bottom_right_radius=bbrr)
    window.blit(temp_surf, (x, y))

def draw_shadowed_text(font: pygame.font.Font, words: str, x, y):
    w_text = font.render(words, True, (255, 255, 255))
    b_text = font.render(words, True, (0, 0, 0))
    
    w_text_location = w_text.get_rect(center=(x, y))
    b_text_location = w_text.get_rect(center=(x, y+3))
    
    window.blit(b_text, b_text_location)
    window.blit(w_text, w_text_location)

def update_objects():
    balls[0].update()
    balls[1].update()
    
    holes[0].update()
    holes[1].update()


if __name__ == "__main__":
    play()
    