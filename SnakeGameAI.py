import pygame
import random
import sys
import neat
pygame.font.init()

#running = True

class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [((WIN_WIDTH/2),(WIN_HEIGHT/2))]
        self.direction = random.choice([UP,DOWN,LEFT,RIGHT])
        self.color = (17,24,47)
        self.score = 0
        
    def get_head_pos(self): # getting the snake head position
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return 
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_pos()
        x,y = self.direction
        new = (((cur[0]+(x*GRIDSIZE))%WIN_WIDTH), (cur[1]+(y*GRIDSIZE))%WIN_HEIGHT)#((cur[0] + (x*GRIDSIZE)% WIN_WIDTH), (cur[1]+ (y*GRIDSIZE))%WIN_HEIGHT)
        #these if statements checking if snake tocuhed itself or not
        if len(self.positions) > 2 and new in self.positions[2:]:
            print("You Died") 
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()


    def reset(self): #reset method
        self.length = 1 #decreasing the snake to only the head
        self.positions = [((WIN_WIDTH/2),(WIN_HEIGHT/2))] # setting the snake start to the middle
        self.direction = random.choice([UP,DOWN,LEFT,RIGHT]) # randomly chosing a direction for the snake to start 
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0],p[1]),(GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface,(93,216,228), r ,1 ) # rgb is a light blue



    def handle_keys(self): # player controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #running = False
                print("Game Quit")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                #running = True
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)
    






#food class
class Food():
    def __init__(self):
        self.position = (0,0)
        self.color = (255,0,0) # color of food
        self.randomize_position() # randomizing pos

    def randomize_position(self): # function for randomizing pos
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRIDSIZE, random.randint(0, GRID_HEIGHT - 1)*GRIDSIZE)

    def draw(self, surface): # drawing the food
        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93,216,228), r ,1) # rgb value is light blue


#drawing grid
def drawGrid(surface):
    for y in range(0, int(WIN_HEIGHT)):
        for x in range(0, int(WIN_WIDTH)):
            if(x + y) % 2 == 0:
                r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE),(GRIDSIZE,GRIDSIZE))
                pygame.draw.rect(surface, (93, 216, 228), r)
            else:
                rr = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE),(GRIDSIZE,GRIDSIZE))
                pygame.draw.rect(surface, (84, 194, 205), rr)

#these two are in place instead of SCREEN_WIDTH & HEIGHT
WIN_WIDTH = 480
WIN_HEIGHT = 480 



GRIDSIZE = 30 # increase this value for bigger squares and decrease for smaller
GRID_WIDTH = WIN_HEIGHT / GRIDSIZE
GRID_HEIGHT = WIN_WIDTH/ GRIDSIZE

UP = (0,-1)
DOWN = (0, 1)
LEFT = (-1,0)
RIGHT = (1,0)

def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT),0,32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)


    snake = Snake()
    food = Food()

    font = pygame.font.SysFont("calibri", 16)
    while(True):
        clock.tick(10)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_pos() == -480:
            print("at -480")
            snake.reset()
        if snake.get_head_pos() == food.position:
            print("Nom Nom")
            snake.length += 1
            snake.score += 1
            food.randomize_position()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0,0))
        text = font.render("Score {0}".format(snake.score), 1, (0,0,0))
        screen.blit(text, (5,10))
        pygame.display.update()


main()


