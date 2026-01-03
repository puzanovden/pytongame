import pygame
import math
from enum import IntEnum
import physics

class Team(IntEnum):
    NEUTRAL = 0
    PLAYER = 1
    ENEMY = 2


class ObjectType(IntEnum):
    GENERIC = 0
    CHARACTER = 1
    LOOT = 2
    PROJECTILE = 3

class GameObjectDef:
    def __init__(
        self,
        obj_type: ObjectType,
        sprite: pygame.Surface,
        sprite_count: int,
        diameter: float,
        default_team: Team = Team.NEUTRAL,
        overlap_limit=0.75
    ):
        self.obj_type = obj_type
        self.sprite = sprite
        self.sprite_count = sprite_count
        self.diameter = diameter
        self.default_team = default_team
        self.overlap_limit = overlap_limit

class GameObject:
    def __init__(
        self,
        obj_def: GameObjectDef,
        x: float,
        y: float,
        angle: float = 0.0,
        team: Team | None = None,
        speed = 0.0
    ):
        self.defn = obj_def

        self.x = x
        self.y = y
        self.angle = angle

        self.team = team if team is not None else obj_def.default_team

        self.sprite_index = 0
        self.alive = True
        self.speed = speed

    def update(self, dt: float):
        pass

    def draw(self, surface):
        sprite = self.defn.sprite

        if self.defn.sprite_count > 1:
            frame_w = sprite.get_width() // self.defn.sprite_count
            frame = sprite.subsurface(
                frame_w * self.sprite_index,
                0,
                frame_w,
                sprite.get_height()
            )
        else:
            frame = sprite

        size = int(self.defn.diameter)
        frame = pygame.transform.scale(frame, (size, size))

        frame = pygame.transform.rotate(frame, self.angle)

        rect = frame.get_rect(center=(self.x, self.y))
        surface.blit(frame, rect.topleft)

        # pygame.draw.circle(
        #     surface, (0, 255, 0),
        #     (int(self.x), int(self.y)),
        #     int(self.defn.diameter // 2), 2
        #)

    def rotate(self, dx, dy):
        if dx or dy:
            self.angle = math.degrees(
                math.atan2(-dy, dx)
            )

    def move(self, dx, dy, dt):
        physics.move(self, dx, dy, dt)

    




