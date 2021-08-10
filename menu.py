import pygame

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W/2, self.game.DISPLAY_H/2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -150

    def draw_cursor(self):
        self.game.draw_text('*', 40, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Start'
        self.startx, self.starty = self.mid_w, self.mid_h
        self.creditsx, self.creditsy = self.mid_w, self.mid_h+100
        self.cursor_rect.midtop = (self.startx+self.offset, self.starty)
       

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Start Game', 40, self.startx, self.starty)
            self.game.draw_text('(Press enter)', 20, self.startx, self.starty+25)
            self.game.draw_text('Credits', 40, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (
                    self.creditsx+self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (
                    self.startx+self.offset, self.starty)
                self.state = 'Start'

        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (
                    self.creditsx+self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (
                    self.startx+self.offset, self.starty)
                self.state = 'Start'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self,game)

    def display_menu(self):
        self.run_display = True

        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY or self.game.ESC:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)
            self.game.draw_text('GimboGeek', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 30)
            self.game.draw_text('Follow me on tiktok if you like the game', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 60)
            self.blit_screen()