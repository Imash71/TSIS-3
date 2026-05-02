import pygame
import random
pygame.init()
# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
# ---------------- GAME ----------------
state = "menu"
player_x = WIDTH // 2
player_y = HEIGHT - 120
speed = 6
cars = []
coins = []
score = 0
distance = 0
spawn_timer = 0

# ---------------- CAR (REAL LOOK) ----------------
def draw_car(x, y, color):
   # body
   pygame.draw.rect(screen, color, (x, y, 50, 90), border_radius=8)
   # windows
   pygame.draw.rect(screen, (40, 40, 40), (x + 10, y + 10, 30, 25))
   pygame.draw.rect(screen, (40, 40, 40), (x + 10, y + 40, 30, 25))
   # wheels
   pygame.draw.circle(screen, (0, 0, 0), (x + 5, y + 15), 6)
   pygame.draw.circle(screen, (0, 0, 0), (x + 45, y + 15), 6)
   pygame.draw.circle(screen, (0, 0, 0), (x + 5, y + 75), 6)
   pygame.draw.circle(screen, (0, 0, 0), (x + 45, y + 75), 6)

# ---------------- SPAWN ----------------
def spawn_car():
   x = random.randint(50, WIDTH - 80)
   cars.append([x, -100])

def spawn_coin():
   x = random.randint(50, WIDTH - 50)
   y = random.randint(-500, 0)
   coins.append([x, y])

def reset():
   global player_x, cars, coins, score, distance, state
   player_x = WIDTH // 2
   cars.clear()
   coins.clear()
   score = 0
   distance = 0
   state = "game"

# ---------------- LOOP ----------------
running = True
while running:
   clock.tick(60)
   # BLACK BACKGROUND
   screen.fill((0, 0, 0))
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False
       if event.type == pygame.KEYDOWN:
           if state == "menu":
               if event.key == pygame.K_SPACE:
                   reset()
           if state == "gameover":
               if event.key == pygame.K_r:
                   state = "menu"
   keys = pygame.key.get_pressed()
   # ---------------- MENU ----------------
   if state == "menu":
       screen.blit(font.render("TSIS3 RACER", True, (255, 255, 255)), (170, 250))
       screen.blit(font.render("SPACE - START", True, (200, 200, 200)), (170, 300))
   # ---------------- GAME ----------------
   elif state == "game":
       # controls
       if keys[pygame.K_LEFT] and player_x > 50:
           player_x -= speed
       if keys[pygame.K_RIGHT] and player_x < WIDTH - 80:
           player_x += speed
       spawn_timer += 1
       if spawn_timer % 35 == 0:
           spawn_car()
       if spawn_timer % 70 == 0:
           spawn_coin()
       # cars
       for car in cars:
           car[1] += 6
           draw_car(car[0], car[1], (255, 0, 0))
           # collision with car
           if (
               player_x < car[0] + 50 and
               player_x + 50 > car[0] and
               player_y < car[1] + 90 and
               player_y + 90 > car[1]
           ):
               state = "gameover"
       cars = [c for c in cars if c[1] < HEIGHT]
       # coins
       for coin in coins:
           coin[1] += 5
           pygame.draw.circle(screen, (255, 215, 0), (coin[0], coin[1]), 10)
           # collect coin
           if (
               player_x < coin[0] < player_x + 50 and
               player_y < coin[1] < player_y + 90
           ):
               score += 5
               coins.remove(coin)
       coins = [c for c in coins if c[1] < HEIGHT]
       # player car
       draw_car(player_x, player_y, (0, 255, 0))
       # score
       distance += 1
       score = distance // 10
       screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
   # ---------------- GAME OVER ----------------
   elif state == "gameover":
       screen.blit(font.render("GAME OVER", True, (255, 0, 0)), (170, 250))
       screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (190, 300))
       screen.blit(font.render("R - MENU", True, (255, 255, 255)), (200, 350))
   pygame.display.update()
pygame.quit()