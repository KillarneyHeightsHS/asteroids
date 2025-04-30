from pygame.math import Vector2
from pygame.sprite import Sprite
from pygame.transform import rotozoom
from pygame import Surface
from typing import Self, Callable
from util import get_random_velocity, load_sound, load_sprite, wrap_position

UP = Vector2(0, -1)

class GameObject:
    MANEUVERABILITY = 3
    ACCELERATION = 0.25
    DECELERATION = 0.1
    MAX_VELOCITY = 5
    MIN_VELOCITY = 0
    BULLET_SPEED = 3

    def __init__(self, position: tuple, sprite: Sprite, velocity: tuple) -> None:
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface: Surface) -> None:
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface: Surface) -> None:
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj: Self) -> bool:
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius

class Bullet(GameObject):
    def __init__(self, position: tuple, velocity: tuple) -> None:
        super().__init__(position, load_sprite("bullet"), velocity)
    
    def move(self, surface: Surface):
        self.position = self.position + self.velocity

class Spaceship(GameObject):
    def __init__(self, position: tuple, create_bullet_callback: Callable[[Bullet], None]) -> None:
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")
        self.explosion_sound = load_sound("explosion")
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("spaceship"), Vector2(0))

    def rotate(self, clockwise=True) -> None:
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self) -> None:
        self.velocity += self.direction * self.ACCELERATION
        if (self.velocity.x > self.MAX_VELOCITY): 
            self.velocity.x = self.MAX_VELOCITY
        if (self.velocity.x < -self.MAX_VELOCITY): 
            self.velocity.x = -self.MAX_VELOCITY
        if (self.velocity.y > self.MAX_VELOCITY): 
            self.velocity.y = self.MAX_VELOCITY
        if (self.velocity.y < -self.MAX_VELOCITY): 
            self.velocity.y = -self.MAX_VELOCITY

    def decelerate(self) -> None:
        self.velocity -= self.direction * self.DECELERATION
        if (abs(self.velocity.x) > self.MIN_VELOCITY): 
            self.velocity.x = self.MIN_VELOCITY
        if (abs(self.velocity.y) > self.MIN_VELOCITY): 
            self.velocity.y = self.MIN_VELOCITY

    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()

    def destroy(self):
        self.explosion_sound.play()

    def draw(self, surface: Surface) -> None:
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

class Asteroid(GameObject):
    def __init__(self, position: tuple, create_asteroid_callback, size: int=3) -> None:
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size

        size_to_scale = {
            3: 1,
            2: 0.5,
            1: 0.25,
        }

        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("asteroid"), 0, scale)
        super().__init__(
            position, sprite, get_random_velocity(1, 3)
        )

    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(
                    self.position, self.create_asteroid_callback, self.size - 1
                )
                self.create_asteroid_callback(asteroid)        

            
