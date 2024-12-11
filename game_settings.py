import pygame

pygame.mixer.init()

pygame.font.init()
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player attributes
player_speed = 5
shoot_delay = 10
# Bullet attributes
player_bullets = []
bullet_speed = -10
enemy_bullets = []
enemy_bullet_speed = 5

# Enemy attributes
enemy_spawn_rate = 5
enemy_attack_rate = 50

# Load resources
shoot_sound = pygame.mixer.Sound("shoot.wav")
player_image = pygame.image.load("player.jpg")
enemy_image = pygame.image.load("enemy2.jpg")
background_image = pygame.image.load("bg.jpg")
bullet_image = pygame.image.load("bullet.png")
blood_splash_image = pygame.image.load("blood_splash.png")

# Resize images
player_image = pygame.transform.scale(player_image, (50, 50))
enemy_image = pygame.transform.scale(enemy_image, (50, 100))
bullet_image = pygame.transform.scale(bullet_image, (10, 10))
background_image = pygame.transform.scale(background_image, (1920, 1080))  # Default full HD
blood_splash_image = pygame.transform.scale(blood_splash_image, (40, 40))

# Font
font = pygame.font.Font(None, 36)
