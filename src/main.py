from src.ppm_utils import *

file_name = '../res/images/nt-P3.ppm'

# generate_random_ppd('../res/images/rand.ppm', 1920, 1080)

rgb_image = read_ppm_file(file_name)

yuv_image = convert_rgb_image_to_yuv(rgb_image)

y_matrix, u_matrix, v_matrix = get_yuv_matrices(yuv_image)

# y_blocks = divide_y_matrix(y_matrix)
#
# u_blocks = divide_u_blocks(u_matrix)
#
# v_blocks = divide_v_blocks(v_matrix)
#
# store_blocks_list(y_blocks, '../res/images/processing/yblocks')
# store_blocks_list(u_blocks, '../res/images/processing/ublocks')
# store_blocks_list(v_blocks, '../res/images/processing/vblocks')
#
# print('Y blocks list')
# print(y_blocks)
# print('U blocks list')
# print(u_blocks)
# print('V blocks list')
# print(v_blocks)