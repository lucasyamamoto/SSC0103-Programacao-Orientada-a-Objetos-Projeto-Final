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
        for i in range(len(objects)):
            if objects[i].name == 'Ball':
                self._ball_index = i
            elif objects[i].name == 'Goal':
                self._goal_index = i
        if self._ball_index is None:
            raise ValueError("Level doesn't contain a ball")
        elif self._ball_index is None:
            raise ValueError("Level doesn't contain a goal")

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

    def get_goal_pos(self) -> tuple:
        return (self._objects[self._goal_index].x, self._objects[self._goal_index].y)

    def display(self, window):
        # Draw objects
        for obj in self.objects:
            if obj.image is not None:
                window.blit(obj.image, (obj.x, obj.y))

        # Draw vertical lines
        for i in range(self._objects[self._ball_index].x % self.SCALE, window.get_width(), self.SCALE):
            pygame.draw.line(window, self.LINE_COLOR, (i, 0), (i, window.get_height()), 1)

        # Draw Y-axis from ball position
        pygame.draw.line(window, self.LINE_COLOR, (self._objects[self._ball_index].x, 0), (self._objects[self._ball_index].x, window.get_height()), 3)

        # Draw horizontal lines
        for i in range(0, window.get_height(), self.SCALE):
            pygame.draw.line(window, self.LINE_COLOR, (0, i), (window.get_width(), i), 1)

        # Draw X-axis near the middle of the screen
        middle_line_y = window.get_height() // 2 + (window.get_height()//2) % self.SCALE
        pygame.draw.line(window, self.LINE_COLOR, (0, middle_line_y), (window.get_width(), middle_line_y), 3)

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
    
    def load(self, file_name: str):
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
        # Create object and append to list
        self._list.append(Level(level_obj))
        # Update size
        self._size = len(self._list)

    def save(self, file_name: str):
        with open(file_name, 'w') as f:
            ...

    def display(self, window, index: int):
        if index is not int:
            raise TypeError("Index must be int")
        if index >= abs(index):
            raise ValueError("Index out of bounds")
        self._list[index].display(window)