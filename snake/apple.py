class Apple:
    """
    This class os reponsible for the cration and update of the Apple object
    """
    def __init__(self, sprite, pos, num, font):
        self.sprite = sprite
        self.pos = pos
        self.font = font
        self.num = num
        self.text = self.font.render(str(num), 1, (255, 255, 255))

    def change(self, pos, num):
        """
        This method create a new number and position to the apple
        :param pos: random int
        :param num: random int
        :return:
        """
        self.pos = pos
        self.num = num
        self.text = self.font.render(str(num), 1, (255, 255, 255))

    def drawn(self, screen, size):
        """
        This method drawn the apple on the pygames screen
        :param screen: pygames screen
        :param size: sprite size
        :return:
        """
        screen.blit(self.sprite, (self.pos[0] * size, self.pos[1] * size))
        screen.blit(self.text, (self.pos[0] * size, self.pos[1] * size))
