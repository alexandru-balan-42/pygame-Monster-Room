import pygame
from random import randint


class GameCharacter:
    def __init__(self, x: int, y: int, image):
        self.x = x
        self.y = y
        self.image = image

# returns a list containing 2 lists that have the lowest and highest values of x and y of the image used for the character    
    def all_pixels(self):
        return [[self.x, self.x + self.image.get_width()], [self.y, self.y + self.image.get_height()]]  

class Player(GameCharacter):
    def __init__(self, x: int, y: int, image):
        super().__init__(x, y, image)
        self.speed = 4              


class Monster(GameCharacter):
    def __init__(self, x: int, y: int, image, origin: str):
        super().__init__(x, y, image)
        self.origin = origin
                 

class Coin(GameCharacter):
    def __init__(self, x: int, y: int, image):
        super().__init__(x, y, image)

# the change methods change the x and y coord of the coin with a random value except the outermost part of the screen 
    def change_coordinates(self):
        self.x = randint(40, 760 - self.image.get_width() - 40)                                           
        self.y = randint(40, 600 - self.image.get_height() - 40)             


class Hunter(GameCharacter):
    def __init__(self, x: int, y: int, image):
        super().__init__(x, y, image)
        self.speed = 1

# moves the hunter towards the location of the player
    def move(self, player_x: int, player_y: int):
        if player_x > self.x:
            self.x += self.speed
        if player_x < self.x:
            self.x -= self.speed
        if player_y > self.y:
            self.y += self.speed
        if player_y < self.y:
            self.y -= self.speed               


class GameOverMenu:
    def __init__(self, font: str, size: int):
        self.font = font
        self.size = size

