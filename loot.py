from game_objects import *

class LootDef(GameObjectDef):
    def __init__(
        self,
        sprite,
        sprite_count,
        diameter,
        loot_type,
        value,
        lifetime=30.0
    ):
        super().__init__(
            ObjectType.LOOT,
            sprite,
            sprite_count,
            diameter,
            Team.NEUTRAL,
            overlap_limit=0.9
        )
        self.loot_type = loot_type
        self.value = value
        self.lifetime = lifetime

class Loot(GameObject):
    def __init__(self, loot_def, x, y):
        super().__init__(loot_def, x, y)
        self.timer = loot_def.lifetime

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.alive = False