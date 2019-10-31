from src.domain import YUVPixel, YUVImage, RGBImage, RGBPixel, Block
from math import cos, pi


# -------------------------------- LAB 1 - The encoder Part --------------------------------------

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

        current_x, current_y = 0, 0

        while True:
            this_line = open_file.readline()
            if this_line == '':
                break

            red = int(this_line)
            green = int(open_file.readline())
            blue = int(open_file.readline())
            rgb_image.pixels.append(RGBPixel(red, green, blue, current_x, current_y))

            current_x += 1
            if current_x == rgb_image.x_size:
                current_x = 0
                current_y += 1

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


def clamp_0_255_value(value):
    """
    Clamps the value between 0 and 255
    :param value: the value to be clamped
    :return: clamped value between 0 and 255
    """
    if value < 0:
        return 0
    if value > 255:
        return 255
    return value


def convert_rgb_pixel_to_yuv(rgb_pixel):
    """
    Converts an RGB pixel to an UIV pixel
    :param rgb_pixel: the pixel to be converted
    :return: the YUV pixel
    """
    y = clamp_0_255_value(int(0.257 * rgb_pixel.red + 0.504 * rgb_pixel.green + 0.098 * rgb_pixel.blue))
    v = clamp_0_255_value(int(128 - 0.148 * rgb_pixel.red - 0.291 * rgb_pixel.green + 0.439 * rgb_pixel.blue))
    u = clamp_0_255_value(int(128 + 0.439 * rgb_pixel.red - 0.368 * rgb_pixel.green - 0.071 * rgb_pixel.blue))
    return YUVPixel(y, u, v, rgb_pixel.x_pos, rgb_pixel.y_pos)


def convert_rgb_image_to_yuv(rgb_image):
    """
    Converts an RGB image to an UIV image
    :param rgb_image: the image to be converted
    :return: the YUV image
    """
    yuv_pixels = []
    for rgb_pixel in rgb_image.pixels:
        yuv_pixels.append(convert_rgb_pixel_to_yuv(rgb_pixel))
    return YUVImage(rgb_image.x_size, rgb_image.y_size, yuv_pixels)


def get_yuv_matrices(yuv_image):
    """
    Separates the Y,U and V components into separate matrices
    :param yuv_image: the image to be separated
    :return: (y matrix, u matrix, v matrix)
    """
    y_blocks = []
    u_blocks = []
    v_blocks = []
    for y_pos in range(yuv_image.y_size):
        y_line = []
        u_line = []
        v_line = []
        for x_pos in range(yuv_image.x_size):
            y_line.append(yuv_image.pixels[y_pos * yuv_image.x_size + x_pos].y)
            u_line.append(yuv_image.pixels[y_pos * yuv_image.x_size + x_pos].u)
            v_line.append(yuv_image.pixels[y_pos * yuv_image.x_size + x_pos].v)
        y_blocks.append(y_line)
        u_blocks.append(u_line)
        v_blocks.append(v_line)

    return y_blocks, u_blocks, v_blocks


def divide_y_matrix(y_matrix):
    """
    Divides the Y matrix into 8X8 pixel blocks
    :param y_matrix: the Y component matrix
    :return: a list with the blocks
    """
    y_blocks = []

    for y_pos in range(int(len(y_matrix) / 8)):
        for x_pos in range(int(len(y_matrix[0]) / 8)):
            block_values = []
            for y_matrix_pos in range(8):
                for x_matrix_pos in range(8):
                    block_values.append(y_matrix[y_pos * 8 + y_matrix_pos][x_pos * 8 + x_matrix_pos])
            y_blocks.append(Block(block_values, 'Y', x_pos, y_pos))

    return y_blocks


