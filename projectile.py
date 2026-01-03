from game_objects import *

class ProjectileDef(GameObjectDef):
    def __init__(
        self,
        sprite,
        sprite_count,
        diameter,
        speed,
        damage,
        nd = False
    ):
        super().__init__(
            ObjectType.PROJECTILE,
            sprite,
            sprite_count,
            diameter
        )
        self.speed = speed
        self.damage = damage
        self.nd = nd


class Projectile(GameObject):
    def __init__(self, proj_def, x, y, angle, team, damage):
        super().__init__(proj_def, x, y, angle, team)
        self.damage = damage

    def update(self, dt):
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.defn.speed * dt
        self.y -= math.sin(rad) * self.defn.speed * dt