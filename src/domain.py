class RGBPixel:
    def __init__(self, red=None, green=None, blue=None, x_pos=None, y_pos=None):
        self.red = red
        self.green = green
        self.blue = blue
        self.x_pos = x_pos
        self.y_pos = y_pos


class YUVPixel:
    def __init__(self, y=None, u=None, v=None, x_pos=None, y_pos=None):
        self.y = y
        self.u = u
        self.v = v
        self.x_pos = x_pos
        self.y_pos = y_pos


class RGBImage:
    def __init__(self, x_size=None, y_size=None, pixels=None):
        self.x_size = x_size
        self.y_size = y_size
        self.pixels = pixels


class YUVImage:
    def __init__(self, x_size=None, y_size=None, pixels=None):
        self.x_size = x_size
        self.y_size = y_size
        self.pixels = pixels


class Block:
    def __init__(self, values, type_of_block, x_pos, y_pos):
        self.values = values
        self.type_of_block = type_of_block
        self.x_pos = x_pos
        self.y_pos = y_pos

    def get_value(self, x, y):
        return self.values[8 * y + x]

    def set_value(self, x, y, value):
        self.values[8 * y + x] = value

    def __str__(self):
        return f'Type: {self.type_of_block}; x: {self.x_pos}; y: {self.y_pos}; values: {self.values}'

    def __repr__(self):
        return f'Type: {self.type_of_block}; x: {self.x_pos}; y: {self.y_pos}; values: {self.values}'
