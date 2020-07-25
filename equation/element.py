from abc import ABC, abstractmethod
import math
import pygame

class GameObject(ABC):
    def __init__(self, name='Game Object', x=0, y=0, height=0, width=0, image=None):
        if height < 0 or width < 0:
            raise ValueError("Dimension values must not be negative")
        self._name = name
        self._x = x
        self._y = y
        self._height = height
        self._width = width
        # Scale image if it doesn't match object's size
        if image is not None and (image.get_width != width or image.get_height != height):
            image = pygame.transform.smoothscale(image, (width, height))
        self._image = image

    @property
    def name(self):
        return self._name

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
    
    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def image(self):
        return self._image

    def distance(self, obj) -> float:
        return math.sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2)

    @abstractmethod
    def max_radius(self) -> float:
        ...

    @abstractmethod
    def collision(self, obj) -> bool:
        ...

class CircularObject(GameObject):
    def __init__(self, name='Circle', x=0, y=0, radius=0, image=None):
        super().__init__(name, x, y, radius, radius, image)
        self._radius = radius

    def max_radius(self) -> float:
        return self._radius

    def collision(self, obj: GameObject) -> bool:
        circular_colision = self.distance(obj) < (self.max_radius() + obj.max_radius())
        if isinstance(obj, CircularObject):
            return circular_colision
        else:
            distance_x = abs(self.x - obj.x)
            distance_y = abs(self.y - obj.y)
            retangular_colision = distance_x < (self.width + obj.width) and distance_y < (self.height + obj.height)
            return circular_colision and retangular_colision

class RectangularObject(GameObject):
    def __init__(self, name='Rectangle', x=0, y=0, height=0, width=0, image=None):
        super().__init__(name, x, y, height, width, image)

    def max_radius(self) -> float:
        return math.sqrt(self.width ** 2 + self.height ** 2)

    def collision(self, obj: GameObject) -> bool:
        distance_x = abs(self.x - obj.x)
        distance_y = abs(self.y - obj.y)
        retangular_colision = distance_x < (self.width + obj.width) and distance_y < (self.height + obj.height)
        if isinstance(obj, RectangularObject):
            return retangular_colision
        else:
            circular_colision = self.distance(obj) < (self.max_radius() + obj.max_radius())
            return retangular_colision and circular_colision