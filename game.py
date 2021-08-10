import pygame
import random
from menu import  *
import sys

def detect_collision(player_position, enemy_position, player_dimension,enemy_dimension):
    p_x = player_position[0]
    p_y = player_position[1]
    e_x = enemy_position[0]
    e_y = enemy_position[1]

    if p_x < e_x < (p_x + player_dimension[0]) or e_x < p_x < (e_x + enemy_dimension[0]):
        if p_y < e_y < (p_y + player_dimension[1]) or (e_y < p_y < (e_y + enemy_dimension[1])):
            return True

    return False


class  Game():
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY,self.BACK_KEY,self.ESC=False,False,False,False,False
        self.DISPLAY_W, self.DISPLAY_H = 500, 1000
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE,self.GREEN,self.RED,self.YELLOW = (0, 0, 0), (255, 255, 255),(0, 255, 0),(255, 0, 0),(255, 255, 0)
        self.SPEED=3
        self.score=0
        self.player_dimension=[20,20]
        self.player_position=[self.DISPLAY_W / 2, self.DISPLAY_H / 2]
        self.enemy_dimension=[10,50]
        self.enemy_position=[random.randint(0, self.DISPLAY_W - self.enemy_dimension[0]), 100]
        self.enemy_list=[]
        self.main_menu=MainMenu(self)
        self.credits=CreditsMenu(self)
        self.curr_menu=self.main_menu

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.display.fill(self.BLACK)
            self.draw_text(f'Score: {self.score}',30,120,20)
            self.window.blit(self.display,(0,0))

            # drop enemies
            delay = random.random()
            if len(self.enemy_list) < 10 and delay < 0.005:
                x_pos = random.randint(0, self.DISPLAY_W - self.enemy_dimension[0])
                y_pos = 0
                self.enemy_list.append([x_pos, y_pos])

            # draw enemies
            for position_enemy in self.enemy_list:
                pygame.draw.rect(self.window, self.GREEN, (position_enemy[0], position_enemy[1], self.enemy_dimension[0], self.enemy_dimension[1]))

            # draw mouse player 
            mouse_position = pygame.mouse.get_pos()
            self.player_position = [mouse_position[0],  mouse_position[1]]
            pygame.draw.rect(self.window, self.RED, (self.player_position[0], self.player_position[1], self.player_dimension[0], self.player_dimension[1]))

            
            # update score
            for position_enemy in self.enemy_list:
                if 0 <= position_enemy[1] < self.DISPLAY_H:
                    position_enemy[1] = position_enemy[1] + self.SPEED
                else:
                    self.score = self.score + 1
                    position_enemy[1] = 0
                    position_enemy[0] = random.randint(0, self.DISPLAY_W - self.enemy_dimension[0])

        
            # detect collisions
            for enemy in self.enemy_list:
                if detect_collision(self.player_position, enemy, self.player_dimension, self.enemy_dimension):
                    self.enemy_list=[]
                    self.score=0
                    self.playing=False


            pygame.display.update()
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    self.START_KEY=True
                    print('enter')
                if event.key==pygame.K_BACKSPACE:
                    self.BACK_KEY=True
                    print('backspace')
                if event.key==pygame.K_DOWN:
                    print('donw')
                    self.DOWN_KEY=True
                if event.key==pygame.K_UP:
                    self.UP_KEY=True
                    print('up')
                if event.key==pygame.K_ESCAPE:
                    self.ESC=True
                    print('esc')

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY,self.BACK_KEY,self.ESC=False,False,False,False,False


    def draw_text(self,text,size,x,y):
        font=pygame.font.Font(self.font_name,size)
        text_surface=font.render(text,True,self.WHITE)
        text_rect=text_surface.get_rect()
        text_rect.center=(x,y)
        self.display.blit(text_surface,text_rect)


