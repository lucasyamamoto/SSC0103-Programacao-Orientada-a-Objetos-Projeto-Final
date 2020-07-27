import pygame
from equation.element import GameObject, CircularObject, RectangularObject

class Level:
    """Level which administrates the game objects inside it"""
    LINE_COLOR = (0, 0, 0)
    SCALE = 100

    def __init__(self, objects: list):
        """
        Constructor of a Level object. Object list must have a ball and a goal and they must not be on the same x coordinate

        :param list objects: List of level objects of type GameObject
        :raise TypeError: List contain something other than a GameObject
        :raise ValueError: Missing ball, goal or they are in the same x coordinate
        """
        if(not all(isinstance(obj, GameObject) for obj in objects)):
            raise TypeError("Game object list must be composed of game objects")

        self._objects = objects

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
        """Getter of the objects attribute"""
        return self._objects

    def get_ball_pos(self) -> tuple:
        """Get ball coordinates"""
        return (self._objects[self._ball_index].x, self._objects[self._ball_index].y)

    def set_ball_pos(self, new_pos: tuple):
        """Set ball coordinates"""
        self._objects[self._ball_index].x, self._objects[self._ball_index].y = new_pos

    def get_goal_pos(self) -> tuple:
        """Get goal coordinates"""
        return (self._objects[self._goal_index].x, self._objects[self._goal_index].y)

    def get_base_pos(self) -> tuple:
        """Get origin relative to the Level xy plane"""
        return (self._objects[self._ball_index].x, self._middle_line_y)

    def get_relative_pos(self, other) -> tuple:
        """Get position of an object relative to the Level xy plane"""
        return (other[0] - self._middle_line_x, self._middle_line_y - other[1])

    def check_goal_collision(self) -> bool:
        """Check if ball collided with the goal object"""
        goal_x, goal_y = self.get_goal_pos()
        return self._objects[self._ball_index].collision(CircularObject(x=goal_x, y=goal_y))

    def check_wall_collision(self) -> bool:
        """Check if ball collided with a wall object"""
        for obj in self._objects:
            if isinstance(obj, RectangularObject) and self._objects[self._ball_index].collision(obj):
                return True
        return False

    def move_ball(self, equation: tuple, move_right: bool):
        """
        Move the ball object one pixel in the X-axis and n pixels in the Y-axis according to an equation

        :param tuple equation: Tuple of the three coeficients of an quadratic function
        :param bool move_right: True if it should move to the right and False if it should move to the left
        """

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
        new_y = ((equation[0] * ((new_x/self.SCALE) ** 2)) + (equation[1] * (new_x/self.SCALE)) + equation[2]/self.SCALE) * self.SCALE
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
    """Holds and administrates all the levels"""
    def __init__(self, level_list = []):
        """
        Constructor of the LevelManager object

        :param level_list: list of available levels
        """
        self._list = level_list
        self._size = len(level_list)

    @property
    def size(self):
        """Getter of the size attribute"""
        return self._size

    def get_level(self, index: int) -> Level:
        """
        Get level of a specified index

        :param int index: Index of the level
        :return:
        Level: Level at the index
        :raise ValueError: Invalid index
        """
        if self.size <= abs(index):
            raise ValueError("Index out of bounds")
        return self._list[index]
    
    def set_level(self, level: Level, index: int):
        """
        Set level of a specified index

        :param Level level: Level object to replace another
        :param int index: Index of the level
        :return:
        Level: Level at the index
        :raise ValueError: Invalid index
        """
        if index >= abs(index):
            raise ValueError("Index out of bounds")
        self._list[index] = level
    
    def load(self, file_name: str, index=None):
        """
        Read a level from a file. Index can be specified to replace an existing level in the list.
        File lines format:
            [Object],[param1],[param2],...,[image_file]
            Goal,x,y,radius,image_file
            Ball,x,y,radius,image_file
            Wall,x,y,width,height,image_file

        :param str file_name: Name of the file
        :param index: Optional. Replaces level with the index specified in the list. Int or None
        :raise FileNotFoundError: File doesn't exist
        :raise IOError: File doesn't follow the format required
        """
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

    def display(self, window, index: int):
        """
        Display level at specified index

        :param window: Window surface to display the level
        :param int index: Index of the level
        :raise ValueError: Invalid index
        """
        if index >= abs(index):
            raise ValueError("Index out of bounds")
        self._list[index].display(window)