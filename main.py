import pygame
from sys import exit


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Fox Runner")
clock = pygame.time.Clock()


fonts = pygame.font.Font('font/Pixeltype.ttf', 30)


player1 = pygame.image.load('player/walk1.png').convert_alpha()
player1_rect = player1.get_rect(midbottom=(90, 300))
jump_img = pygame.image.load('player/jump.png').convert_alpha()
jump_rect = jump_img.get_rect(midbottom=(90, 300))


rock = pygame.image.load('images/rock.png').convert_alpha()
rock_rect = rock.get_rect(midbottom=(800, 300))


homescreen = pygame.image.load('images/home.png')
sky = pygame.image.load('images/sky.png').convert()
ground = pygame.image.load('images/ground2.png').convert()
logo = pygame.image.load('images/logo.png')
optiontxt = pygame.image.load('images/optionstext.png')


start = pygame.image.load('images/Start.png')
start_rect = start.get_rect(midbottom=(400, 280))
options = pygame.image.load('images/options.png')
options_rect = options.get_rect(midbottom=(400, 350))
back = pygame.image.load('images/back.png')
back_rect = back.get_rect(center = (80,40))


jumpsfx = pygame.mixer.Sound("aud/jump.wav")
clicksfx = pygame.mixer.Sound("aud/click.wav")

game_active = False
Home = True
optionscreen = False
startermisc = False
gamemisc = False


player_gravity = 0


start_time = 0
score = 0



def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surf = fonts.render(f'Score: {current_time//1000}', False, (0))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time // 1000

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player1_rect.bottom >= 300:
                player_gravity = -20
                if game_active:
                    jumpsfx.play()
            if event.key == pygame.K_BACKSPACE and not game_active:
                game_active = True
                Home = False
                start_time = pygame.time.get_ticks()
                rock_rect.left = 800
                pygame.mixer.music.stop()
                gamemisc = False

     
        if event.type == pygame.MOUSEBUTTONDOWN:
            if Home:
                optionscreen=False
                if start_rect.collidepoint(event.pos):
                    Home = False
                    game_active = True
                    gamemisc = False
                    start_time = pygame.time.get_ticks()
                    clicksfx.play()
                elif options_rect.collidepoint(event.pos):
                    optionscreen = True
                    Home = False
                    clicksfx.play()
            elif optionscreen:
                Home = False
                if back_rect.collidepoint(event.pos):
                    Home = True
                    clicksfx.play()

   
    if Home:
        screen.blit(homescreen, (0, 0))
        screen.blit(start, start_rect)
        screen.blit(options, options_rect)
        screen.blit(logo, (80, 0))

        if not startermisc:
            pygame.mixer.music.load('aud/01 - Opening.ogg')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            startermisc = True


    elif optionscreen:
        screen.blit(homescreen, (0, 0))
        screen.blit(back,back_rect)
        screen.blit(optiontxt, (200,150))




    elif game_active:
        if not gamemisc:
            pygame.mixer.music.load('aud/game.ogg')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            gamemisc = True

 
        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 300))

  
        screen.blit(rock, rock_rect)

    
        score = display_score()

       
        base_speed = 7.5
        speed_increase = (score // 10) * 1.5
        rock_speed = base_speed + speed_increase
        
        rock_rect.x -= rock_speed
        if rock_rect.right <= 0:
            rock_rect.left = 800

        
        player_gravity += 1
        player1_rect.y += player_gravity
        if player1_rect.bottom >= 300:
            player1_rect.bottom = 300

        
        if player1_rect.bottom < 250:
            screen.blit(jump_img, jump_rect)
        else:
            screen.blit(player1, player1_rect)

        
        if rock_rect.colliderect(player1_rect):
            game_active = False
            pygame.mixer.music.stop()

    
    else:
        screen.fill((0, 0, 0))
        rock_rect.x = 800
        player1_rect.bottom = 300


        msg = fonts.render('GAME OVER', False, (255, 255, 255))
        help = fonts.render('Press BACKSPACE to play', False, (255, 255, 255))
        score_message = fonts.render(f'Your Score was: {score}', False, (255, 225, 225))

        screen.blit(msg, msg.get_rect(center=(400, 100)))
        screen.blit(help, help.get_rect(center=(400, 130)))
        screen.blit(score_message, score_message.get_rect(center=(400, 330)))

    pygame.display.update()
    clock.tick(60)
