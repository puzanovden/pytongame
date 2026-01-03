from character import *
from weapon import *
from loot import *
from projectile import *
import random
import physics
import highscores

game_over = False
score = 0


SCREEN_W = 1300
SCREEN_H = 750

heal_small  = None
heal_mid    = None
heal_big    = None
buff_proj  = None
buff_dmg   = None
buff_rate  = None

player = None




def init_world():

    global player
    global heal_small,heal_mid,heal_big,buff_proj,buff_dmg,buff_rate
    

    player_sprite = pygame.image.load("images/player.png").convert_alpha()
    enemy_sprite  = pygame.image.load("images/enem1.png").convert_alpha()
    pistol_sprite  = pygame.image.load("images/weap1.png").convert_alpha()
    shotgun_sprite  = pygame.image.load("images/weap2.png").convert_alpha()
    automat_sprite  = pygame.image.load("images/weap3.png").convert_alpha()
    loot_sprite   = pygame.image.load("images/55.png").convert_alpha()
    bullet_sprite   = pygame.image.load("images/555.png").convert_alpha()
    heal_sprite   = pygame.image.load("images/heal_sprite.png").convert_alpha()


    heal_small = LootDef(heal_sprite,1, 20, "heal", 15)
    heal_mid    = LootDef(heal_sprite,1, 30, "heal", 40)
    heal_big    = LootDef(heal_sprite,1, 45, "heal", 100)

    buff_proj  = LootDef(pygame.image.load("images/pp.png").convert_alpha(), 1, 50, "buff_projectiles", 1)
    buff_dmg   = LootDef(pygame.image.load("images/pd.png").convert_alpha(), 1, 50, "buff_damage", 0.05)
    buff_rate  = LootDef(pygame.image.load("images/pr.png").convert_alpha(), 1, 50, "buff_fire_rate", 0.05)

    player_def = CharacterDef(player_sprite, 1, 40, hp_max=100, speed=300, default_team=Team.PLAYER)
    enemy_def  = CharacterDef(enemy_sprite, 1, 40, hp_max=50,  speed=200, default_team=Team.ENEMY)
    loot_def   = LootDef(loot_sprite,   1, 30, loot_type="medkit", value=25)

    pisbullet_def = ProjectileDef(sprite=bullet_sprite,sprite_count=1,diameter=10,speed=700,damage=35)
    pistol = Weapon(sprite=pistol_sprite,ammo_def=pisbullet_def,fire_rate=7,spread_mul=1.0)

    shobullet_def = ProjectileDef(sprite=bullet_sprite,sprite_count=1,diameter=8,speed=600,damage=25)
    shotgun = Weapon(sprite=shotgun_sprite,ammo_def=shobullet_def,fire_rate=5,spread_mul=2.7,projectiles=3)

    autbullet_def = ProjectileDef(sprite=bullet_sprite,sprite_count=1,diameter=8,speed=800,damage=8)
    automat = Weapon(sprite=automat_sprite,ammo_def=autbullet_def,fire_rate=25,spread_mul=2.7,projectiles=1)

    player = Character(
        player_def,
        600, 400,
        is_player=True,
        weapons=[pistol,shotgun,automat]
        )

    physics.set_objects([
        player,
        Character(enemy_def,  300, 300),
        Character(enemy_def,  900, 300),
        Loot(loot_def, 500, 500),
        Loot(loot_def, 700, 500)])

def update_objects(dt):
    for obj in physics._objects:
        if isinstance(obj, Character):
            obj.update(dt, player)
        else:
            obj.update(dt)


def spawn_enemy():
    side = random.choice([(random.randint(0, SCREEN_W), -40),
                        (random.randint(0, SCREEN_W), SCREEN_H + 40),
                        (-40, random.randint(0, SCREEN_H)),
                        (SCREEN_W + 40, random.randint(0, SCREEN_H))])
    x, y = side

    hp = random.randint(50, 250)
    k = (hp - 50) / 150
    diameter = int(30 + 40 * k)
    speed = int(220 - 140 * k)

    enemy_sprite  = pygame.image.load("images/enem1.png").convert_alpha()

    enemy = Character(CharacterDef(enemy_sprite, 1, diameter, hp, speed, Team.ENEMY), x, y)
    physics._objects.append(enemy)

