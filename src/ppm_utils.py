from src.domain import RGBImage, RGBPixel


def read_ppm_file(file_name):
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
    with open(file_name, 'w+') as write_file:
        write_file.write('P3\n')
        write_file.write('# CREATOR: Most amazing Python 3.x program ever written\n')
        write_file.write(str(image.x_size) + ' ' + str(image.y_size) + '\n')
        write_file.write('255\n')
        for pixel in image.pixels:
            write_file.write(str(pixel.red) + '\n')
            write_file.write(str(pixel.green) + '\n')
            write_file.write(str(pixel.blue) + '\n')


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
