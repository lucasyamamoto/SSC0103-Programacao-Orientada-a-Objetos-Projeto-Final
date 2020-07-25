import pygame
from abc import ABC, abstractmethod

class InterfaceManager(ABC):
    def __init__(self, elements = []):
        if(not all(isinstance(elem, InterfaceElement) for elem in elements)):
            raise TypeError("Element list must be composed of interface elements")
        self._elements = elements

    def display(self, window):
        for elem in self._elements:
            elem.display(window)

    @abstractmethod
    def listen(self, game, event):
        ...

class MainMenu(InterfaceManager):
    FONTCOLOR = (0, 0, 0)
    def __init__(self):
        width, height = pygame.display.get_surface().get_size()
        start_button = TextBox('Iniciar', self.FONTCOLOR, width//2, height//2, TextBox.ALIGN_CENTER, 'arial', 32)
        exit_button = TextBox('Sair', self.FONTCOLOR, width//2, (height//2)+start_button.height, TextBox.ALIGN_CENTER, 'arial', 32)
        super().__init__([start_button, exit_button])

    def listen(self, game, event):
        mouse_pos = pygame.mouse.get_pos()
        
        for elem in self._elements:
            if isinstance(elem, TextBox):
                # Hover animations
                if elem.hover(mouse_pos):
                    elem.color = (255, 255, 255)
                    elem.background = self.FONTCOLOR
                    # Menu interactions
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if elem.text == 'Iniciar':
                            game.open_level_selection()
                        elif elem.text == 'Sair':
                            game.quit()
                else:
                    elem.color = self.FONTCOLOR
                    elem.background = (255, 255, 255)

class LevelSelection(InterfaceManager):
    FONTCOLOR = (0, 0, 0)

    def __init__(self, num_levels: int):
        width, height = pygame.display.get_surface().get_size()
        if num_levels > 0:
            level_buttons = [TextBox('Tutorial', self.FONTCOLOR, width//2, (height//2))]
            for i in range(1, num_levels-1):
                level_buttons.append(TextBox(f'Nível {i}', self.FONTCOLOR, width//2, (height//2)+(level_buttons[0].height*i)))
            level_buttons.append(TextBox('Voltar ao menu principal', self.FONTCOLOR, width//2, (height//2)+(level_buttons[0].height*num_levels)))
        else:
            level_buttons = [TextBox('Voltar ao menu principal', self.FONTCOLOR, width//2, (height//2))]
        super().__init__(level_buttons)

    def listen(self, game, event):
        mouse_pos = pygame.mouse.get_pos()
        
        for elem in self._elements:
            if isinstance(elem, TextBox):
                # Hover animations
                if elem.hover(mouse_pos):
                    elem.color = (255, 255, 255)
                    elem.background = self.FONTCOLOR
                    # Menu interactions
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if elem.text[:6] == 'Nível ':
                            game.set_current_level(int(elem.text[6:]))
                        elif elem.text == 'Voltar ao menu principal':
                            game.open_main_menu()
                        elif elem.text == 'Tutorial':
                            game.set_current_level(0)
                else:
                    elem.color = self.FONTCOLOR
                    elem.background = (255, 255, 255)

class GameInterface(InterfaceManager):
    FONTCOLOR = (0, 0, 0)

    def __init__(self):
        width, height = pygame.display.get_surface().get_size()
        equation_text = TextBox('f(x) =           x² +           x', self.FONTCOLOR, width//2, height-(height//20))
        exit_button = TextBox('Sair', self.FONTCOLOR, 0, height-(height//20))
        exit_button.x = width-(width//20)
        super().__init__([equation_text, exit_button])

    def listen(self, game, event):
        mouse_pos = pygame.mouse.get_pos()

        for elem in self._elements:
            if isinstance(elem, TextBox):
                # Hover animations
                if elem.hover(mouse_pos):
                    elem.color = (255, 255, 255)
                    elem.background = self.FONTCOLOR
                    # Menu interactions
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if elem.text == 'Sair':
                            game.exit_current_level()
                else:
                    elem.color = self.FONTCOLOR
                    elem.background = (255, 255, 255)

class InterfaceElement:
    def __init__(self, x, y, image=None):
        if image is None or isinstance(image, pygame.Surface):
            self._image = image
        else:
            raise TypeError("Image must be a surface object")
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, new_x):
        self._x = new_x

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, new_y):
        self._y = new_y

    @property
    def width(self):
        return self._image.get_width() if self._image is not None else 0

    @property
    def height(self):
        return self._image.get_height() if self._image is not None else 0

    def hover(self, mouse_pos: tuple) -> bool:
        return mouse_pos[0] >= self.x and mouse_pos[0] <= self.x+self.width and mouse_pos[1] >= self.y and mouse_pos[1] <= self.y+self.height

    def display(self, window):
        window.blit(self._image, (self._x, self._y))

class TextBox(InterfaceElement):
    ALIGN_CENTER = 0
    ALIGN_LEFT = 1
    ALIGN_RIGHT = 2

    def __init__(self, text="", color=(0, 0, 0), x=0, y=0, alignment=0, font_name='arial', size=32, bold=False, italic=False, background=None):
        super().__init__(x, y)
        self._font = pygame.font.SysFont(font_name, size, bold, italic)
        self._text = text
        self._color = color
        self._background = background
        self._render = self._font.render(text, 1, color, background)
        self._alignment = alignment

    @property
    def font(self) -> pygame.font.Font:
        return self._font

    @font.setter
    def font(self, new_font: pygame.font.Font):
        if self._font != new_font:
            self._font = new_font
            self._render = new_font.render(self.text, 1, self.color, self.background)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, new_text: str):
        if self._text != new_text:
            self._text = new_text
            self._render = self._font.render(new_text, 1, self.color, self.background)

    @property
    def color(self) -> tuple:
        return self._color

    @color.setter
    def color(self, new_color: tuple):
        if self._color != new_color:
            self._color = new_color
            self._render = self._font.render(self.text, 1, new_color, self.background)

    @property
    def background(self) -> tuple:
        return self._background

    @background.setter
    def background(self, new_color: tuple):
        if self._background is None or self._background != new_color:
            self._background = new_color
            self._render = self._font.render(self.text, 1, self.color, self.background)

    @property
    def width(self):
        return self._render.get_width()

    @property
    def height(self):
        return self._render.get_height()

    def hover(self, mouse_pos: tuple) -> bool:
        # Check if mouse position collides with Y-coordinates of textbox
        collision_y = mouse_pos[1] >= self.y-(self.height//2) and mouse_pos[1] <= (self.y+self.height//2)

        # Check if mouse position collides with X-coordinates of textbox
        if self._alignment == self.ALIGN_CENTER:
            collision_x = mouse_pos[0] >= self.x-(self.width//2) and mouse_pos[0] <= self.x+(self.width//2)
        elif self._alignment == self.ALIGN_LEFT:
            collision_x = mouse_pos[0] >= self.x and mouse_pos[0] <= self.x+self.width
        else:
            collision_x = mouse_pos[0] >= self.x+self.width and mouse_pos[0] <= self.x

        return collision_x and collision_y

    def display(self, window):
        # Display text according to the aligmnent of the text
        if self._alignment == self.ALIGN_CENTER:
            window.blit(self._render, (self.x-(self.width//2), self.y-(self.height//2)))
        elif self._alignment == self.ALIGN_LEFT:
            window.blit(self._render, (self.x, self.y-(self.height//2)))
        else:
            window.blit(self._render, (self.x-self.width, self.y-(self.height//2)))

class InteractiveTextBox(TextBox):
    IDLE_CHAR = '_'
    def __init__(self, text="", color=(0, 0, 0), x=0, y=0, font_name='arial', size=32, bold=False, italic=False, background=None, char_limit=None):
        super().__init__(text, color, x, y, font_name, size, bold, italic, background)
        self._active = False
        self._limit = char_limit

    @property
    def active(self):
        return self._active

    def activate(self):
        if not self._active:
            self._active = True
            self._render = self._font.render(self.text + IDLE_CHAR, 1, self.color, self.background)
    
    def deactivate(self):
        if self._active:
            self._active = False
            self._render = self._font.render(self.text, 1, self.color)

    def delete_char(self):
        if self._active and len(self.text) > 0:
            self._text = self.text[:-1]
            self._render = self._font.render(self.text + IDLE_CHAR, 1, self.color, self.background)

    def write_char(self, new_char: str):
        if self._active and len(self.text) < self._limit:
            self._text = self.text.append(new_char)
            self._render = self._font.render(self.text + IDLE_CHAR, 1, self.color, self.background)