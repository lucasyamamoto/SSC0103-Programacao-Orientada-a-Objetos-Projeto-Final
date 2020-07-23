class Apple:
    def __init__(self, sprite, pos, num, font):
        self.sprite = sprite
        self.pos = pos
        self.font = font
        self.num = num
        self.text = self.font.render(str(num), 1, (255, 255, 255))

    def change(self, pos, num):
        self.pos = pos
        self.num = num
        self.text = self.font.render(str(num), 1, (255, 255, 255))

    def drawn(self, screen, size):
        screen.blit(self.sprite, (self.pos[0] * size, self.pos[1] * size))
        screen.blit(self.text, (self.pos[0] * size, self.pos[1] * size))
