import sys
import pygame
from pathlib import Path
import LogitechSteeringWheelPy as lsw
from LogitechSteeringWheelPy.g29 import G29

Button = G29.Button

# [Pygame] Prepare Window
pygame.init()
screen = pygame.display.set_mode((800, 200))
hwnd = pygame.display.get_wm_info()["window"]
clock = pygame.time.Clock()
pygame.display.set_caption("Pygame Client - LogitechSteeringWheelPy")
font = pygame.font.Font(None, 24)


def draw_text(text: str, color, dest):
    surface = font.render(text, True, color)
    screen.blit(surface, dest)


# [LogitechSteeringWheelPy] Initialize
dll_file = Path(
    Path("./DLLLocation.txt").read_text())  # Please create `DLLLocation.txt` and type the path to the dll file.
lsw.load_dll(dll_file)
initialized = lsw.initialize_with_window(True, hwnd)
assert initialized
g29 = lsw.G29(
    index=1,
    positive_angle="counterclockwise"
)

should_loop = True
while should_loop:
    lsw.update()
    g29.update()

    pressed_text = "Pressed: "
    triggered_text = "Triggered: "
    released_text = "Released: "
    for button in Button:
        if g29.is_pressed(button):
            pressed_text += str(button) + " "
        if button in G29.POV_BUTTONS:
            continue
        if g29.is_triggered(button):
            triggered_text += str(button) + " "
        if g29.is_released(button):
            released_text += str(button) + " "

    screen.fill((255, 255, 255))
    draw_text(pressed_text, (0, 0, 0), (0, 0))
    draw_text(triggered_text, (255, 100, 100), (0, 50))
    draw_text(released_text, (100, 100, 255), (0, 100))
    pygame.display.update()

    print(
        f"Steering Range = {g29.steering_range_rad:.03f} rad",
        f"Steering = {g29.steering_rad:.03f} rad",
        f"Throttle = {g29.throttle_normalized:.03f}",
        f"Brake = {g29.brake_normalized:.03f}",
        f"Updated At = {g29.updated_at}"
    )

    # [Pygame] Wait & Handle Events
    clock.tick(15)  # 15fps
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            should_loop = False

pygame.quit()
lsw.shutdown()  # DO NOT FORGET TO CALL THIS OR THE PYTHON PROCESS BECOMES ZOMBIE
sys.exit()
