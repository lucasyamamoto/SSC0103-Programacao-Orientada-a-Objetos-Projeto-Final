import pygame
from element import GameObject, CircularObject, RectangularObject

class Level:
    LINE_COLOR = (0, 0, 0)
    SCALE = 100

    def __init__(self, objects: list, completed=False):
        if(not all(isinstance(obj, GameObject) for obj in objects)):
            raise TypeError("Game object list must be composed of game objects")

        self._objects = objects
        self._completed = completed

        # Search for ball and goal indexes
        self._ball_index = None
        self._goal_index = None
        self._middle_line_y = pygame.display.get_surface().get_height() // 2 + (pygame.display.get_surface().get_height()//2) % self.SCALE
        for i in range(len(objects)):
            if objects[i].name == 'Ball':
                self._ball_index = i
            elif objects[i].name == 'Goal':
                self._goal_index = i
        if self._ball_index is None:
            raise ValueError("Level doesn't contain a ball")
        elif self._goal_index is None:
            raise ValueError("Level doesn't contain a goal")
        elif self._objects[self._ball_index].x == self._objects[self._goal_index].x:
            raise ValueError("Ball and goal can't be above each other")
        self._middle_line_x = self._objects[self._ball_index].x

    @property
    def objects(self) -> list:
        return self._objects
    
    @property
    def is_completed(self) -> bool:
        return self._completed

    @is_completed.setter
    def is_completed(self, completed: bool):
        self._completed = completed

    def get_ball_pos(self) -> tuple:
        return (self._objects[self._ball_index].x, self._objects[self._ball_index].y)

    def set_ball_pos(self, new_pos: tuple):
        self._objects[self._ball_index].x, self._objects[self._ball_index].y = new_pos

    def get_goal_pos(self) -> tuple:
        return (self._objects[self._goal_index].x, self._objects[self._goal_index].y)

    def get_base_pos(self) -> tuple:
        return (self._objects[self._ball_index].x, self._middle_line_y)

    def get_relative_pos(self, other) -> tuple:
        return (other[0] - self._middle_line_x, self._middle_line_y - other[1])

    def check_goal_collision(self) -> bool:
        goal_x, goal_y = self.get_goal_pos()
        return self._objects[self._ball_index].collision(CircularObject(x=goal_x, y=goal_y))

    def check_wall_collision(self) -> bool:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for obj in self._objects:
            if isinstance(obj, RectangularObject) and self._objects[self._ball_index].collision(obj):
                return True
        return False


    def move_ball(self, equation: tuple, move_right: bool):
        # Get positions relative to the level coordinates
        relative_ball_pos = self.get_relative_pos(self.get_ball_pos())
        relative_goal_pos = self.get_relative_pos(self.get_goal_pos())
        new_x, new_y = relative_ball_pos

        # Move horizontally
        if move_right:
            new_x = relative_ball_pos[0] + 1
        else:
            new_x = relative_ball_pos[0] - 1

        # Move vertically
        new_y = ((equation[0] * ((new_x/self.SCALE) ** 2)) + (equation[1] * (new_x/self.SCALE)) + equation[2]) * self.SCALE
        self.set_ball_pos((self.get_ball_pos()[0] + (new_x - relative_ball_pos[0]), self.get_ball_pos()[1] - (new_y - relative_ball_pos[1])))

    def display(self, window):
        # Draw objects
        for obj in self.objects:
            obj.display(window)

        # Draw vertical lines
        for i in range(self._middle_line_x % self.SCALE, window.get_width(), self.SCALE):
            pygame.draw.line(window, self.LINE_COLOR, (i, 0), (i, window.get_height()), 1)

        # Draw Y-axis from ball position
        pygame.draw.line(window, self.LINE_COLOR, (self._middle_line_x, 0), (self._middle_line_x, window.get_height()), 3)

        # Draw horizontal lines
        for i in range(0, window.get_height(), self.SCALE):
            pygame.draw.line(window, self.LINE_COLOR, (0, i), (window.get_width(), i), 1)

        # Draw X-axis near the middle of the screen
        pygame.draw.line(window, self.LINE_COLOR, (0, self._middle_line_y), (window.get_width(), self._middle_line_y), 3)

class LevelManager:
    def __init__(self, level_list = []):
        self._list = level_list
        self._size = len(level_list)

    @property
    def size(self):
        return self._size

    def get_level(self, index: int) -> Level:
        if self.size <= abs(index):
            raise ValueError("Index out of bounds")
        return self._list[index]
    
    def set_level(self, level: Level, index: int):
        if index >= abs(index):
            raise ValueError("Index out of bounds")
        self._list[index] = level
    
    def load(self, file_name: str, index=None):
        level_obj = []
        # Read object from file
        with open(file_name, 'r') as f:
            obj = f.readline()
            while obj:
                # Parse line from file
                obj = obj.rstrip().split(',')
                # Check if object is a wall
                if obj[0] == 'Wall' and len(obj) == 6:
                    image = pygame.image.load(obj[5]).convert_alpha() if obj[5] != 'None' else None
                    level_obj.append(RectangularObject(obj[0], int(obj[1]), int(obj[2]), int(obj[3]), int(obj[4]), image))
                # Check if object is a goal
                elif obj[0] == 'Goal' and len(obj) == 5:
                    image = pygame.image.load(obj[4]).convert_alpha() if obj[4] != 'None' else None
                    level_obj.append(CircularObject(obj[0], int(obj[1]), int(obj[2]), int(obj[3]), image))
                # Check if object is a ball
                elif obj[0] == 'Ball' and len(obj) == 5:
                    image = pygame.image.load(obj[4]).convert_alpha() if obj[4] != 'None' else None
                    level_obj.append(CircularObject(obj[0], int(obj[1]), int(obj[2]), int(obj[3]), image))
                # Then file doesn't follow any of the specifications
                else:
                    raise IOError("Level file is corrupted")
                obj = f.readline()
        if index is None:
            # Create object and append to list
            self._list.append(Level(level_obj))
            # Update size
            self._size = len(self._list)
        elif abs(index) < self.size:
            self._list[index] = Level(level_obj)
        else:
            raise ValueError("Invalid index")

    def save(self, file_name: str):
        with open(file_name, 'w') as f:
            ...

    def display(self, window, index: int):
        if index is not int:
            raise TypeError("Index must be int")
        if index >= abs(index):
            raise ValueError("Index out of bounds")
        self._list[index].display(window)