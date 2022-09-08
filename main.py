import pygame
import random
import pygame.freetype


def moving_player():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT


def restart_ball(sx, sy):
    ball.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
    sx = random.choice((random.randint(-max_speed_ball, -min_speed_ball), random.randint(min_speed_ball, max_speed_ball)))
    sy = random.choice((random.randint(-max_speed_ball, -min_speed_ball), random.randint(min_speed_ball, max_speed_ball)))
    return sx, sy


def change_ball_speed(sx,sy):
    if sx < 0:
        sx -= 1
    else:
        sx += 1
    if sy < 0:
        sy -= 1
    else:
        sy += 1
    return sx, sy

def move_ball(sx, sy, cc):
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        sy = - sy
    if ball.colliderect(player) and sx < 0:
        cc += 1
        pong_sound.play()
        if abs(ball.left - player.right) < 10:
            sx = -sx
        elif abs(ball.top - player.bottom) < 10 and sy < 0:
            sy = -sy
        elif abs(player.top - ball.bottom) < 10 and sy > 0:
            sy = -sy
    if ball.colliderect(bot) and sx > 0:
        cc += 1
        pong_sound.play()
        if abs(ball.right - bot.left) < 10:
            sx = -sx
        elif abs(ball.top - bot.bottom) < 10 and sy < 0:
            sy = -sy
        elif abs(bot.top - ball.bottom) < 10 and sy > 0:
            sy = -sy
    now = pygame.time.get_ticks()
    if now - score_time > pause_len and not game_over:
        ball.x += sx
        ball.y += sy
    return sx, sy, cc


def move_bot():
    if ball.centerx > SCREEN_WIDTH / 2 and ball_sx > 0:
        if bot.bottom < ball.top:
            bot.y += bot_speed
        elif bot.top > ball.bottom:
            bot.y -= bot_speed


def exit():
    if player_score == 10 or bot_score == 10:
        quit()


def play_sound():
    if player_score == score_finish:
        win_sound.play()
    elif bot_score == score_finish:
        lose_sound.play()
    else:
        score_sound.play()


SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500
BG_COLOR = (0,0,0)
PLAYER_COLOR = (230,107,13)
BALL_COLOR = (160,234,242)
FONT_COLOR = (255,255,255)

player = pygame.Rect(10,SCREEN_HEIGHT / 2,10,100)
bot = pygame.Rect(SCREEN_WIDTH - 20,SCREEN_HEIGHT / 2, 10,100)
ball = pygame.Rect(SCREEN_WIDTH / 2,SCREEN_HEIGHT / 2, 20, 20)

end_text = None
restart_text = 'press tab to restart'
game_over = False

player_speed = 0
bot_speed = 7
ball_sx = -7
ball_sy = 7
min_speed_ball = 3
max_speed_ball = 11

collide_count = 0

score_time = 0
pause_len = 1000
score_finish = 2

player_score,bot_score = 0,0

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ping pong')

pong_sound = pygame.mixer.Sound('pong.wav')
lose_sound = pygame.mixer.Sound('lose.wav')
win_sound = pygame.mixer.Sound('win.wav')
score_sound = pygame.mixer.Sound('score.wav')

main_font = pygame.freetype.Font(None, 42)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                game_over = False
                player_score, bot_score = 0,0
            if event.key == pygame.K_w:
                player_speed -= 7
            elif event.key == pygame.K_s:
                player_speed += 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player_speed += 7
            elif event.key == pygame.K_s:
                player_speed -= 7

    moving_player()
    move_bot()
    ball_sx, ball_sy, collide_count = move_ball(ball_sx, ball_sy, collide_count)
    if collide_count == 6:
        ball_sx, ball_sy = change_ball_speed(ball_sx, ball_sy)
        collide_count = 0
    #exit()

    if ball.right <= 0:
        bot_score += 1
        if bot_score == score_finish:
            game_over = True
            end_text = 'You lose'
    elif ball.left >= SCREEN_WIDTH:
        player_score +=1
        if player_score == score_finish:
            end_text = 'You WIN!'
            game_over = True

    if ball.right <= 0 or ball.left >= SCREEN_WIDTH:
        play_sound()
        ball_sx, ball_sy = restart_ball( ball_sx, ball_sy)
        collide_count = 0
        score_time = pygame.time.get_ticks()

    screen.fill(BG_COLOR)
    main_font.render_to(screen, (SCREEN_WIDTH / 3, 20), str(player_score), FONT_COLOR)
    main_font.render_to(screen, (SCREEN_WIDTH / 1.5, 20), str(bot_score), FONT_COLOR)
    pygame.draw.rect(screen,PLAYER_COLOR,player)
    pygame.draw.rect(screen,PLAYER_COLOR,bot)
    pygame.draw.ellipse(screen,BALL_COLOR,ball)

    if game_over:
        main_font.render_to(screen, (SCREEN_WIDTH / 2.6, 100), end_text, FONT_COLOR)
        main_font.render_to(screen, (SCREEN_WIDTH / 3.2, 150), restart_text, FONT_COLOR)
    print(ball_sx, ball_sy)

    clock.tick(60)
    pygame.display.flip()
