import pygame

pygame.font.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("soldiers")
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE= (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BULLET_COLOR = (255, 0, 0)

HEALTH_FONT = pygame.font.SysFont("Comicsans",50)
WINNER_FONT = pygame.font.SysFont("Comicsans",100)

FPS = 120
VELOCITY = 1

BULLET_VELOCITY = 4
MAX_BULLET = 10
SOLDIER_WIDTH = 30
SOLDIER_HEIGHT = 60

soldier_1_image = pygame.image.load("images/soldier_1.png")
soldier_1_image = pygame.transform.scale(soldier_1_image,(SOLDIER_WIDTH,SOLDIER_HEIGHT))
soldier_1 = pygame.transform.rotate(soldier_1_image,360)

soldier_2_image = pygame.image.load("images/soldier_2.png")
soldier_2_image = pygame.transform.scale(soldier_2_image,(SOLDIER_WIDTH,SOLDIER_HEIGHT))
soldier_2 = pygame.transform.rotate(soldier_2_image,360)

warzone_image = pygame.image.load("images/warzone.jpg")
warzone = pygame.transform.scale(warzone_image,(WIDTH,HEIGHT))

screen.fill(WHITE)

one_hit = pygame.USEREVENT + 1
two_hit = pygame.USEREVENT + 2

def draw_window(one,two,one_bullets,two_bullets,one_health,two_health):
    screen.blit(warzone,(0,0))
    two_health_text = HEALTH_FONT.render("health:"+str(two_health),1,WHITE)
    one_health_text = HEALTH_FONT.render("Health:"+str(one_health),1,WHITE)
    screen.blit(soldier_1,(one.x,one.y))
    screen.blit(soldier_2,(two.x,two.y))

    for bullet in one_bullets:
        pygame.draw.rect(screen,BULLET_COLOR,bullet)
    
    for bullet in two_bullets:
        pygame.draw.rect(screen,BULLET_COLOR,bullet)
    pygame.display.update()

#one wasd 

def one_movement(keys_pressed,soldier_1):
    if keys_pressed[pygame.K_w] and soldier_1.y - VELOCITY > 0:
        soldier_1.y -= VELOCITY
    if keys_pressed[pygame.K_a] and soldier_1.x - VELOCITY > 0:
        soldier_1.x -= VELOCITY
    if keys_pressed[pygame.K_s] and soldier_1.y + VELOCITY + soldier_1.height < HEIGHT-15:
        soldier_1.y += VELOCITY
    if keys_pressed[pygame.K_s] and soldier_1.y + VELOCITY + soldier_1.height < HEIGHT-15:
        soldier_1.y += VELOCITY

def two_movement(keys_pressed,soldier_2):
    if keys_pressed[pygame.K_LEFT] and soldier_2.x - VELOCITY > 0:
        soldier_2.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and soldier_2.x + VELOCITY + soldier_2.width < WIDTH:
        soldier_2.x += VELOCITY
    if keys_pressed[pygame.K_UP] and soldier_2.y - VELOCITY > 0:
        soldier_2.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and soldier_2.y + VELOCITY + soldier_2.height < HEIGHT-15:
        soldier_2.y += VELOCITY

def handle_bullets(one_bullets,two_bullets,one,two):
    for bullet in one_bullets:
        bullet.x -= BULLET_VELOCITY
        if two.colliderect(bullet):
            pygame.event.post(pygame.event.Event(two_hit))
            one_bullets.remove(bullet)
        elif bullet.x > WIDTH :
            one_bullets.remove(bullet)
    
    for bullet in two_bullets:
        bullet.x += BULLET_VELOCITY
        if one.colliderect(bullet):
            pygame.event.post(pygame.event.Event(one_hit))
            two_bullets.remove(bullet)
        elif bullet.x < 0 :
            two_bullets.remove(bullet)

def draw_winner(winner_text):
    winner_text = WINNER_FONT.render(winner_text,1,WHITE)
    screen.blit(winner_text,(WIDTH//2 - winner_text.get_width()//2,HEIGHT//2 - winner_text.get_height()//2 ))
    pygame.display.update()
    pygame.time.delay(5000)



def main():
    one = pygame.Rect(700,300,SOLDIER_WIDTH,SOLDIER_HEIGHT)
    two = pygame.Rect(100,300,SOLDIER_WIDTH,SOLDIER_HEIGHT)

    one_bullet = []
    two_bullet = []

    one_health = 10
    two_health = 10

    is_running  = True

    while is_running :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and  len(one_bullet ) < MAX_BULLET:
                    bullet = pygame.Rect(one.x + SOLDIER_WIDTH,one.y + SOLDIER_HEIGHT//2,10,5)
                    one_bullet.append(bullet) 
                if event.key == pygame.K_RCTRL and len(two_bullet) < MAX_BULLET:
                    bullet = pygame.Rect(two.x,two.y + SOLDIER_HEIGHT//2,10,5)
                    two_bullet.append(bullet)     

            if event.type == one_hit:
                two_health -=  1
            if event.type == two_hit:
                one_health -= 1
            
        winner_text = ""
        if two_health <= 0:
            winner_text = "soldier_1 wins"
        if one_health <= 0:
            winner_text = "soldier_2_wins"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()

        one_movement(keys_pressed,one)
        two_movement(keys_pressed,two)
        handle_bullets(one_bullet,two_bullet,one,two)
        draw_window(two,one,two_bullet,one_bullet,two_health,one_health)
        
main()


