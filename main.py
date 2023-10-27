import random
import socket
import pygame
import sys

MULTIPLIER = 0.005
TIME = 120000  # 2 minutes in milliseconds

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
    "Rain",
    "Snow",
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
GRAY = (200, 200, 200)

# Setting up font
font_size = 48
font = pygame.font.SysFont(None, font_size)


def draw_dot(x, y, size, color=WHITE):
    x = x * width
    y = height - (y * (height - font_size * 1.5))
    adjusted_size = size * 30.0 if size > 0.1 else 0
    pygame.draw.circle(screen, color, (int(x), int(y)), adjusted_size)


x_loc = 0.5
y_loc = 0.5
touch = 0.0
screen.fill(BLACK)
drawing = random.choice(drawing_list)
mission_text = font.render("Draw a " + drawing, True, WHITE)
text_rect = mission_text.get_rect(center=(width / 2, font_size / 2))

# Timer
start_ticks = pygame.time.get_ticks()


# Main game loop
running = True
while running:
    clear_rect = pygame.Rect(0, 0, width, font_size)
    screen.fill(BLACK, clear_rect)
    screen.blit(mission_text, text_rect.topleft)

    draw_dot(x_loc, y_loc, 0, GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            running = False

    # Timer
    elapsed_time = pygame.time.get_ticks() - start_ticks
    remaining_time = max(TIME - elapsed_time, 0)
    minutes = remaining_time // 60000
    seconds = (remaining_time % 60000) // 1000
    timer_text = font.render(f"{int(minutes):02}:{int(seconds):02}", True, WHITE)
    timer_rect = timer_text.get_rect(topright=(width - 10, 10))
    screen.blit(timer_text, timer_rect.topleft)

    if remaining_time == 0:
        mission_text = font.render(drawing, True, WHITE)
        text_rect = mission_text.get_rect(center=(width / 2, font_size / 2))

    else:
        data, address = udp_socket.recvfrom(1024)
        data = data.decode("utf-8").strip()
        data_split = data.split(",")
        pitch, roll, touch, hands = [float(i[(i.find(": ") + 2) :]) for i in data_split]

        print(pitch, roll, touch, hands)
        pitch = pitch * MULTIPLIER
        roll = roll * MULTIPLIER

        x_loc = max(0, min(1, x_loc + roll))
        y_loc = max(0, min(1, y_loc + pitch))
        
        if not hands:
            draw_dot(x_loc, y_loc, touch)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