def divide_4_4_blocks(u_matrix, type):
    u_blocks = []

    for y_pos in range(int(len(u_matrix) / 8)):
        for x_pos in range(int(len(u_matrix[0]) / 8)):
            block_values = []
            for y_matrix_pos in range(4):
                for x_matrix_pos in range(4):
                    avg_value = int((
                                            u_matrix[y_pos * 8 + y_matrix_pos * 2][x_pos * 8 + x_matrix_pos * 2]
                                            +
                                            u_matrix[y_pos * 8 + y_matrix_pos * 2][x_pos * 8 + x_matrix_pos * 2 + 1]
                                            +
                                            u_matrix[y_pos * 8 + y_matrix_pos * 2 + 1][x_pos * 8 + x_matrix_pos * 2]
                                            +
                                            u_matrix[y_pos * 8 + y_matrix_pos * 2 + 1][x_pos * 8 + x_matrix_pos * 2 + 1]
                                    ) / 4)
                    block_values.append(avg_value)
            u_blocks.append(Block(block_values, type, x_pos, y_pos))

    return u_blocks


def print_blocks_list(block_list):
    print('[')
    for block in block_list:
        print(str(block))
    print(']')


def save_blocks_list(blocks_list, file_name):
    with open(file_name, 'w+') as write_file:
        for block in blocks_list:
            write_file.write(str(block) + '\n')


# -------------------------------- LAB 2 - The encoder Part --------------------------------------


def sigma(value):
    if value == 0:
        return 1 / 1.41421356237
    return 1


def calculate_discrete_cosine_transform_cell_value(u, v, block_8_8):
    cos_sum = 0

    for x in range(8):
        for y in range(8):
            cos_sum += block_8_8.get_value(x, y) * cos(((2 * x + 1) * u * pi) / 16) * cos(((2 * x + 1) * v * pi) / 16)

    return 0.25 * sigma(u) * sigma(v) * cos_sum


def discrete_cosine_transform_block(block_8_8):
    transformed_block = Block([], block_8_8.type_of_block, block_8_8.x_pos, block_8_8.y_pos)

    for y in range(8):
        for x in range(8):
            block_8_8.set_value(x, y, block_8_8.get_value(x, y) - 128)

    for y in range(8):
        for x in range(8):
            transformed_block.values.append(calculate_discrete_cosine_transform_cell_value(x, y, block_8_8))

    return transformed_block


quantization_matrix = [
    [6, 4, 4, 6, 10, 16, 20, 24],
    [5, 5, 6, 8, 10, 23, 24, 22],
    [6, 5, 6, 10, 16, 23, 28, 22],
    [6, 7, 9, 12, 20, 35, 32, 25],
    [7, 9, 15, 22, 27, 44, 41, 31],
    [10, 14, 22, 26, 32, 42, 45, 37],
    [20, 26, 31, 35, 41, 48, 48, 40],
    [29, 37, 38, 39, 45, 40, 41, 40]
]


def quantization():
    pass


# -------------------------------- LAB 2 - The decoder Part --------------------------------------

def inverse_quantization():
    pass


def inverse_discrete_cosine_transform_block():
    pass


# -------------------------------- LAB 1 - The decoder Part --------------------------------------

def un_divide_4_4_blocks(blocks_list, x_size, y_size):
    matrix = [[0] * x_size for _ in range(y_size)]

    for block in blocks_list:
        x_pos_block = block.x_pos * 8
        y_pos_block = block.y_pos * 8
        for index, value in enumerate(block.values):
            x_img = x_pos_block + int(index % 4) * 2
            y_img = y_pos_block + int(index / 4) * 2
            matrix[y_img][x_img] = value
            matrix[y_img + 1][x_img] = value
            matrix[y_img][x_img + 1] = value
            matrix[y_img + 1][x_img + 1] = value

    return matrix


def un_divide_y_blocks(y_blocks, x_size, y_size):
    matrix = [[0] * x_size for _ in range(y_size)]

    for block in y_blocks:
        x_pos_block = block.x_pos * 8
        y_pos_block = block.y_pos * 8
        for index, value in enumerate(block.values):
            x_img = x_pos_block + (index % 8)
            y_img = y_pos_block + int(index / 8)
            matrix[y_img][x_img] = value

    return matrix


def form_yuv_image_from_matrices(y_matrix, u_matrix, v_matrix, x_size, y_size):
    yuv_image = YUVImage(x_size, y_size, [])

    for y_pos in range(y_size):
        for x_pos in range(x_size):
            yuv_pixel = YUVPixel(y_matrix[y_pos][x_pos], u_matrix[y_pos][x_pos], v_matrix[y_pos][x_pos], x_pos, y_pos)
            yuv_image.pixels.append(yuv_pixel)

    return yuv_image