# the methods return the rendering of the text used in the game over screen    
    def title(self):
        game_over_font = pygame.font.SysFont(self.font, self.size) 
        return game_over_font.render("Game over", True, (255, 0, 0))
    
    def new_game_text(self):
        new_game_font = pygame.font.SysFont(self.font, self.size // 2)
        return new_game_font.render('Press "n" for new game', True, (255, 0, 0))
    
    def exit_text(self):
        exit_font = pygame.font.SysFont(self.font, self.size // 2)
        return exit_font.render('Press "e" to exit', True, (255, 0, 0))


class MonsterRoom:
    def __init__(self):
        pygame.init()

        self.load_images()
        self.player_width = self.images["robot"].get_width()
        self.player_height = self.images["robot"].get_height()
        self.coin_width = self.images["coin"].get_width()
        self.coin_height = self.images["coin"].get_height()
        self.monster_width = self.images["monster"].get_width()
        self.monster_height = self.images["monster"].get_height()
        self.door_width = self.images["door"].get_width()
        self.door_height = self.images["door"].get_height()
        
        self.width, self.height = 760, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        self.create_player()
        self.create_coin()

        self.game_over_menu = GameOverMenu("Arial", 70)

        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.SysFont("Arial", 24)
        
        self.right, self.left, self.up, self.down = False, False, False, False       # 4 checks used for player movement
        self.game_over_check = False                                                 # a check that tells if the game is over
        self.hunter_exists = False                                                   # a check for the existance of the hunter, it starts as false as the hunter appears at 10 points
        self.points = 0        

        self.monsters = []                                                           # a list which stores the monster objects created that are later moved, drawn on screen and eventually removed
        
        pygame.display.set_caption("Monster Room")

        self.main_loop()

# creates a dictionary of the images given for further use
    def load_images(self):
        self.images = {}                                                                    
        for name in ["robot", "monster", "coin", "door"]:                                       
            self.images[name] = pygame.image.load("pygame-Monster-Room/images/" + name + ".png")

# creates the player in the middle of the screen
    def create_player(self):
        self.player = Player(self.width//2 - self.player_width//2, self.height//2 - self.player_height//2, self.images["robot"])                         

# creates the coin in a random location except the outermost part of the screen
    def create_coin(self):
        self.coin = Coin(randint(40, self.width - self.coin_width - 40), randint(40, self.height - self.coin_height - 40), self.images["coin"])       

# creates the hunter in the bottom right corner    
    def create_hunter(self):
        self.hunter = Hunter(self.width, self.height, self.images["monster"])
        self.hunter_exists = True

# the methods create monsters coming from the specified location
    def create_m_upper_left(self):
        self.monsters.append(Monster(0 - self.monster_width, self.height // 3 - self.door_height, self.images["monster"], "left"))
    
    def create_m_lower_left(self):
        self.monsters.append(Monster(0 - self.monster_width, self.height // 3 * 2 - self.door_height, self.images["monster"], "left"))
    
    def create_m_left_up(self):
        self.monsters.append(Monster(self.width // 3 - self.monster_width // 2, 0 - self.monster_height, self.images["monster"], "up"))
    
    def create_m_right_up(self):
        self.monsters.append(Monster(self.width // 3 * 2 - self.monster_width // 2, 0 - self.monster_height, self.images["monster"], "up"))

# creates monsters randomly, the frequency inscreases from 10 to 30 points at which point it decreases for balance reasons as the monsters receive a speed bonus at 30 points
    def create_monsters(self):        
        if self.points < 10:
            n = randint(1, 280)
        if self.points >= 10 and self.points < 20:
            n = randint(1, 260)
        if self.points >= 20 and self.points < 30:
            n = randint(1, 240)
        if self.points >= 30:
            n = randint(1, 250)

        if n == 1 or n == 2 or n == 3:
            m = randint(1, 4)
            if m == 1:
                self.create_m_upper_left()
            if m == 2:
               self.create_m_lower_left()
            if m == 3:
                self.create_m_left_up()
            if m == 4:
                self.create_m_right_up()

# moves monsters every tick, at 30 points the monsters move faster   
    def move_monsters(self):
        for i in range(len(self.monsters)):            
            if self.points < 30:
                if self.monsters[i].origin == "left":
                    self.monsters[i].x += 2
                if self.monsters[i].origin == "up":
                    self.monsters[i].y += 2
            
            else:
                if self.monsters[i].origin == "left":
                    self.monsters[i].x += 3
                if self.monsters[i].origin == "up":
                    self.monsters[i].y += 3

# removes the monsters that leave the screen in order to use less resources
    def remove_m_outside_screen(self):
        outside = []
        for monster in self.monsters:
            if monster.x >= self.width or monster.y >= self.height:
                outside.append(monster)
        
        for monster in outside:
            self.monsters.remove(monster)

# checks if the player touched the coin
    def check_point(self, coin: Coin, player: Player):
        player_pixels = player.all_pixels()
        coin_pixels = coin.all_pixels()
        touched = False
        for x in coin_pixels[0]:
            for y in coin_pixels[1]:
                if x in range(player_pixels[0][0], player_pixels[0][1] + 1) and y in range(player_pixels[1][0], player_pixels[1][1] + 1):
                    touched = True

        return touched

# checks if the player touched a randomly generated monster
    def game_over_monster(self, index: int, player: Player):
        player_pixels = player.all_pixels()
        monster_pixels = self.monsters[index].all_pixels()        
        touched = False
        for x in range(monster_pixels[0][0], monster_pixels[0][1] + 1):
            for y in range(monster_pixels[1][0], monster_pixels[1][1] + 1):
                #the check excludes the outermost pixels of the player image because it has "empty space" around it and you shouldn't lose if the monster or hunter are only close to you
                if x in range(player_pixels[0][0] + 5, player_pixels[0][1] - 4) and y in range(player_pixels[1][0] + 5, player_pixels[1][1] - 4):   
                    touched = True

        return touched

# checks if the player touched the hunter 
    def game_over_hunter(self, player: Player):
        player_pixels = player.all_pixels()
        hunter_pixels = self.hunter.all_pixels()
        touched = False
        for x in range(hunter_pixels[0][0], hunter_pixels[0][1] + 1):
            for y in range(hunter_pixels[1][0], hunter_pixels[1][1] + 1):
                if x in range(player_pixels[0][0] + 5, player_pixels[0][1] - 4) and y in range(player_pixels[1][0] + 5, player_pixels[1][1] - 4):
                    touched = True

        return touched

# the main loop, if the game is over, it shows the game over screen, otherwise it shows the game screen   
    def main_loop(self):
        while True:
            if self.game_over_check:
                self.draw_game_over_screen()
                self.events_game_over()
                self.clock.tick(60)
            else:
                self.create_monsters()
                self.events()
                self.draw_screen()
                self.clock.tick(60)

# the events that happen in the game            
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.left = True
                if event.key == pygame.K_RIGHT:
                    self.right = True
                if event.key == pygame.K_UP:
                    self.up = True
                if event.key == pygame.K_DOWN:
                    self.down = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left = False
                if event.key == pygame.K_RIGHT:
                    self.right = False
                if event.key == pygame.K_UP:
                    self.up = False
                if event.key == pygame.K_DOWN:
                    self.down = False

            if event.type == pygame.QUIT:
                exit()

# moves the player and forbids him from leaving the screen
        if self.right and self.player.x < self.width - self.player_width:
            self.player.x += self.player.speed
        if self.left and self.player.x > 0:
            self.player.x -= self.player.speed
        if self.up and self.player.y > 0:
            self.player.y -= self.player.speed
        if self.down and self.player.y < self.height - self.player_height:
            self.player.y += self.player.speed

# if the player touched the coin it randomly moves elsewhere, and the points increase
        if self.check_point(self.coin, self.player):
            self.coin.change_coordinates()
            self.points += 1

# if the player gets 10 points the hunter is spawned, and if it exists it also moves towards the player
        if self.points >= 10 and not self.hunter_exists:
            self.create_hunter()

        if self.hunter_exists:
            self.hunter.move(self.player.x, self.player.y)

        self.move_monsters()
        self.remove_m_outside_screen()

# checks if the game is over either from monsters or from the hunter
        for i in range(len(self.monsters)):
            if self.game_over_monster(i, self.player):
               self.game_over_check = True
        
        if self.hunter_exists and self.game_over_hunter(self.player):
            self.game_over_check = True

# the events that can happen in the game over screen
    def events_game_over(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    MonsterRoom()
                if event.key == pygame.K_e:
                    exit()
            
            if event.type == pygame.QUIT:
                exit()

# draws the in game screen
    def draw_screen(self):
        self.screen.fill((205, 205, 205))
        
        self.screen.blit(self.player.image, (self.player.x, self.player.y))
        self.screen.blit(self.coin.image, (self.coin.x, self.coin.y))

        #draws the 2 doors on every side        
        self.screen.blit(self.images["door"], (-self.door_width / 2, self.height // 3 - self.door_height))                       
        self.screen.blit(self.images["door"], (-self.door_width / 2, self.height // 3 * 2 - self.door_height))
        self.screen.blit(self.images["door"], (self.width - self.door_width / 2, self.height // 3 - self.door_height))
        self.screen.blit(self.images["door"], (self. width - self.door_width / 2, self.height / 3 * 2 - self.door_height))
        
        self.screen.blit(self.images["door"], (self.width / 3 - self.door_width / 2, 0 - self.door_height / 1.5))
        self.screen.blit(self.images["door"], (self.width / 3 * 2 - self.door_width / 2, 0 - self.door_height / 1.5))
        self.screen.blit(self.images["door"], (self.width / 3 - self.door_width / 2, self.height - self.door_height / 3))
        self.screen.blit(self.images["door"], (self.width / 3 * 2 - self.door_width / 2, self.height - self.door_height / 3))
        
        for i in range(len(self.monsters)):
            self.screen.blit(self.monsters[i].image, (self.monsters[i].x, self.monsters[i].y))
        if self.hunter_exists:
            self.screen.blit(self.hunter.image, (self.hunter.x, self.hunter.y))

        points_text = self.game_font.render("Points: " + str(self.points), True, (255, 0, 0))
        self.screen.blit(points_text, (670, 10))
        
        pygame.display.flip()

# draws the game over prompt and the text for the 2 options given in the game over screen
    def draw_game_over_screen(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.game_over_menu.title(), (self.width / 2 - self.game_over_menu.title().get_width() / 2, 150))
        self.screen.blit(self.game_over_menu.new_game_text(), (self.width / 2 - self.game_over_menu.new_game_text().get_width() / 2, 180 + self.game_over_menu.title().get_height()))
        self.screen.blit(self.game_over_menu.exit_text(), (self.width / 2 - self.game_over_menu.exit_text().get_width() / 2, 210 + self.game_over_menu.title().get_height() + self.game_over_menu.new_game_text().get_height()))
        
        pygame.display.flip()


MonsterRoom()
