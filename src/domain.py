class RGBPixel:
    def __init__(self, red=None, green=None, blue=None, x_pos=None, y_pos=None):
        self.red = red
        self.green = green
        self.blue = blue
        self.x_pos = x_pos
        self.y_pos = y_pos

    def convert_to_yuv(self):
        y = int(0.299 * self.red + 0.587 * self.green + 0.114 * self.blue)
        u = int(128 - 0.1687 * self.red - 0.3312 * self.green + 0.5 * self.blue)
        v = int(128 + 0.5 * self.red - 0.4186 * self.green - 0.0813 * self.blue)
        return YUVPixel(y, u, v, self.x_pos, self.y_pos)


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

    def convert_to_yuv(self):
        yuv_pixels = []
        for rgb_pixel in self.pixels:
            yuv_pixels.append(rgb_pixel.convert_to_yuv())
        return YUVImage(self.x_size, self.y_size, yuv_pixels)


class YUVImage:
    def __init__(self, x_size=None, y_size=None, pixels=None):
        self.x_size = x_size
        self.y_size = y_size
        self.pixels = pixels
