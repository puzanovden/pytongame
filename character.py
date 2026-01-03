import pygame
import physics
from enum import IntEnum
from game_objects import *

class CharacterDef(GameObjectDef):
    def __init__(
        self,
        sprite,
        sprite_count,
        diameter,
        hp_max,
        speed,
        default_team
    ):
        super().__init__(
            ObjectType.CHARACTER,
            sprite,
            sprite_count,
            diameter,
            default_team
        )
        self.hp_max = hp_max
        self.speed = speed
        self._rmb_prev = False


class Character(GameObject):
    def __init__(self, char_def, x, y, is_player=False, weapons=None):
        super().__init__(char_def, x, y)
        self.hp = char_def.hp_max
        self.hp_max = self.hp
        self.speed = char_def.speed
        self.is_player = is_player

        self.weapons = weapons or []
        self.active_weapon = 0 if self.weapons else None

        self.contact_cd = 0.0

    @property
    def weapon(self):
        if self.active_weapon is None:
            return None
        return self.weapons[self.active_weapon]
    
    def add_weapon(self, weapon):
        self.weapons.append(weapon)

        if self.active_weapon is None:
            self.active_weapon = 0

    def switch_weapon(self):
        if not self.weapons:
            return

        self.active_weapon = (self.active_weapon + 1) % len(self.weapons)

    def update(self, dt, player=None):
        if self.weapon:
            self.weapon.update(dt)

        if self.contact_cd > 0:
            self.contact_cd -= dt

        if self.is_player:
            dx, dy, lx, ly = self.read_input()

            mo = pygame.mouse.get_pressed()
            if mo[0]:
                physics.shoot(self)

            rmb = mo[2]

            if rmb and not self._rmb_prev:
                self.switch_weapon()

            self._rmb_prev = rmb

        else:
            dx, dy, lx, ly = self.decide(player)

        physics.move(self, dx, dy, dt)
        self.rotate(lx, ly)

    def read_input(self):
        dx = dy = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        mx, my = pygame.mouse.get_pos()
        look_dx = mx - self.x
        look_dy = my - self.y

        return dx, dy, look_dx, look_dy

    def decide(self, player):
        if not player:
            return 0, 0, 0, 0

        dx = player.x - self.x
        dy = player.y - self.y

        return dx, dy, dx, dy

    def take_damage(self, amount):
            self.hp -= amount
            if self.hp <= 0:
                self.alive = False
                

