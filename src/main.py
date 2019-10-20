from src.ppm_utils import *

file_name = '../res/images/nt-P3.ppm'

generate_random_ppd('../res/images/rand.ppm', 800, 600)

# ppm_image = read_ppm_file(file_name)
ppm_image = read_ppm_file('../res/images/rand.ppm')

write_ppm_rgb_file('../res/images/new.ppm', ppm_image)
write_ppm_rgb_only_blue_file('../res/images/new_blue.ppm', ppm_image)
write_ppm_rgb_only_green_file('../res/images/new_green.ppm', ppm_image)
write_ppm_rgb_only_red_file('../res/images/new_red.ppm', ppm_image)

yuv_image = ppm_image.convert_to_yuv()

write_ppm_yuv_grayscale_file('../res/images/new_yuv_grayscale.ppm', yuv_image)
write_ppm_yuv_cb_file('../res/images/new_yuv_cb.ppm', yuv_image)
write_ppm_yuv_cr_file('../res/images/new_yuv_cr.ppm', yuv_image)

yuv_image = ppm_image.convert_to_yuv()
