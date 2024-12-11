import pygame
import random
import numpy as np
from sklearn.cluster import KMeans


def draw_text(screen, font, text, x, y, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def create_enemies(enemies, width, spawn_rate):
    for _ in range(spawn_rate):
        x = random.randint(0, width - 50)
        y = random.randint(50, 200)
        enemies.append([x, y])

def handle_player_movement(player_x, player_speed, width):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < width - 50:
        player_x += player_speed
    return player_x

def handle_player_shooting(player_x, player_y, shoot_timer, shoot_delay, bullets, shoot_sound):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and shoot_timer == 0:
        bullets.append([player_x + 20, player_y])
        shoot_sound.play()
        shoot_timer = shoot_delay
    shoot_timer = max(0, shoot_timer - 1)
    return shoot_timer, bullets

def move_bullets(bullets, bullet_speed, height):
    for bullet in bullets[:]:
        bullet[1] += bullet_speed
        if bullet[1] < 0 or bullet[1] > height:
            bullets.remove(bullet)

def handle_enemy_shooting(enemies, attack_rate, enemy_bullets):
    if random.randint(1, attack_rate) == 1 and enemies:
        enemy = random.choice(enemies)
        enemy_bullets.append([enemy[0] + 20, enemy[1] + 100])

def move_enemy_bullets(enemy_bullets, bullet_speed, player_x, player_y, health, height):
    for bullet in enemy_bullets[:]:
        bullet[1] += bullet_speed
        if bullet[1] > height:
            enemy_bullets.remove(bullet)
        if player_x < bullet[0] < player_x + 50 and player_y < bullet[1] < player_y + 50:
            enemy_bullets.remove(bullet)
            health -= 10
    return health

def check_bullet_enemy_collision(player_bullets, enemies, blood_splashes, score):
    for bullet in player_bullets[:]:
        for enemy in enemies[:]:
            if enemy[0] < bullet[0] < enemy[0] + 50 and enemy[1] < bullet[1] < enemy[1] + 100:
                enemies.remove(enemy)
                blood_splashes.append([enemy[0] + 25, enemy[1] + 50, 0])
                player_bullets.remove(bullet)
                score += 10
    return score

def apply_kmeans_clustering(enemies):
    enemy_positions = np.array([enemy[:2] for enemy in enemies])
    if len(enemy_positions) > 1:
        kmeans = KMeans(n_clusters=2)
        kmeans.fit(enemy_positions)
        return kmeans.labels_, kmeans.cluster_centers_
    return [], []

def update_blood_splashes(blood_splashes, screen, blood_splash_image):
    for splash in blood_splashes[:]:
        splash[2] += 1
        if splash[2] < 10:
            screen.blit(blood_splash_image, (splash[0], splash[1]))
        else:
            blood_splashes.remove(splash)

def draw_game_objects(screen, player_image, player_x, player_y, bullets, bullet_image, enemies, enemy_image, enemy_bullets):
    screen.blit(player_image, (player_x, player_y))
    for bullet in bullets:
        screen.blit(bullet_image, (bullet[0], bullet[1]))
    for enemy in enemies:
        screen.blit(enemy_image, (enemy[0], enemy[1]))
    for bullet in enemy_bullets:
        pygame.draw.rect(screen, (255, 0, 0), (bullet[0], bullet[1], 5, 10))
