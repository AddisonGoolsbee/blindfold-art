import random
import socket
import pygame
import sys
from enum import Enum

MULTIPLIER = 0.005
TIME = 120000  # 2 minutes in milliseconds
START_MESSAGE = "Welcome Gamma Gary\n\nPlease make sure you have a companion with you\nTo begin, please dip your hands in water and put a blindfold on\nyour partner (Peter Scottsen) will try to guide you through a painting\nWhen you are ready, firmly grab the two metal bars\nof the device with the gold circle facing you\nand hold it at head level"
INACTIVE_DURATION = 3000
FINISH_RESTART_DURATION = 20000

drawing_list = [
    "Cat",
    "Dog",
    "Tree",
    "Sun",
    "Moon",
    "Star",
    "Fish",
    "Bird",
    "House",
    "Car",
    "Boat",
    "Flower",
    "Apple",
    "Banana",
    "Hat",
    "Shoe",
    "Book",
    "Chair",
    "Table",
    "Ball",
    "Circle",
    "Square",
    "Triangle",
    "Heart",
    "Smile",
    "Cloud",
    "Raindrop",
    "Snowflake",
    "Mountain",
    "River",
    "Ocean",
    "Beach",
    "Island",
    "Forest",
    "Desert",
    "Sky",
    "Grass",
    "Leaf",
    "Branch",
    "Roots",
    "Bear",
    "Lion",
    "Tiger",
    "Elephant",
    "Monkey",
    "Giraffe",
    "Kangaroo",
    "Horse",
    "Cow",
    "Pig",
    "Chicken",
    "Duck",
    "Goose",
    "Turkey",
    "Deer",
    "Rabbit",
    "Fox",
    "Wolf",
    "Owl",
    "Eagle",
    "Parrot",
    "Penguin",
    "Dolphin",
    "Whale",
    "Shark",
    "Octopus",
    "Crab",
    "Lobster",
    "Snail",
    "Butterfly",
    "Bee",
    "Ant",
    "Spider",
    "Frog",
    "Turtle",
    "Snake",
    "Lizard",
    "Dinosaur",
    "Dragon",
    "Unicorn",
    "Fairy",
    "Angel",
    "Robot",
    "Alien",
    "Monster",
    "Zombie",
    "Vampire",
    "Ghost",
    "Witch",
    "Wizard",
    "King",
    "Queen",
    "Prince",
    "Princess",
    "Knight",
    "Pirate",
    "Ninja",
    "Samurai",
    "Cowboy",
    "Astronaut",
]

class State(Enum):
    NEW = 1
    RUNNING = 2
    FINISHED = 3

ip_address = "0.0.0.0"
port = 12346

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((ip_address, port))
udp_socket.settimeout(1)  # Set a timeout of 1 second

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

# Setting up font
font_size = 60
font = pygame.font.SysFont(None, font_size)


def draw_dot(x, y, size, color=WHITE):
    x = x * width
    y = height - (y * (height - font_size * 1.5))
    adjusted_size = size * 30.0
    pygame.draw.circle(screen, color, (int(x), int(y)), adjusted_size)

state = State.NEW
x_loc = 0.5
y_loc = 0.5
touch = 0.0
previous_x = 0.5
previous_y = 0.5
screen.fill(BLACK)
drawing = random.choice(drawing_list)
mission_text = font.render(f"Draw a{'n' if drawing[0].lower() in 'aeiou' else ''} {drawing.lower()}", True, WHITE)
text_rect = mission_text.get_rect(center=(width / 2, font_size / 2))
inactive_time = None
inactive = True
was_inactive = False
finish_time = None

# Timer
start_ticks = pygame.time.get_ticks()

def display_start():
    screen.fill(BLACK)
    text_rendered = [font.render(line, True, WHITE) for line in START_MESSAGE.split('\n')]
    y = 30
    for text in text_rendered:
        text_rect = text.get_rect(center=(width // 2, y))
        screen.blit(text, text_rect)
        y += text.get_height()
    
# Main game loop
running = True

display_start()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            running = False
    
    try:
        data, address = udp_socket.recvfrom(1024)
    

        data = data.decode("utf-8").strip()
        data_split = data.split(",")
        pitch, roll, touch, hands = [float(i[(i.find(": ") + 2) :]) for i in data_split]
        

        if hands:
            if inactive_time is None:
                inactive_time = pygame.time.get_ticks()
            else:
                if pygame.time.get_ticks() - inactive_time >= INACTIVE_DURATION:
                    inactive = True
                    inactive_time = None
        else:
            inactive = False
            inactive_time = None

        # print(pitch, roll, touch, hands, inactive)

        if state == State.RUNNING:
            clear_rect = pygame.Rect(0, 0, width, font_size)
            screen.fill(BLACK, clear_rect)
            screen.blit(mission_text, text_rect.topleft)

            # Timer
            elapsed_time = pygame.time.get_ticks() - start_ticks
            remaining_time = max(TIME - elapsed_time, 0)
            minutes = remaining_time // 60000
            seconds = (remaining_time % 60000) // 1000
            timer_text = font.render(f"{int(minutes):02}:{int(seconds):02}", True, WHITE)
            timer_rect = timer_text.get_rect(topright=(width - 10, 10))
            screen.blit(timer_text, timer_rect.topleft)

            if remaining_time == 0 or inactive:
                state=State.FINISHED
                finish_time = pygame.time.get_ticks()
                
            else:
                pitch = pitch * MULTIPLIER
                roll = roll * MULTIPLIER

                x_loc = max(0, min(1, x_loc + roll))
                y_loc = max(0, min(1, y_loc + pitch))
                
                if not hands:
                    draw_dot(previous_x, previous_y, 0.1, BLACK)
                    draw_dot(x_loc, y_loc, touch, color=WHITE)
                    draw_dot(x_loc, y_loc, 0.1, WHITE)
                
                previous_x = x_loc
                previous_y = y_loc

        elif state == State.NEW:
            if not hands:
                screen.fill(BLACK)
                drawing = random.choice(drawing_list)
                mission_text = font.render(f"Draw a{'n' if drawing[0].lower() in 'aeiou' else ''} {drawing.lower()}", True, WHITE)
                text_rect = mission_text.get_rect(center=(width / 2, font_size / 2))
                start_ticks = pygame.time.get_ticks()
                was_inactive = False
                state = State.RUNNING

        elif state == State.FINISHED:
            clear_rect = pygame.Rect(0, 0, width, font_size)
            screen.fill(BLACK, clear_rect)
            display_text = font.render("Amazing "+ drawing + "!", True, WHITE)
            display_rect = display_text.get_rect(center=(width / 2, font_size / 2))
            screen.blit(display_text, display_rect)

            if inactive:
                was_inactive = True
                if pygame.time.get_ticks() - finish_time >= FINISH_RESTART_DURATION:
                    display_start()
                    was_inactive = False
                    state = State.NEW
            elif was_inactive and not inactive:
                screen.fill(BLACK)
                drawing = random.choice(drawing_list)
                mission_text = font.render(f"Draw a{'n' if drawing[0].lower() in 'aeiou' else ''} {drawing.lower()}", True, WHITE)
                text_rect = mission_text.get_rect(center=(width / 2, font_size / 2))
                start_ticks = pygame.time.get_ticks()
                was_inactive = False
                state = State.RUNNING

    except socket.error as e:
        pass


    pygame.display.flip()

pygame.quit()
sys.exit()
