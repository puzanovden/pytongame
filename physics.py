import math
from projectile import *
import random

BASE_SPREAD_ANGLE = 2.0 
CONTACT_COOLDOWN = 0.6

_objects = []


def set_objects(objects):
    global _objects
    _objects = objects




def _try_step(obj, dx, dy, dt):
    nx = obj.x + dx * obj.speed * dt
    ny = obj.y + dy * obj.speed * dt

    if can_move(obj, nx, ny):
        obj.x = nx
        obj.y = ny
        return True

    return False

def move(obj, dx, dy, dt):
    length = math.hypot(dx, dy)
    if length == 0:
        return

    dx /= length
    dy /= length

    if _try_step(obj, dx, dy, dt):
        return

    base = math.atan2(dy, dx)
    for a in (30, -30, 60, -60):
        ang = base + math.radians(a)
        ndx = math.cos(ang)
        ndy = math.sin(ang)

        if _try_step(obj, ndx, ndy, dt):
            return


def can_move(obj, nx, ny):
    r1 = obj.defn.diameter / 2

    for other in _objects:
        if other is obj or not other.alive:
            continue

        if other.defn.obj_type == ObjectType.PROJECTILE:
            continue

        r2 = other.defn.diameter / 2
        dist = math.hypot(nx - other.x, ny - other.y)

        allowed = (r1 + r2) * min(
            obj.defn.overlap_limit,
            other.defn.overlap_limit
        )

        if dist < allowed:
            return False

    return True


def shoot(shooter):
    weapon = shooter.weapon
    if weapon is None or not weapon.can_fire():
        return

    count = weapon.projectiles
    base_angle = shooter.angle

    if count == 1:
        angles = [0.0]
    else:
        step = BASE_SPREAD_ANGLE
        start = -step * (count - 1) / 2
        angles = [start + i * step for i in range(count)]

    angles = [a * weapon.spread_mul for a in angles]

    for a in angles:
        proj_def = weapon.ammo_def

        damage = int(weapon.ammo_def.damage * weapon.damage_mul)

        bullet = Projectile(
            weapon.ammo_def,
            shooter.x,
            shooter.y,
            base_angle + a,
            shooter.team,
            damage)


        _objects.append(bullet)
    weapon.trigger()

def check_projectile_hits():
    for obj in _objects:

        if not obj.alive:
            continue
        if obj.defn.obj_type != ObjectType.PROJECTILE:
            continue

        for other in _objects:
            if not other.alive:
                continue
            if other is obj:
                continue
            if other.team == obj.team:
                continue
            if other.defn.obj_type != ObjectType.CHARACTER:
                continue

            r1 = obj.defn.diameter / 2
            r2 = other.defn.diameter / 2
            dist = math.hypot(obj.x - other.x, obj.y - other.y)

            if dist <= r1 + r2:
                other.take_damage(obj.defn.damage)
                obj.alive = False
                break

def is_outside_screen(obj, w, h):
    return (
        obj.x < -100 or
        obj.y < -100 or
        obj.x > w + 100 or
        obj.y > h + 100
    )
def cleanup_outside():
    for obj in _objects:
        if obj.defn.obj_type == ObjectType.PROJECTILE:
            if is_outside_screen(obj, 1300, 800):
                obj.alive = False
                
def check_character_contacts():
    for obj in _objects:
        if not obj.alive:
            continue
        if obj.defn.obj_type != ObjectType.CHARACTER:
            continue
        if obj.team != Team.ENEMY:
            continue

        enemy = obj

        if enemy.contact_cd > 0:
            continue

        for other in _objects:
            if not other.alive:
                continue
            if other.defn.obj_type != ObjectType.CHARACTER:
                continue
            if other.team != Team.PLAYER:
                continue

            player = other

            dist = math.hypot(player.x - enemy.x, player.y - enemy.y)
            r = (player.defn.diameter + enemy.defn.diameter) / 2

            if dist <= r:
                dmg = random.randint(5, 15)
                player.take_damage(dmg)
                enemy.contact_cd = CONTACT_COOLDOWN
                break 

