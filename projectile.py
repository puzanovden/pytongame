from game_objects import *

class ProjectileDef(GameObjectDef):
    def __init__(
        self,
        sprite,
        sprite_count,
        diameter,
        speed,
        damage
    ):
        super().__init__(
            ObjectType.PROJECTILE,
            sprite,
            sprite_count,
            diameter
        )
        self.speed = speed
        self.damage = damage


class Projectile(GameObject):
    def __init__(self, proj_def: ProjectileDef, x, y, angle, team):
        super().__init__(proj_def, x, y, angle, team)

    def update(self, dt):
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.defn.speed * dt
        self.y -= math.sin(rad) * self.defn.speed * dt