import pygame
import random
import os

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 640, 720
PLAYER_HEIGHT = 130
PLAYER_WIDTH = 130
BORDER = pygame.Rect(0, 0, WIDTH, HEIGHT)

ground_image = pygame.image.load(os.path.join('gmtk-assets', 'ground_image.png'))
SCORE_B = pygame.image.load(os.path.join('gmtk-assets', 'score_boarder.png'))
PLAYER = pygame.image.load(os.path.join('gmtk-assets', 'coin.png'))
PLAYER = pygame.transform.scale(PLAYER, (PLAYER_WIDTH, PLAYER_HEIGHT))
CAR = pygame.image.load(os.path.join('gmtk-assets', 'car.png'))
SCREEN_1 = pygame.image.load(os.path.join('gmtk-assets', 'Screen_1.png'))
SCREEN_2 = pygame.image.load(os.path.join('gmtk-assets', 'Screen_2.png'))
SCREEN_3 = pygame.image.load(os.path.join('gmtk-assets', 'Screen_3.png'))
SOUND_3 = pygame.mixer.Sound(os.path.join("gmtk-assets", "game_over.wav"))
SOUND_1 = pygame.mixer.Sound(os.path.join("gmtk-assets", "coin.wav"))
game_over_text = pygame.image.load(os.path.join('gmtk-assets', 'gameover.png'))
game_over_text = pygame.transform.scale(game_over_text, (384, 144))

restart = pygame.image.load(os.path.join('gmtk-assets', 'restart.png'))

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collection Quest")

ground_height = ground_image.get_height()

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((ground_image.get_width(), ground_height * 2))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.image.blit(ground_image, (0, 0))
        self.image.blit(ground_image, (0, ground_height))

    def update(self, vel):
        self.rect.y -= vel  # Control the scrolling speed
        if self.rect.y <= -ground_height:
            self.rect.y = 0

ground = Ground(0, 0)

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] == 1 and self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = (pygame.transform.scale(CAR, (117.5, 212.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.paused = False  # Added a paused flag

    def update(self, vel):
        if not self.paused:  # Only update the position if not paused
            self.rect.y += vel  # Control the car's vertical movement

            if self.rect.y >= HEIGHT:
                global SCORE  # Declare SCORE as a global variable
                SCORE -= 1  # Decrease the score by one when the car goes off the screen
                self.kill()  # Remove the car sprite if it goes beyond the window

def display_score():
    font = pygame.font.Font(os.path.join('gmtk-assets', 'font.ttf'), 55)
    text = font.render(str(SCORE), True, (0, 0, 0))
    WINDOW.blit(SCORE_B, (265, 85))
    WINDOW.blit(text, (300, 85))

button = Button(WIDTH // 2 - 57, HEIGHT // 2 - 35, restart)

player_x = 250
player_y = 250
gravity = 2
game_over = False
current_screen = 1  # Variable to keep track of the current screen

cars = pygame.sprite.Group()  # Group to store the car sprites

running = True
clock = pygame.time.Clock()

SCORE = 0

while running:
    clock.tick(80)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if current_screen == 1:
                current_screen = 2
            elif current_screen == 2:
                current_screen = 3
            elif current_screen == 3:
                current_screen = 4

    keys_pressed = pygame.key.get_pressed()

    if current_screen == 4:
        pygame.mixer.Sound.stop(SOUND_3)
        if not game_over:
            if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
                player_x -= 5  # Move the player position to the left

            if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
                player_x += 5  # Move the player position to the right

            if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
                player_y -= 7

            player_y += gravity  # Apply constant downward displacement to the player's vertical position

            # Check if the player has touched the ground and reset the vertical position
            if player_y >= HEIGHT - PLAYER_HEIGHT:
                game_over = True
                player_y = HEIGHT - PLAYER_HEIGHT

            # Check for collision with the border
            if player_x < BORDER.left:
                player_x = BORDER.left
                game_over = True
            elif player_x > BORDER.right - PLAYER_WIDTH:
                player_x = BORDER.right - PLAYER_WIDTH
                game_over = True
            if player_y < BORDER.top:
                player_y = BORDER.top
                game_over = True
            elif player_y > BORDER.bottom - PLAYER_HEIGHT:
                player_y = BORDER.bottom - PLAYER_HEIGHT
                game_over = True

        WINDOW.blit(ground_image, (0, 0))

        if not game_over:
            ground.update(2)  # Update the ground position with a scrolling speed of 2

        WINDOW.blit(ground.image, ground.rect)
        pygame.draw.rect(WINDOW, (255, 255, 255), BORDER, 1)  # Draw the border
        WINDOW.blit(PLAYER, (player_x, player_y))

        if game_over:
            WINDOW.blit(game_over_text, (120, 200))
            pygame.mixer.Sound.play(SOUND_3)
            button.draw(WINDOW)

            if button.is_clicked():
                game_over = False
                player_x = 250
                player_y = 250
                SCORE = 0
                gravity = 2

                cars.empty()  # Clear the cars group

        # Check for collision between player and cars
        if not game_over:
            player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
            for car in cars:
                if car.rect.colliderect(player_rect):
                    if car == cars.sprites()[0]:
                        SCORE += 1
                        pygame.mixer.Sound.play(SOUND_1)
                        pygame.mixer.music.stop()
                    car.kill()
                    break

        # Generate cars at random positions if game is not over
        if not game_over:
            if random.randint(1, 100) == 3:  # Adjust the number to control the car spawn rate
                x_positions = [25, 255, 475]
                x = random.choice(x_positions)
                y = random.randint(-PLAYER_HEIGHT, 0)
                car = Car(x, y)
                cars.add(car)

        if SCORE > 10:
            if random.randint(1, 65) == 3:
                x_positions = [25, 255, 475]
                x = random.choice(x_positions)
                y = random.randint(-PLAYER_HEIGHT, 0)
                car = Car(x, y)
                cars.add(car)
                ground.update(6)
                cars.update(8)
                gravity = 3
                if car.rect.y >= HEIGHT and SCORE > 10:
                    SCORE -= 2  # Deduct 2 points from the score

        if SCORE > 25:
            if random.randint(1, 45) == 3:
                x_positions = [25, 255, 475]
                x = random.choice(x_positions)
                y = random.randint(-PLAYER_HEIGHT, 0)
                car = Car(x, y)
                cars.add(car)
                ground.update(7)
                cars.update(12)
                gravity = 4
                if car.rect.y >= HEIGHT and SCORE > 10:
                    SCORE -= 3  # Deduct 3 points from the score

        if SCORE > 50:
            if random.randint(1, 20) == 3:
                x_positions = [25, 255, 475]
                x = random.choice(x_positions)
                y = random.randint(-PLAYER_HEIGHT, 0)
                car = Car(x, y)
                ground.update(7)
                cars.update(15)
                gravity = 4.5
                if car.rect.y >= HEIGHT and SCORE > 10:
                    SCORE -= 10  # Deduct 10 points from the score

                # Pause movement of cars
                if game_over:
                    for car in cars:
                        car.paused = True

        if SCORE < 0:
            game_over = True

        cars.update(4)  # Control the car's vertical movement speed
        cars.draw(WINDOW)  # Draw the car sprites

        display_score()
        pygame.display.update()

    elif current_screen == 3:
        WINDOW.blit(SCREEN_3, (0, 0))
        pygame.display.update()

    elif current_screen == 2:
        WINDOW.blit(SCREEN_2, (0, 0))
        pygame.display.update()

    else:
        WINDOW.blit(SCREEN_1, (0, 0))
        pygame.display.update()

pygame.quit()
