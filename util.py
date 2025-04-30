import random

from pygame.image import load
from pygame import Surface, Vector2, Color
from pygame.mixer import Sound

def load_sprite(name: str, with_alpha: bool=True) -> Surface:
    path = f"assets/sprites/{name}.png"
    load_sprite = load(path)

    if with_alpha:
        return load_sprite.convert_alpha()
    else:
        return load_sprite.convert()
    
def wrap_position(position: tuple, surface: Surface) -> Vector2:
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)

def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )

def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)

def load_sound(name):
    path = f"assets/sounds/{name}.wav"
    return Sound(path)

def print_text(surface, text, font, color=Color("tomato")):
    text_surface = font.render(text, True, color)

    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2

    surface.blit(text_surface, rect)