from src.domain import YUVPixel, YUVImage, RGBImage, RGBPixel, Block


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
    y_blocks = []
    u_blocks = []
    v_blocks = []
    b = 0
    for y_pos in range(yuv_image.y_size):
        y_line = []
        u_line = []
        v_line = []
        for x_pos in range(yuv_image.x_size):
            y_line.append(yuv_image.pixels[y_pos * yuv_image.y_size + x_pos].y)
            u_line.append(yuv_image.pixels[y_pos * yuv_image.y_size + x_pos].u)
            v_line.append(yuv_image.pixels[y_pos * yuv_image.y_size + x_pos].v)
        b += 1
        y_blocks.append(y_line)
        u_blocks.append(u_line)
        v_blocks.append(v_line)
    a = len(y_blocks)
    return y_blocks, u_blocks, v_blocks


def divide_y_matrix(y_matrix):
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
