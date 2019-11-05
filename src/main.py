from src.ppm_utils import *

file_name = '../res/images/nt-P3.ppm'
# file_name = '../res/images/best.ppm'
# file_name = '../res/images/craciunelul.ppm'
# file_name = '../res/images/text.ppm'
DEBUG = False

# generate_random_ppd('../res/images/rand.ppm', 1920, 1080)

# -------------------------------- LAB 1 - The encoder Part --------------------------------------
print('---- ENCODER PART ----')

print('Reading PPM file')
rgb_image = read_ppm_file(file_name)

x_size = rgb_image.x_size
y_size = rgb_image.y_size

print('Converting image from RGB to YUV')
yuv_image = convert_rgb_image_to_yuv(rgb_image)

if DEBUG:
    print('DEBUG: Intermediary YUV image printing...')
    write_ppm_yuv_grayscale_file('../res/images/processing/grayscale_encoding.ppm', yuv_image)
    write_ppm_yuv_cb_file('../res/images/processing/U_encoding.ppm', yuv_image)
    write_ppm_yuv_cr_file('../res/images/processing/V_encoding.ppm', yuv_image)

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

# -------------------------------- LAB 2 - The encoder Part --------------------------------------

print('Transforming v blocks from 4X4 to 8X8')
enlarged_v_blocks = from_4_4_to_8_8(v_blocks, x_size, y_size)
print('Transforming u blocks from 4X4 to 8X8')
enlarged_u_blocks = from_4_4_to_8_8(u_blocks, x_size, y_size)

print('Applying discrete cosine transform and quantization on Y blocks')
cosine_quantized_transformed_y_blocks = []
for block in y_blocks:
    cosined_block = discrete_cosine_transform_block(block)
    quantization(cosined_block)
    cosine_quantized_transformed_y_blocks.append(cosined_block)

print('Applying discrete cosine transform and quantization on U blocks')
cosine_quantized_transformed_u_blocks = []
for block in enlarged_u_blocks:
    cosined_block = discrete_cosine_transform_block(block)
    quantization(cosined_block)
    cosine_quantized_transformed_u_blocks.append(cosined_block)

print('Applying discrete cosine transform and quantization on V blocks')
cosine_quantized_transformed_v_blocks = []
for block in enlarged_v_blocks:
    cosined_block = discrete_cosine_transform_block(block)
    quantization(cosined_block)
    cosine_quantized_transformed_v_blocks.append(cosined_block)

# -------------------------------- LAB 3 - The encoder Part --------------------------------------


# -------------------------------- LAB 3 - The decoder Part --------------------------------------


# -------------------------------- LAB 2 - The decoder Part --------------------------------------

print('---- DECODER PART ----')

print('Undoing discrete cosine transform and quantization on Y blocks')
undo_cosine_quantized_transformed_y_blocks = []
for block in cosine_quantized_transformed_y_blocks:
    inverse_quantization(block)
    undo_cosine_quantized_transformed_y_blocks.append(inverse_discrete_cosine_transform_block(block))

print('Undoing discrete cosine transform and quantization on U blocks')
undo_cosine_quantized_transformed_u_blocks = []
for block in cosine_quantized_transformed_u_blocks:
    inverse_quantization(block)
    undo_cosine_quantized_transformed_u_blocks.append(inverse_discrete_cosine_transform_block(block))

print('Undoing discrete cosine transform and quantization on V blocks')
undo_cosine_quantized_transformed_v_blocks = []
for block in cosine_quantized_transformed_v_blocks:
    inverse_quantization(block)
    undo_cosine_quantized_transformed_v_blocks.append(inverse_discrete_cosine_transform_block(block))

# -------------------------------- LAB 1 - The decoder Part --------------------------------------

print('Un-dividing V blocks')
# decoded_v_matrix = un_divide_4_4_blocks(v_blocks, x_size, y_size)
decoded_v_matrix = un_divide_y_blocks(undo_cosine_quantized_transformed_v_blocks, x_size, y_size)

print('Un-dividing U blocks')
# decoded_u_matrix = un_divide_4_4_blocks(u_blocks, x_size, y_size)
decoded_u_matrix = un_divide_y_blocks(undo_cosine_quantized_transformed_u_blocks, x_size, y_size)

print('Un-dividing Y blocks')
decoded_y_matrix = un_divide_y_blocks(undo_cosine_quantized_transformed_y_blocks, x_size, y_size)

print('Forming YUV image from matrices')
decoded_yuv_image = form_yuv_image_from_matrices(decoded_y_matrix, decoded_u_matrix, decoded_v_matrix, x_size, y_size)

if DEBUG:
    print('DEBUG: Intermediary YUV image printing...')
    write_ppm_yuv_grayscale_file('../res/images/processing/grayscale_decoding.ppm', decoded_yuv_image)
    write_ppm_yuv_cb_file('../res/images/processing/U_decoding.ppm', decoded_yuv_image)
    write_ppm_yuv_cr_file('../res/images/processing/V_decoding.ppm', decoded_yuv_image)

print('Converting YUV image to RGB')
decoded_rgb_image = convert_yuv_image_to_rgb(decoded_yuv_image)

print('Saving converted RGB image')
write_ppm_rgb_file('../res/images/processing/decoded_rgb.ppm', decoded_rgb_image)

print('DONE! <3')
