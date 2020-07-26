from abc import ABC, abstractmethod
import math
import pygame

class GameObject(ABC):
    def __init__(self, name='Game Object', x=0, y=0, width=0, height=0, image=None):
        """
        Constructor of GameObject

        :param name: Identification of the object for listening events
        :param x: x position of the center of the object
        :param y: y position of the center of the object
        :param width: Width of the object
        :param height: Height of the object
        :param image: Surface to be displayed or None
        :raise ValueError: Negative dimension values
        """
        if height < 0 or width < 0:
            raise ValueError("Dimension values must not be negative")
        self._name = name
        self._x = x
        self._y = y
        self._height = height
        self._width = width
        # Scale image if it doesn't match object's size
        if image is not None and (image.get_width() != width or image.get_height() != height):
            image = pygame.transform.smoothscale(image, (width, height))
        self._image = image

    @property
    def name(self):
        """Getter of name attribute"""
        return self._name

    @property
    def x(self):
        """Getter of x attribute"""
        return self._x

    @x.setter
    def x(self, x):
        """Setter of x attribute"""
        self._x = x

    @property
    def y(self):
        """Getter of y attribute"""
        return self._y

    @y.setter
    def y(self, y):
        """Setter of y attribute"""
        self._y = y
    
    @property
    def height(self):
        """Getter of height attribute"""
        return self._height

    @property
    def width(self):
        """Getter of width attribute"""
        return self._width

    @property
    def image(self):
        """Getter of image attribute"""
        return self._image

    def distance(self, obj) -> float:
        """
        Calculates the distance from the center of this object to another

        :param obj: Another game object
        """
        return math.sqrt(((self.x - obj.x) ** 2) + ((self.y - obj.y) ** 2))

    def display(self, window):
        """
        Display object on window

        :param window: Window surface to display the object
        """
        if self.image is not None:
            window.blit(self.image, (self.x - self.width//2, self.y - self.height//2))
    
    @abstractmethod
    def max_radius(self) -> float:
        """
        Radius of the circumference that circumscribe the object
        
        :return:
        Float: Radius
        """
        ...

    @abstractmethod
    def collision(self, obj) -> bool:
        """
        Test if two game objects collided
        
        :param obj: Another object to test collision
        :return:
        Boolean: Collision
        """
        ...


class CircularObject(GameObject):
    def __init__(self, name='Circle', x=0, y=0, radius=0, image=None):
        """
        Constructor of CircularObject

        :param name: Identification of the object for listening events
        :param x: x position of the center circle
        :param y: y position of the center circle
        :param radius: Radius of the circle
        :param image: Surface to be displayed or None
        """
        super().__init__(name, x, y, radius*2, radius*2, image)
        self._radius = radius

    def max_radius(self) -> float:
        """Get the radius of the circle"""
        return self._radius

    def collision(self, obj: GameObject) -> bool:
        """
        Test if two game objects collided
        
        :param GameObject obj: Another object to test collision
        :return:
        Boolean: Collision
        """
        circular_colision = self.distance(obj) < (self.max_radius() + obj.max_radius())
        if isinstance(obj, CircularObject):
            return circular_colision
        else:
            distance_x = abs(self.x - obj.x)
            distance_y = abs(self.y - obj.y)
            retangular_colision = distance_x < (self.width + obj.width)/2 and distance_y < (self.height + obj.height)/2
            return circular_colision and retangular_colision

class RectangularObject(GameObject):
    def __init__(self, name='Rectangle', x=0, y=0, width=0, height=0, image=None):
        """
        Constructor of RectangularObject

        :param name: Identification of the object for listening events
        :param x: x position of the center of the rectangle
        :param y: y position of the center of the rectangle
        :param width: Width of the rectangle
        :param height: Height of the rectangle
        :param image: Surface to be displayed or None
        """
        super().__init__(name, x, y, width, height, image)

    def max_radius(self) -> float:
        """
        Radius of the circumference that circumscribe the rectangle
        
        :return:
        Float: Radius
        """
        return math.sqrt((self.width/2) ** 2 + (self.height/2) ** 2)

    def collision(self, obj: GameObject) -> bool:
        """
        Test if two game objects collided
        
        :param GameObject obj: Another object to test collision
        :return:
        Boolean: Collision
        """
        distance_x = abs(self.x - obj.x)
        distance_y = abs(self.y - obj.y)
        retangular_colision = distance_x < (self.width + obj.width)/2 and distance_y < (self.height + obj.height)/2
        if isinstance(obj, RectangularObject):
            return retangular_colision
        else:
            circular_colision = self.distance(obj) < (self.max_radius() + obj.max_radius())
            return retangular_colision and circular_colision