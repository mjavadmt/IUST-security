import cv2
import numpy as np
import enchant


def pixel2binary(pixel):
    if type(pixel) == bytes or type(pixel) == np.ndarray:
        return [format(i, "08b") for i in pixel]
    else:
        raise TypeError("Input type not supported")


def convert_pixel_to_lsb(image):
    lsbs = []
    for pixel_list in image:
        for pixel in pixel_list:
            r, g, b = pixel2binary(pixel)
            all_binaries = list(r + g + b)
            lsbs.extend(all_binaries)
    return lsbs


def encode_hidden_to_main(main_image_, hidden_image_):
    lsbs = convert_pixel_to_lsb(hidden_image_)
    counter = 0
    for enumerator_1, pixel_list in enumerate(main_image_):
        for enumerator_2, pixel in enumerate(pixel_list):
            r, g, b = pixel2binary(pixel)
            r = r[:len(r) - 1] + lsbs[counter]
            counter += 1
            g = g[:len(g) - 1] + lsbs[counter]
            counter += 1
            b = b[:len(b) - 1] + lsbs[counter]
            counter += 1
            r = int(r, 2)
            g = int(g, 2)
            b = int(b, 2)
            main_image_[enumerator_1][enumerator_2] = (r, g, b)
    return main_image_


def decode_hidden_from_main(image):
    values = []
    blank_image = np.zeros((256, 256, 3), np.uint8)
    for enumerator_1, pixel_list in enumerate(image):
        for enumerator_2, pixel in enumerate(pixel_list):
            r, g, b = pixel2binary(pixel)
            values.extend([r[-1], g[-1], b[-1]])

    for i in range(256 * 256):
        r = values[i * 24: i * 24 + 8]
        g = values[i * 24 + 8: i * 24 + 16]
        b = values[i * 24 + 16: i * 24 + 24]
        r = int("".join(r), 2)
        g = int("".join(g), 2)
        b = int("".join(b), 2)
        index_row = i // 256
        col_row = i % 256
        blank_image[index_row, col_row] = (r, g, b)
    return blank_image


def multiply_function(*params):
    m = 1
    for i in params:
        m *= i
    return m


def convert_text_to_bits(text):
    bits = []
    for char in text:
        ascii_code = ord(char)
        binary = format(ascii_code, "08b")
        bits.extend(list(binary))
    return bits


def encode_hidden_text_to_image(main_image_, text):
    text_bits = convert_text_to_bits(text)
    main_image_lsb_counts = multiply_function(*main_image_.shape)
    remaining_bits = ['0'] * (main_image_lsb_counts - len(text_bits))
    text_bits.extend(remaining_bits)
    counter = 0
    for enumerator_1, pixel_list in enumerate(main_image_):
        for enumerator_2, pixel in enumerate(pixel_list):
            r, g, b = pixel2binary(pixel)
            r = r[:len(r) - 1] + text_bits[counter]
            counter += 1
            g = g[:len(g) - 1] + text_bits[counter]
            counter += 1
            b = b[:len(b) - 1] + text_bits[counter]
            counter += 1
            r = int(r, 2)
            g = int(g, 2)
            b = int(b, 2)
            main_image_[enumerator_1][enumerator_2] = (r, g, b)
    return main_image_


def decode_text_from_image(image):
    values = []
    hidden_string = ""
    for enumerator_1, pixel_list in enumerate(image):
        for enumerator_2, pixel in enumerate(pixel_list):
            r, g, b = pixel2binary(pixel)
            values.extend([r[-1], g[-1], b[-1]])

    for idx in range(0, len(values), 8):
        char = int("".join(values[idx:idx + 8]), 2)
        char = chr(char)
        if char != '' and char != '\x00':
            hidden_string += char
    return hidden_string


if __name__ == "__main__":
    is_image = False
    main_image = cv2.imread("main_image.jpg")
    if is_image:
        hidden_image = cv2.imread("hidden_image.jpg")

        encoded_image = encode_hidden_to_main(main_image, hidden_image)
        cv2.imwrite("merged.jpg", encoded_image)
        decoded_image = decode_hidden_from_main(encoded_image)
        cv2.imwrite("splitted.jpg", decoded_image)

    else:
        hidden_text = "you're nahh mah"

        encoded_image_with_text = encode_hidden_text_to_image(main_image, hidden_text)
        decoded_text = decode_text_from_image(encoded_image_with_text)
        print(decoded_text)
        d = enchant.Dict("en_US")
        if 0.5 <= np.array([d.check(i) for i in decoded_text.split()]).mean():
            print("our text is meaningful")
        else:
            print("our text is meaningless")
