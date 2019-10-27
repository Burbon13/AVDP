from src.domain import YUVPixel, YUVImage, RGBImage, RGBPixel, Block


def read_ppm_file(file_name):
    """
    Reads a PPM file format image
    :param file_name: the path of the file
    :return: an instance of RGBImage
    """
    rgb_image = RGBImage(pixels=[])

    with open(file_name) as open_file:
        next(open_file)
        next(open_file)
        x_size, y_size = open_file.readline().split(' ')

        rgb_image.x_size = int(x_size)
        rgb_image.y_size = int(y_size)

        next(open_file)

        current_x, current_y = 1, 1

        while True:
            this_line = open_file.readline()
            if this_line == '':
                break

            red = int(this_line)
            green = int(open_file.readline())
            blue = int(open_file.readline())
            rgb_image.pixels.append(RGBPixel(red, green, blue, current_x, current_y))

            current_y += 1
            if current_y == rgb_image.y_size:
                current_y = 1
                current_x += 1

    return rgb_image


def write_ppm_rgb_file(file_name, image):
    """
    Writes an PPM image to file
    :param file_name: path for the new file
    :param image: an instance of PPMImage
    :return: None
    """
    with open(file_name, 'w+') as write_file:
        write_file.write('P3\n')
        write_file.write('# CREATOR: Most amazing Python 3.x program ever written\n')
        write_file.write(str(image.x_size) + ' ' + str(image.y_size) + '\n')
        write_file.write('255\n')
        for pixel in image.pixels:
            write_file.write(str(pixel.red) + '\n')
            write_file.write(str(pixel.green) + '\n')
            write_file.write(str(pixel.blue) + '\n')


def convert_rgb_pixel_to_yuv(rgb_pixel):
    y = int(0.299 * rgb_pixel.red + 0.587 * rgb_pixel.green + 0.114 * rgb_pixel.blue)
    u = int(128 - 0.1687 * rgb_pixel.red - 0.3312 * rgb_pixel.green + 0.5 * rgb_pixel.blue)
    v = int(128 + 0.5 * rgb_pixel.red - 0.4186 * rgb_pixel.green - 0.0813 * rgb_pixel.blue)
    return YUVPixel(y, u, v, rgb_pixel.x_pos, rgb_pixel.y_pos)


def convert_rgb_image_to_yuv(rgb_image):
    yuv_pixels = []
    for rgb_pixel in rgb_image.pixels:
        yuv_pixels.append(convert_rgb_pixel_to_yuv(rgb_pixel))
    return YUVImage(rgb_image.x_size, rgb_image.y_size, yuv_pixels)


def get_yuv_matrices(yuv_image):
    y_blocks = u_blocks = v_blocks = []

    for y_pos in range(yuv_image.y_size):
        for x_pos in range(yuv_image.x_size):
            y_blocks.append(yuv_image.pixels[y_pos * yuv_image.y_size + x_pos].y)
            u_blocks.append(yuv_image.pixels[y_pos * yuv_image.y_size + x_pos].u)
            v_blocks.append(yuv_image.pixels[y_pos * yuv_image.y_size + x_pos].v)

    return y_blocks, u_blocks, v_blocks
