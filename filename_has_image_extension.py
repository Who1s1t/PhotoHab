def filename_has_image_extension(filename):
    valid_img_extensions = \
        ['bmp', 'gif', 'jpg', 'jpeg', 'png', 'pbm', 'pgm', 'ppm', 'xbm', 'xpm']
    filename = filename.lower()
    extension = filename[-3:]
    four_char = filename[-4:]
    if extension in valid_img_extensions or four_char in valid_img_extensions:
        return True
    else:
        return False
