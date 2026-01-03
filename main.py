
import pygame
import physics
import gameplay
import highscores

pygame.init()
screen = pygame.display.set_mode((gameplay.SCREEN_W, gameplay.SCREEN_H))
clock = pygame.time.Clock()

gameplay.init_world()
highscores.init_ui()

background = pygame.image.load("images/55.png").convert()

spawn_timer = 0.0
spawn_interval = 0.75

running = True
while running:
    dt = clock.tick(60) / 1500

    spawn_timer += dt

    if spawn_timer >= spawn_interval:
        spawn_timer = 0.0
        gameplay.spawn_enemy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif gameplay.game_over:
            if highscores.entering_name:
                highscores.handle_event(event, gameplay.score)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                gameplay.restart_game()


    gameplay.update_objects(dt)
    physics.check_projectile_hits()
    physics.check_character_contacts()
    gameplay.delete_dead()
    gameplay.check_loot_pickup()

    #objects = [o for o in physics._objects if o.alive]

    screen.blit(background, (0, 0))  

    for obj in physics._objects:               
        obj.draw(screen)

    gameplay.draw_score(screen)
    gameplay.draw_weapon_bar(screen)
    gameplay.draw_hp_bar(screen, gameplay.player)

    if gameplay.game_over:
        gameplay.draw_game_over(screen,highscores.entering_name)
        if highscores.entering_name:
            highscores.draw_name_input(screen)
        else:
            highscores.draw_highscores(screen) 

    pygame.display.flip()  

pygame.quit()


