
class FlyingObject(object):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.can_clear = False
        self.current_image = None

    def load_resources(self):
        pass

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def get_width(self):
        if self.current_image is not None:
            return self.current_image.get_width()
        else:
            return 0

    def get_height(self):
        if self.current_image is not None:
            return self.current_image.get_width()
        else:
            return 0

    def blit_me(self, screen):
        x = self.x
        y = self.y
        img = self.current_image
        screen.blit(img, (x, y))

    def get_rect(self):
        rect = self.current_image.get_rect()
        rect.left = self.x
        rect.top = self.y
        return rect

    def update_image(self):
        pass

    def update_position(self):
        pass
