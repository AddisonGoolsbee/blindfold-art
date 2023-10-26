import socket
import pygame
import sys

MULTIPLIER = 0.005
TIME = 120000  # 2 minutes in milliseconds

ip_address = "0.0.0.0"
port = 12345

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((ip_address, port))

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Setting up font
font_size = 48
font = pygame.font.SysFont(None, font_size)
text = font.render("Draw a Cat", True, WHITE)
text_rect = text.get_rect(center=(width / 2, font_size / 2))


def draw_dot(x, y, color=WHITE):
    x = x * width
    y = height - (y * (height - font_size))
    pygame.draw.circle(screen, color, (int(x), int(y)), 5)


x_loc = 0.5
y_loc = 0.5
screen.fill(BLACK)

# Timer
start_ticks = pygame.time.get_ticks()


# Main game loop
running = True
while running:
    clear_rect = pygame.Rect(0, 0, width, font_size)
    screen.fill(BLACK, clear_rect)
    screen.blit(text, text_rect.topleft)

    draw_dot(x_loc, y_loc, GRAY)

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
        text = font.render("Amazing!", True, WHITE)
        text_rect = text.get_rect(center=(width / 2, font_size / 2))

    else:
        data, address = udp_socket.recvfrom(1024)
        data = data.decode("utf-8").strip()
        data_split = data.split(",")
        pitch = float(data_split[0][(data_split[0].find(": ") + 2) :])
        yaw = float(data_split[1][(data_split[1].find(": ") + 2) :])

        print(pitch, yaw)
        pitch = pitch * MULTIPLIER
        yaw = yaw * MULTIPLIER

        x_loc = max(0, min(1, x_loc + pitch))
        y_loc = max(0, min(1, y_loc + yaw))

        draw_dot(x_loc, y_loc)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
