import sys
import pygame
from pathlib import Path
import LogitechSteeringWheelPy as lsw
import json
from dataclasses import asdict

# [Pygame] Prepare Window
pygame.init()
screen = pygame.display.set_mode((640, 200))
hwnd = pygame.display.get_wm_info()["window"]
clock = pygame.time.Clock()
pygame.display.set_caption("Pygame Client - LogitechSteeringWheelPy")
font = pygame.font.Font(None, 24)
text = font.render("Look at the console, with keeping this window active.",True, (0, 0, 0))
text_rect = text.get_rect()
screen.fill((255, 255, 255))
screen.blit(
    text,
    (
        (screen.get_width()-text_rect.width)/2,
        (screen.get_height()-text_rect.height)/2
     )
)
pygame.display.update()

# [LogitechSteeringWheelPy] Initialize
dll_file = Path(Path("./DLLLocation.txt").read_text())
lsw.load_dll(dll_file)
initialized = lsw.initialize_with_window(True, hwnd)
assert initialized
g29 = lsw.G29(0)

should_loop = True
while should_loop:
    # [LogitechSteeringWheelPy] Update and Get State
    # lsw.update()
    # state = lsw.get_state(0)
    g29.update()
    state = g29.state
    state_dict = asdict(state)
    # print(state_dict)
    print(
        f"Steering Range = {g29.steering_range_rad:.03f} rad",
        f"Steering = {g29.steering_rad:.03f} rad",
        f"Throttle = {g29.throttle_normalized:.03f}",
        f"Brake = {g29.brake_normalized:.03f}",
        f"Updated At = {g29.updated_at}"
    )

    state_json = json.dumps(state_dict, indent=1)

    # [Pygame] Wait & Handle Events
    clock.tick(15)  # 15fps
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            should_loop = False

pygame.quit()
lsw.shutdown()  # DO NOT FORGET TO CALL THIS OR THE PYTHON PROCESS BECOMES ZOMBIE
sys.exit()
