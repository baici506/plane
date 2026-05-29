import pygame
import sys
import random

pygame.init()

try:
    player_image = pygame.image.load("plane.png")
    player_image = pygame.transform.scale(player_image, (60, 60))
    use_image = True
except:
    use_image = False
    print("没有找到 plane.png，继续使用红色方块")

try:
    heart_image = pygame.image.load("heart.png")
    heart_image = pygame.transform.scale(heart_image, (30, 30))
    use_heart = True
except:
    use_heart = False
    print("没有找到 heart.png，继续使用文字显示血量")

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("plane")

WHITE = (255, 255, 255)
RED = (255, 0, 0)

player_width = 40
player_height = 40
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 80
player_speed = 5

bullet_width = 8
bullet_height = 12
bullet_speed = 5
bullets = []
spawn_delay = 30
spawn_counter = 0

hp = 3
invincible_frames = 0

start_ticks = pygame.time.get_ticks()
game_duration = 30000
game_state = "playing"

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if game_state == "playing":
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < HEIGHT - player_height:
            player_y += player_speed

        spawn_counter += 1
        if spawn_counter >= spawn_delay:
            spawn_counter = 0
            bullet_x = random.randint(0, WIDTH - bullet_width)
            bullet_y = 0
            bullets.append([bullet_x, bullet_y])

        for bullet in bullets[:]:
            bullet[1] += bullet_speed
            if bullet[1] > HEIGHT:
                bullets.remove(bullet)

        for bullet in bullets[:]:
            if (player_x < bullet[0] + bullet_width and
                    player_x + player_width > bullet[0] and
                    player_y < bullet[1] + bullet_height and
                    player_y + player_height > bullet[1]):
                if invincible_frames <= 0:
                    hp -= 1
                    invincible_frames = 45
                bullets.remove(bullet)

        if invincible_frames > 0:
            invincible_frames -= 1

        elapsed_time = pygame.time.get_ticks() - start_ticks
        remaining_time = max(0, game_duration - elapsed_time)

        if remaining_time <= 0:
            game_state = "win"
        if hp <= 0:
            game_state = "lose"

    screen.fill(WHITE)

    for bullet in bullets:
        pygame.draw.rect(screen, RED, (bullet[0], bullet[1], bullet_width, bullet_height))

    if game_state == "playing" and invincible_frames > 0 and (invincible_frames // 5) % 2 == 0:
        pass
    else:
        if use_image:
            screen.blit(player_image, (player_x, player_y))
        else:
            pygame.draw.rect(screen, RED, (player_x, player_y, player_width, player_height))

    if use_heart:
        for i in range(hp):
            screen.blit(heart_image, (10 + i * 35, 10))
    else:
        font = pygame.font.Font(None, 36)
        hp_text = font.render(f"HP: {hp}", True, (0, 0, 0))
        screen.blit(hp_text, (10, 10))

    font = pygame.font.Font(None, 36)
    if game_state == "playing":
        timer_text = font.render(f"Time: {remaining_time // 1000}s", True, (0, 0, 0))
        screen.blit(timer_text, (WIDTH - 120, 10))
    elif game_state == "win":
        win_text = font.render("YOU WIN! Press R to restart", True, (0, 255, 0))
        screen.blit(win_text, (WIDTH // 2 - 150, HEIGHT // 2))
    elif game_state == "lose":
        lose_text = font.render("YOU LOSE! Press R to restart", True, (255, 0, 0))
        screen.blit(lose_text, (WIDTH // 2 - 150, HEIGHT // 2))

    if keys[pygame.K_r] and game_state != "playing":
        hp = 3
        bullets.clear()
        player_x = WIDTH // 2 - player_width // 2
        player_y = HEIGHT - 80
        start_ticks = pygame.time.get_ticks()
        game_state = "playing"
        invincible_frames = 0
        spawn_counter = 0

    pygame.display.flip()
    clock.tick(60)