import pygame
from game_utils import *
from game_settings import *

pygame.init()

# Set fullscreen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
pygame.display.set_caption("Assault Rifle Shooting Game")

clock = pygame.time.Clock()

# Initialize variables
player_x = WIDTH // 2
player_y = HEIGHT - 100
shoot_timer = 0
player_health = 100
score = 0
level = 1

# Initialize enemies
enemies = []
create_enemies(enemies, WIDTH, enemy_spawn_rate)

# Blood splash effect
blood_splashes = []

# Main game loop
running = True
while running:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement and shooting
    player_x = handle_player_movement(player_x, player_speed, WIDTH)
    shoot_timer, player_bullets = handle_player_shooting(
        player_x, player_y, shoot_timer, shoot_delay, player_bullets, shoot_sound
    )

    # Move player bullets
    move_bullets(player_bullets, bullet_speed, HEIGHT)

    # Enemy shooting
    handle_enemy_shooting(enemies, enemy_attack_rate, enemy_bullets)

    # Move enemy bullets
    player_health = move_enemy_bullets(
        enemy_bullets, enemy_bullet_speed, player_x, player_y, player_health, HEIGHT
    )

    # Bullet-enemy collision
    score = check_bullet_enemy_collision(
        player_bullets, enemies, blood_splashes, score
    )

    # KMeans clustering visualization
    cluster_labels, cluster_centers = apply_kmeans_clustering(enemies)
    for center in cluster_centers:
        pygame.draw.circle(screen, RED, (int(center[0]), int(center[1])), 10)

    # Blood splashes
    update_blood_splashes(blood_splashes, screen, blood_splash_image)

    # If all enemies are gone, go to next level
    if not enemies:
        level += 1
        enemy_spawn_rate += 1
        create_enemies(enemies, WIDTH, enemy_spawn_rate)

    # Draw player, bullets, and enemies
    draw_game_objects(
        screen,
        player_image,
        player_x,
        player_y,
        player_bullets,
        bullet_image,
        enemies,
        enemy_image,
        enemy_bullets,
    )

    # Display score, level, and health
    draw_text(screen, font, f"Score: {score}", 10, 10)
    draw_text(screen, font, f"Level: {level}", 10, 40)
    draw_text(screen, font, f"Health: {player_health}", 10, 70)

    # Game over condition
    if player_health <= 0:
        draw_text(screen, font, "GAME OVER", WIDTH // 2 - 100, HEIGHT // 2, RED)
        pygame.display.update()
        pygame.time.wait(2000)
        running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
