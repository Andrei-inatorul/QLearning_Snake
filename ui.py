import pygame
import sys
import gameloop

class UI_BUTTON:
    def __init__(self, x, y, width, height, text, font_color:tuple, color:tuple, fcolor_hovered=None, color_hovered = None):
        self.font = pygame.font.SysFont("Impact", height-10)
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
        self.font_color = font_color
        self.color = color
        self.fcolor_hovered = font_color if fcolor_hovered is None else fcolor_hovered
        self.color_hovered = color if color_hovered is None else color_hovered

    def render(self, screen):
        text = None
        if(self.is_hovered):
            text = f"> {self.text}"
        else:
            text = self.text
        pygame.draw.rect(screen, self.color if self.is_hovered == False else self.color_hovered, self.rect)
        text_surface = self.font.render(text, True, self.font_color if self.is_hovered == False else self.fcolor_hovered)
        screen.blit(text_surface, (self.rect.x+3, self.rect.y+2))

    def check_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, click_event):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and click_event == True:
            return True

def titlescreen(screen: pygame.Surface):
    menu_background = pygame.image.load('./Assets/bg.jpg')
    FONT_COLOR = (234, 234, 234)
    MENU_TEXT = pygame.font.SysFont('Impact', 60)
    text_surface = MENU_TEXT.render(f'> Q_Learning_Snake', True, FONT_COLOR)

    play_as_user = UI_BUTTON(100, 250, 360, 50, "Joacă", FONT_COLOR, (34, 49, 29), (47, 47, 47), (255, 255, 255))
    train = UI_BUTTON(100, 320, 360, 50, "Antrenează Modelul", FONT_COLOR, (34, 49, 29), (47, 47, 47), (255, 255, 255))
    test = UI_BUTTON(100, 390, 360, 50, "Testează Modelul", FONT_COLOR, (34, 49 ,29), (47, 47, 47), (255, 255, 255))
    while True:
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        play_as_user.check_hovered()
        train.check_hovered()
        test.check_hovered()

        if (play_as_user.check_click(clicked)):
            return 1
        if (train.check_click(clicked)):
            return 2
        if (test.check_click(clicked)):
            return 3

        screen.blit(menu_background, (0, 0))
        screen.blit(text_surface, (100, 150))
        play_as_user.render(screen)
        train.render(screen)
        test.render(screen)
        pygame.display.update()