def convert_yuv_pixel_to_rgb(yuv_pixel):
    r = clamp_0_255_value(int(1.164 * (yuv_pixel.y - 16) + 2.018 * (yuv_pixel.u - 128)))
    g = clamp_0_255_value(int(1.164 * (yuv_pixel.y - 16) - 0.813 * (yuv_pixel.v - 128) - 0.391 * (yuv_pixel.u - 128)))
    b = clamp_0_255_value(int(1.164 * (yuv_pixel.y - 16) + 1.596 * (yuv_pixel.v - 128)))
    return RGBPixel(r, g, b, yuv_pixel.x_pos, yuv_pixel.y_pos)


def convert_yuv_image_to_rgb(yuv_image):
    rgb_pixels = []
    for yuv_pixel in yuv_image.pixels:
        rgb_pixels.append(convert_yuv_pixel_to_rgb(yuv_pixel))
    return YUVImage(yuv_image.x_size, yuv_image.y_size, rgb_pixels)


# -------------------------------------- EXTRA ----------------------------------------------

def write_ppm_rgb_only_red_file(file_name, image):
    with open(file_name, 'w+') as write_file:
        write_file.write('P3\n')
        write_file.write('# CREATOR: Most amazing Python 3.x program ever written\n')
        write_file.write(str(image.x_size) + ' ' + str(image.y_size) + '\n')
        write_file.write('255\n')
        for pixel in image.pixels:
            write_file.write(str(pixel.red) + '\n')
            write_file.write('0\n')
            write_file.write('0\n')


def write_ppm_rgb_only_green_file(file_name, image):
    with open(file_name, 'w+') as write_file:
        write_file.write('P3\n')
        write_file.write('# CREATOR: Most amazing Python 3.x program ever written\n')
        write_file.write(str(image.x_size) + ' ' + str(image.y_size) + '\n')
        write_file.write('255\n')
        for pixel in image.pixels:
            write_file.write('0\n')
            write_file.write(str(pixel.green) + '\n')
            write_file.write('0\n')


def write_ppm_rgb_only_blue_file(file_name, image):
    with open(file_name, 'w+') as write_file:
        write_file.write('P3\n')
        write_file.write('# CREATOR: Most amazing Python 3.x program ever written\n')
        write_file.write(str(image.x_size) + ' ' + str(image.y_size) + '\n')
        write_file.write('255\n')
        for pixel in image.pixels:
            write_file.write('0\n')
            write_file.write('0\n')
            write_file.write(str(pixel.blue) + '\n')


def write_ppm_yuv_grayscale_file(file_name, image):
    with open(file_name, 'w+') as write_file:
        write_file.write('P3\n')
        write_file.write('# CREATOR: Most amazing Python 3.x program ever written\n')
        write_file.write(str(image.x_size) + ' ' + str(image.y_size) + '\n')
        write_file.write('255\n')
        for pixel in image.pixels:
            write_file.write(str(pixel.y) + '\n')
            write_file.write(str(pixel.y) + '\n')
            write_file.write(str(pixel.y) + '\n')


def write_ppm_yuv_cb_file(file_name, image):
    with open(file_name, 'w+') as write_file:
        write_file.write('P3\n')
        write_file.write('# CREATOR: Most amazing Python 3.x program ever written\n')
        write_file.write(str(image.x_size) + ' ' + str(image.y_size) + '\n')
        write_file.write('255\n')
        for pixel in image.pixels:
            write_file.write(str(pixel.u) + '\n')
            write_file.write(str(pixel.u) + '\n')
            write_file.write(str(pixel.u) + '\n')


def write_ppm_yuv_cr_file(file_name, image):
    with open(file_name, 'w+') as write_file:
        write_file.write('P3\n')
        write_file.write('# CREATOR: Most amazing Python 3.x program ever written\n')
        write_file.write(str(image.x_size) + ' ' + str(image.y_size) + '\n')
        write_file.write('255\n')
        for pixel in image.pixels:
            write_file.write(str(pixel.v) + '\n')
            write_file.write(str(pixel.v) + '\n')
            write_file.write(str(pixel.v) + '\n')
