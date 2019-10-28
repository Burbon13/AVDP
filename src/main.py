from src.ppm_utils import *

file_name = '../res/images/nt-P3.ppm'

# generate_random_ppd('../res/images/rand.ppm', 1920, 1080)

print('Reading PPM file')
rgb_image = read_ppm_file(file_name)

print('Converting image from RGB to YUV')
yuv_image = convert_rgb_image_to_yuv(rgb_image)

print('Separating YUV components into different matrices')
y_matrix, u_matrix, v_matrix = get_yuv_matrices(yuv_image)

print('Dividing Y matrix into blocks')
y_blocks = divide_y_matrix(y_matrix)

u_blocks = divide_4_4_blocks(u_matrix, 'U')

v_blocks = divide_4_4_blocks(v_matrix, 'V')

print('Y blocks')
# print_blocks_list(y_blocks)
print('Writing Y blocks into file')
save_blocks_list(y_blocks, '../res/images/processing/y_blocks')

print('U blocks')
# print_blocks_list(y_blocks)
print('Writing U blocks into file')
save_blocks_list(u_blocks, '../res/images/processing/u_blocks')

print('V blocks')
# print_blocks_list(y_blocks)
print('Writing V blocks into file')
save_blocks_list(v_blocks, '../res/images/processing/v_blocks')