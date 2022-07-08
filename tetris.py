import pygame
import random
 
pygame.font.init()
 
screen_w = 800
screen_h = 700
game_w = 300  
game_h = 600  
block_dim = 30
 
tl_x = (screen_w - game_w) // 2
tl_y = screen_h - game_h
 
S = [[\'.....\',
      \'.....\',
      \'..00.\',
      \'.00..\',
      \'.....\'],
     [\'.....\',
      \'..0..\',
      \'..00.\',
      \'...0.\',
      \'.....\']]
 
Z = [[\'.....\',
      \'.....\',
      \'.00..\',
      \'..00.\',
      \'.....\'],
     [\'.....\',
      \'..0..\',
      \'.00..\',
      \'.0...\',
      \'.....\']]
 
I = [[\'..0..\',
      \'..0..\',
      \'..0..\',
      \'..0..\',
      \'.....\'],
     [\'.....\',
      \'0000.\',
      \'.....\',
      \'.....\',
      \'.....\']]
 
O = [[\'.....\',
      \'.....\',
      \'.00..\',
      \'.00..\',
      \'.....\']]
 
J = [[\'.....\',
      \'.0...\',
      \'.000.\',
      \'.....\',
      \'.....\'],
     [\'.....\',
      \'..00.\',
      \'..0..\',
      \'..0..\',
      \'.....\'],
     [\'.....\',
      \'.....\',
      \'.000.\',
      \'...0.\',
      \'.....\'],
     [\'.....\',
      \'..0..\',
      \'..0..\',
      \'.00..\',
      \'.....\']]
 
L = [[\'.....\',
      \'...0.\',
      \'.000.\',
      \'.....\',
      \'.....\'],
     [\'.....\',
      \'..0..\',
      \'..0..\',
      \'..00.\',
      \'.....\'],
     [\'.....\',
      \'.....\',
      \'.000.\',
      \'.0...\',
      \'.....\'],
     [\'.....\',
      \'.00..\',
      \'..0..\',
      \'..0..\',
      \'.....\']]
 
T = [[\'.....\',
      \'..0..\',
      \'.000.\',
      \'.....\',
      \'.....\'],
     [\'.....\',
      \'..0..\',
      \'..00.\',
      \'..0..\',
      \'.....\'],
     [\'.....\',
      \'.....\',
      \'.000.\',
      \'..0..\',
      \'.....\'],
     [\'.....\',
      \'..0..\',
      \'.00..\',
      \'..0..\',
      \'.....\']]
 
shapes = [S, Z, I, O, J, L, T]
colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

 
class Piece(object):
    rows = 20
    columns = 10
 
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.col[shapes.index(shape)]
        self.rotation = 0  
 
 
def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid
 
 
def convert_shape(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == \'0\':
                positions.append((shape.x + j, shape.y + i))
 
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
 
    return positions
 
def freespace(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape(shape)
 
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
 
    return True
 
def check(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False
 
def random_shape():
    global sha
    return Piece(5, 0, random.choice(shapes))
 
 
def text_sc(text, size, color, surface):
    font = pygame.font.SysFont(\'comicsans\', size, bold=True)
    label = font.render(text, 1, color)
 
    surface.blit(label, (t_l_x + game_w/2 - (label.get_width() / 2), tl_y + game_h/2 - label.get_height()/2))
 
def draw_grid(surface, row, col):
    sx = t_l_x
    sy = tl_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + game_w, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + game_h))  # vertical lines
 
 
def del_rows(grid, locked):
  
 
    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
 
 
def draw_next(shape, surface):
    font = pygame.font.SysFont(\'comicsans\', 30)
    label = font.render(\'Next Shape\', 1, (255,255,255))
 
    sx = t_l_x + game_w + 50
    sy = tl_y + game_h/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == \'0\':
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)
 
    surface.blit(label, (sx + 10, sy- 30))
 
 
def window_d(surface):
    surface.fill((0,0,0))
   
    font = pygame.font.SysFont(\'comicsans\', 60)
    label = font.render(\'TETRIS\', 1, (255,255,255))
 
    surface.blit(label, (t_l_x + game_w / 2 - (label.get_width() / 2), 30))
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (t_l_x + j* 30, tl_y + i * 30, 30, 30), 0)
 
   
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (t_l_x, tl_y, game_w, game_h), 5)
    
def main():
    global grid
 
    locked_positions = {}
    grid = create_grid(locked_positions)
 
    change_piece = False
    run = True
    current = random_shape()
    next_piece = random_shape()
    clock = pygame.time.Clock()
    time = 0
 
    while run:
        speed = 0.27
 
        grid = create_grid(locked_positions)
        time += clock.get_rawtime()
        clock.tick()
 
        
        if time/1000 >= speed:
            time = 0
            current.y += 1
            if not (freespace(current, grid)) and current.y > 0:
                current.y -= 1
                change_piece = True
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current.x -= 1
                    if not freespace(current, grid):
                        current.x += 1
 
                elif event.key == pygame.K_RIGHT:
                    current.x += 1
                    if not freespace(current, grid):
                        current.x -= 1
                elif event.key == pygame.K_UP:
                   
                    current.rotation = current.rotation + 1 % len(current.shape)
                    if not freespace(current, grid):
                        current.rotation = current.rotation - 1 % len(current.shape)
 
                if event.key == pygame.K_DOWN:
                    
                    current.y += 1
                    if not freespace(current, grid):
                        current.y -= 1
 
                
                   while freespace(current, grid):
                       current.y += 1
                   current.y -= 1
                   print(convert_shape(current))\'\'\'  
 
        shape_pos = convert_shape(current)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current.color
 
       
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current.color
            current = next_piece
            next_piece = random_shape()
            change_piece = False
 
          
            del_rows(grid, locked_positions)
 
        draw_next(next_piece, win)
        pygame.display.update()
 
        if check(locked_positions):
            run = False
 
    text_sc("You Lost", 40, (255,255,255), win)
    pygame.display.update()
    pygame.time.delay(2000)
 
 
def main_menu():
    run = True
    while run:
        win.fill((0,0,0))
        text_sc(\'Press space key to begin.\', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
 
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()
 
 
win = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption(\'Tetris python\')
 
main_menu()