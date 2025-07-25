import pygame
import math
from random import randint

WIDTH = 1080
HEIGHT = 720

class Obj(pygame.sprite.Sprite):
    def __init__(self, img):
        self.speedx=randint(-10,10)
        self.speedy=randint(-10,10)
        self.image = img  # Use the loaded image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)  # Create a mask for collision detection
        self.rect.topleft = (randint(50,WIDTH-50),randint(50,HEIGHT-50)) # Initial position
    def move(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speedx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speedy *= -1
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:   
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        return self.rect
    def collide(self,other):
        tmpx = self.speedx
        tmpy = self.speedy
        self.speedx = other.speedx
        self.speedy = other.speedy
        other.speedx = tmpx
        other.speedy = tmpy
        self.move()
        other.move()
    def update_prop(self, other):
        self.speedx = other.speedx
        self.speedy = other.speedy
        self.rect.topleft= other.rect.topleft

    
class Rock(Obj):
    def __init__(self):
        super().__init__(rock_img)

class Paper(Obj):
    def __init__(self):
        super().__init__(paper_img)

class Scissors(Obj):
    def __init__(self):
        super().__init__(scissors_img)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
rock_img = pygame.image.load('rock.png').convert_alpha()
rock_img = pygame.transform.scale(rock_img, (50, 50))
paper_img = pygame.image.load('paper.png').convert_alpha()
paper_img = pygame.transform.scale(paper_img, (30, 30))
scissors_img = pygame.image.load('scissors.png').convert_alpha()
scissors_img = pygame.transform.scale(scissors_img, (50, 50))
font = pygame.font.Font(None, 36)  # Create a font object (default font, size 36)
pygame.display.set_caption("Rock Paper Scissors Game")
clock = pygame.time.Clock()
running = True
num_each_objects = randint(5,30)  # Total number of objects
obj=[Rock() for _ in range(num_each_objects)]+[Paper() for _ in range(num_each_objects)]+[Scissors() for _ in range(num_each_objects)]


while running:
    clock.tick(60)
    screen.fill("white")
    

    # RENDER YOUR GAME HERE
    for o in obj:
        o.move()
        screen.blit(o.image, o.rect)

    for i in range(len(obj)):
        for j in range(i + 1, len(obj)):
            if pygame.sprite.collide_mask(obj[i], obj[j]):
                obj[i].collide(obj[j])
                # Handle collision logic here
                if isinstance(obj[i], Rock) and isinstance(obj[j], Scissors):
                    tmp_obj= obj[j] # Store the object to be replaced
                    obj[j]= Rock()  # Replace with a new Rock object
                    obj[j].update_prop(tmp_obj)  # Update the new Rock's properties
                elif isinstance(obj[i], Scissors) and isinstance(obj[j], Paper):
                    tmp_obj = obj[j]
                    obj[j] = Scissors()
                    obj[j].update_prop(tmp_obj)
                elif isinstance(obj[i], Paper) and isinstance(obj[j], Rock):
                    tmp_obj = obj[j]
                    obj[j] = Paper()
                    obj[j].update_prop(tmp_obj)
                elif isinstance(obj[i], Scissors) and isinstance(obj[j], Rock):
                    tmp_obj = obj[i]
                    obj[i] = Rock()
                    obj[i].update_prop(tmp_obj)
                elif isinstance(obj[i], Paper) and isinstance(obj[j], Scissors):
                    tmp_obj = obj[i]
                    obj[i] = Scissors()
                    obj[i].update_prop(tmp_obj)
                elif isinstance(obj[i], Rock) and isinstance(obj[j], Paper):
                    tmp_obj = obj[i]
                    obj[i] = Paper()
                    obj[i].update_prop(tmp_obj)

    # Count the number of each object
    num_rocks = sum(isinstance(o, Rock) for o in obj)
    num_papers = sum(isinstance(o, Paper) for o in obj)
    num_scissors = sum(isinstance(o, Scissors) for o in obj)

    # Draw a box for the count display
    pygame.draw.rect(screen, (200, 200, 200), (10, 10, 200, 100))  # Light gray box
    pygame.draw.rect(screen, (0, 0, 0), (10, 10, 200, 100), 2)  # Black border

    # Render the text for the counts
    rock_text = font.render(f"Rocks: {num_rocks}", True, (0, 0, 0))  # Black text
    paper_text = font.render(f"Papers: {num_papers}", True, (0, 0, 0))
    scissors_text = font.render(f"Scissors: {num_scissors}", True, (0, 0, 0))

    # Blit the text onto the screen
    screen.blit(rock_text, (20, 20))  # Position inside the box
    screen.blit(paper_text, (20, 50))
    screen.blit(scissors_text, (20, 80))
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()