def draw_weapon_bar(surface):

    weapons = player.weapons
    if not weapons:
        return

    icon_size = 75
    icon_sizex = 150
    spacing = 10
    y = 10

    total_w = len(weapons) * icon_sizex + (len(weapons) - 1) * spacing
    start_x = (surface.get_width() - total_w) // 2

    for i, weapon in enumerate(weapons):
        x = start_x + i * (icon_sizex + spacing)

        icon = pygame.transform.scale(weapon.sprite, (icon_sizex, icon_size))
        surface.blit(icon, (x, y))

        if i == player.active_weapon:
            pygame.draw.rect(
                surface,
                (255, 255, 0),            
                (x - 2, y - 2, icon_sizex + 4, icon_size + 4),
                2
            )

def check_loot_pickup():
    if not player:
        return

    for obj in physics._objects:
        if not obj.alive or obj.defn.obj_type != ObjectType.LOOT:
            continue

        dist = math.hypot(obj.x - player.x, obj.y - player.y)
        if dist <= (obj.defn.diameter + player.defn.diameter) / 2:
            apply_loot(player, obj)
            obj.alive = False

def apply_loot(player, loot):
    weapon = player.weapon

    if loot.defn.loot_type == "heal":
        player.hp = min(
            player.hp + loot.defn.value,
            player.defn.hp_max
        )
        return  

    if loot.defn.loot_type == "buff_projectiles":
        weapon.projectiles += 1

    elif loot.defn.loot_type == "buff_damage":
        weapon.damage_mul += loot.defn.value

    elif loot.defn.loot_type == "buff_fire_rate":
        weapon.fire_rate += loot.defn.value
        weapon.cooldown = 1.0 / weapon.fire_rate

    weapon.level += 1

def delete_dead():
    global game_over, score

    for obj in physics._objects:
        if not obj.alive:
            if obj.defn.obj_type == ObjectType.CHARACTER:
                if obj.team == Team.ENEMY:
                    score += int(obj.hp_max * 0.5 + obj.speed * 0.3)
                    drop_loot(obj)
                elif obj.team == Team.PLAYER:
                    game_over = True
                    #if not score == 0: highscores.start_name_input()
                    highscores.start_name_input()
    physics._objects[:] = [o for o in physics._objects if o.alive]

def drop_loot(enemy):
    hp = enemy.defn.hp_max

    drop_chance = min(0 + hp / 500, 0.3)
    if random.random() > drop_chance:
        return

    rn = random.random()

    if rn < 0.02:
        loot_def = buff_proj         
    elif rn < 0.06:#0.06
        loot_def = buff_dmg          
    elif rn < 0.11:
        loot_def = buff_rate         
    else:
        if hp < 100:
            loot_def = heal_small
        elif hp < 250:
            loot_def = heal_mid
        else:
            loot_def = heal_big

    physics._objects.append(Loot(loot_def, enemy.x, enemy.y))

def draw_hp_bar(screen, player):
    if not player:
        return

    bar_w = 300
    bar_h = 20
    x = (screen.get_width() - bar_w) // 2
    y = screen.get_height() - bar_h - 10

    hp_frac = max(player.hp / player.defn.hp_max, 0)

    pygame.draw.rect(screen, (60, 60, 60), (x, y, bar_w, bar_h))
    pygame.draw.rect(
        screen,
        (200, 40, 40),
        (x, y, int(bar_w * hp_frac), bar_h)
    )

def draw_score(screen):
    _font = pygame.font.SysFont("consolas", 28, bold=True)
    text = _font.render(f"SCORE: {score}", True, (240, 240, 240))
    screen.blit(text, (20, 20))

def draw_game_over(screen, print = True):
    w, h = screen.get_size()

    overlay = pygame.Surface((w, h))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    if print:
        _font = pygame.font.SysFont("consolas", 28, bold=True)
        _font_big = pygame.font.SysFont("consolas", 56, bold=True)
        title = _font_big.render("YOU DIED", True, (220, 60, 60))
        score_text = _font.render(f"YOUR SCORE: {score}", True, (230, 230, 230))
        screen.blit(title, title.get_rect(center=(w//2, h//2 - 40)))
        screen.blit(score_text, score_text.get_rect(center=(w//2, h//2 + 10)))

def restart_game():
    global game_over
    game_over = False
    init_world()