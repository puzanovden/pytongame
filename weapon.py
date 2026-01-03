class Weapon:
    def __init__(
        self,
        sprite,
        ammo_def,
        fire_rate,
        spread_mul=1.0,
        projectiles=1
    ):
        self.sprite = sprite
        self.ammo_def = ammo_def

        self.fire_rate = fire_rate
        self.cooldown = 1.0 / fire_rate

        self.projectiles = projectiles
        self.damage_mul = 1.0
        self.spread_mul = spread_mul
        self._timer = 0.0
        self.level = 1
    
    def update(self, dt):
        if self._timer > 0:
            self._timer -= dt
    
    def can_fire(self):
        return self._timer <= 0
    
    def trigger(self):
        self._timer = self.cooldown