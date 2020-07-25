import pygame
from abc import ABC, abstractmethod
from level import Level

class InterfaceManager(ABC):
    KEYMAXTICK = 60

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
        start_button = TextBox('start', 'Iniciar', self.FONTCOLOR, width//2, height//2, TextBox.ALIGN_CENTER, 'arial', 32, clicable=True)
        exit_button = TextBox('exit', 'Sair', self.FONTCOLOR, width//2, (height//2)+start_button.height, TextBox.ALIGN_CENTER, 'arial', 32, clicable=True)
        super().__init__([start_button, exit_button])

    def listen(self, game, event):
        mouse_pos = pygame.mouse.get_pos()
        
        for elem in self._elements:
            if isinstance(elem, TextBox):
                # Hover animations
                if elem.hover(mouse_pos) and elem.clicable:
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
            level_buttons = [TextBox('level0', 'Tutorial', self.FONTCOLOR, width//2, (height//2), clicable=True)]
            for i in range(1, num_levels-1):
                level_buttons.append(TextBox(f'level{i}', f'Nível {i}', self.FONTCOLOR, width//2, (height//2)+(level_buttons[0].height*i), clicable=True))
            level_buttons.append(TextBox(f'level{num_levels}', 'Voltar ao menu principal', self.FONTCOLOR, width//2, (height//2)+(level_buttons[0].height*num_levels), clicable=True))
        else:
            level_buttons = [TextBox('back', 'Voltar ao menu principal', self.FONTCOLOR, width//2, (height//2), clicable=True)]
        super().__init__(level_buttons)

    def listen(self, game, event):
        mouse_pos = pygame.mouse.get_pos()
        
        for elem in self._elements:
            if isinstance(elem, TextBox):
                # Hover animations
                if elem.hover(mouse_pos) and elem.clicable:
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

    def __init__(self, level: Level):
        self._equation = [0.0, 0.0, 0.0]
        self._attempt = False
        self._move_right = None

        # Create exit button
        width, height = pygame.display.get_surface().get_size()
        exit_button = TextBox('sair', 'Sair', self.FONTCOLOR, width-(width//20), height-(height//20), clicable=True)

        # Create mouse tracker
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = level.get_relative_pos(mouse_pos)
        mouse_tracker = TextBox('mousetracker', f'Mouse: x = {mouse_pos[0]}, y = {mouse_pos[1]}', self.FONTCOLOR, 2, 0, TextBox.ALIGN_LEFT, size=20)
        mouse_tracker.y = height - round(mouse_tracker.height/2)

        # Create goal tracker
        goal_pos = level.get_goal_pos()
        goal_pos = level.get_relative_pos(goal_pos)
        goal_tracker = TextBox('goaltracker', f'Objetivo: x = {mouse_pos[0]}, y = {mouse_pos[1]}', self.FONTCOLOR, 2, height-round(1.5 * mouse_tracker.height), TextBox.ALIGN_LEFT, size=20)
        
        # Create ball tracker
        ball_pos = level.get_ball_pos()
        ball_pos = level.get_relative_pos(ball_pos)
        ball_tracker = TextBox('balltracker', f'Bola: x = {ball_pos[0]}, y = {ball_pos[1]}', self.FONTCOLOR, 2, height-round(2.5 * mouse_tracker.height), TextBox.ALIGN_LEFT, size=20)
        
        # Create equation format
        equation_c_text = f' + {ball_pos[1]}' if ball_pos[1] >= 0 else f' - {abs(ball_pos[1])}'
        equation_text = TextBox('equationtext', ''.join(['f(x) = ______x² + ______x', equation_c_text]), self.FONTCOLOR, goal_tracker.width+(width-goal_tracker.width-exit_button.width-width//20-2)//2, height-(height//15), size=30)
        self._equation[2] = ball_pos[1]

        # Create writable text boxes
        offset1 = TextBox('', 'f(x) = ______', size=30).width
        offset2 = TextBox('', 'x² + ______', size=30).width

        input_x_squared = InteractiveTextBox(name='x_squared', x=(equation_text.x-(equation_text.width//2)+offset1), y=height-(height//15), alignment=TextBox.ALIGN_RIGHT, size=30, clicable=True, char_limit=6)
        input_x = InteractiveTextBox(name='x_normal', x=(input_x_squared.x+offset2), y=height-(height//15), alignment=TextBox.ALIGN_RIGHT, size=30, clicable=True, char_limit=6)

        super().__init__([mouse_tracker, exit_button, equation_text, ball_tracker, goal_tracker, input_x_squared, input_x])

    @property
    def equation(self) -> tuple:
        return self._equation

    @property
    def attempt(self) -> bool:
        return self._attempt

    @attempt.setter
    def attempt(self, new_value: bool):
        self._attempt = new_value

    @property
    def move_right(self) -> bool:
        return self._move_right

    @move_right.setter
    def move_right(self, right: bool):
        self._move_right = right

    def listen(self, game, event):
        # Mouse related events
        mouse_pos = pygame.mouse.get_pos()

        for elem in self._elements:
            if isinstance(elem, TextBox):
                # Hover animations
                if elem.hover(mouse_pos) and elem.clicable:
                    # Hovering
                    elem.color = (255, 255, 255)
                    elem.background = self.FONTCOLOR
                    # Menu interactions
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if elem.text == 'Sair':
                            game.exit_current_level()
                        elif isinstance(elem, InteractiveTextBox):
                            elem.activate()
                        else:
                            InteractiveTextBox.deactivate_all()
                else:
                    # Not hovering
                    elem.color = self.FONTCOLOR
                    elem.background = None
                # Update mouse tracker
                if elem.text[:5] == 'Mouse':
                    relative_mouse_pos = game.get_current_level().get_relative_pos(mouse_pos)
                    elem.text = f'Mouse: x = {relative_mouse_pos[0]}, y = {relative_mouse_pos[1]}'
                if isinstance(elem, InteractiveTextBox):
                    if elem.name == 'x_squared':
                        self._equation[0] = elem.float()
                    elif elem.name == 'x_normal':
                        self._equation[1] = elem.float()
        
        # Keyboard related events
        if event.type == pygame.KEYDOWN:
            if InteractiveTextBox.active_textbox is not None:
                if event.unicode.isnumeric():
                    InteractiveTextBox.active_textbox.write_char(event.unicode)
                elif event.unicode == '-' and len(InteractiveTextBox.active_textbox.text) == 0:
                    InteractiveTextBox.active_textbox.write_char(event.unicode)
                elif event.unicode == ',' and len(InteractiveTextBox.active_textbox.text.replace('-', '')) > 0 and ',' not in InteractiveTextBox.active_textbox.text:
                    InteractiveTextBox.active_textbox.write_char(event.unicode)
                elif event.key == pygame.K_BACKSPACE:
                    InteractiveTextBox.active_textbox.delete_char()
            if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                self._attempt = True

class InterfaceElement:
    def __init__(self, name='interfaceelement', x=0, y=0, image=None):
        if image is None or isinstance(image, pygame.Surface):
            self._image = image
        else:
            raise TypeError("Image must be a surface object")
        self._name = name
        self._x = x
        self._y = y

    @property
    def name(self):
        return self._name

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

    def __init__(self, name='textbox', text='', color=(0, 0, 0), x=0, y=0, alignment=0, font_name='arial', size=32, bold=False, italic=False, background=None, clicable=False):
        super().__init__(name, x, y)
        self._font = pygame.font.SysFont(font_name, size, bold, italic)
        self._text = text
        self._color = color
        self._background = background
        self._render = self._font.render(text, 1, color, background)
        self._alignment = alignment
        self._clicable = clicable

    @property
    def font(self) -> pygame.font.Font:
        return self._font

    @font.setter
    def font(self, new_font: pygame.font.Font):
        if self._font != new_font:
            self._font = new_font
            self._render = self.render(self.text, 1, self.color, self.background)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, new_text: str):
        if self._text != new_text:
            self._text = new_text
            self._render = self.render(new_text, 1, self.color, self.background)

    @property
    def color(self) -> tuple:
        return self._color

    @color.setter
    def color(self, new_color: tuple):
        if self._color != new_color:
            self._color = new_color
            self._render = self.render(self.text, 1, new_color, self.background)

    @property
    def background(self) -> tuple:
        return self._background

    @background.setter
    def background(self, new_color: tuple):
        if self._background is None or self._background != new_color:
            self._background = new_color
            self._render = self.render(self.text, 1, self.color, self.background)

    @property
    def width(self):
        return self._render.get_width()

    @property
    def height(self):
        return self._render.get_height()

    @property
    def clicable(self) -> bool:
        return self._clicable

    @clicable.setter
    def clicable(self, can_click: bool):
        self._clicable = can_click

    def render(self, text, antialiasing, color, background=None) -> pygame.Surface:
        return self._font.render(text, antialiasing, color, background)

    def hover(self, mouse_pos: tuple) -> bool:
        # Check if mouse position collides with Y-coordinates of textbox
        collision_y = mouse_pos[1] >= self.y-(self.height//2) and mouse_pos[1] <= (self.y+self.height//2)

        # Check if mouse position collides with X-coordinates of textbox
        if self._alignment == self.ALIGN_CENTER:
            collision_x = mouse_pos[0] >= self.x-(self.width//2) and mouse_pos[0] <= self.x+(self.width//2)
        elif self._alignment == self.ALIGN_LEFT:
            collision_x = mouse_pos[0] >= self.x and mouse_pos[0] <= self.x+self.width
        else:
            collision_x = mouse_pos[0] >= self.x-self.width and mouse_pos[0] <= self.x

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
    IDLE_CHAR = '|'
    BLANK_CHAR = '_'
    active_textbox = None

    def __init__(self, name='interactivetextbox', text='', color=(0, 0, 0), x=0, y=0, alignment=0, font_name='arial', size=32, bold=False, italic=False, background=None, clicable=False, char_limit=None):
        super().__init__(name, text, color, x, y, alignment, font_name, size, bold, italic, background, clicable)
        self._limit = char_limit

    @property
    def active(self):
        return self == InteractiveTextBox.active_textbox

    def activate(self):
        if self != InteractiveTextBox.active_textbox:
            InteractiveTextBox.active_textbox = self
            self._render = self.render(self.text, 1, self.color, self.background)

    @classmethod
    def deactivate_all(cls):
        if cls.active_textbox is not None:
            last_textbox = cls.active_textbox
            cls.active_textbox = None
            last_textbox._render = last_textbox.render(last_textbox.text, 1, last_textbox.color, last_textbox.background)

    @property
    def width(self) -> int:
        return self._render.get_width()

    def render(self, text, antialiasing, color, background=None) -> pygame.Surface:
        if self.active and len(self.text) < self._limit:
            new_text = text + self.IDLE_CHAR
        else:
            new_text = text
        if self._limit is not None:
            if self._alignment == self.ALIGN_LEFT:
                new_text = new_text + ' '*(self._limit - len(new_text))
            elif self._alignment == self.ALIGN_CENTER:
                new_text = self.BLANK_CHAR*((self._limit - len(new_text))//2) + new_text + self.BLANK_CHAR*round((self._limit - len(new_text))/2)
            else:
                new_text = self.BLANK_CHAR*(self._limit - len(new_text)) + new_text
        return self._font.render(new_text, antialiasing, color, background)

    def delete_char(self):
        if self.active and len(self.text) > 0:
            self._text = self.text[:-1]
            self._render = self.render(self.text, 1, self.color, self.background)

    def write_char(self, new_char: str):
        if self.active and len(self.text) < self._limit:
            self._text = self.text + new_char
            self._render = self.render(self.text, 1, self.color, self.background)

    def float(self) -> float:
        newtext = self.text if self.text != '' and self.text[-1] != ',' and self.text[-1] != '-' else self.text + '0'
        return float(newtext.replace(',', '.'))