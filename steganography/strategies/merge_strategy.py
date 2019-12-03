from PIL import Image
from steganography.utilities.img_manipulation import to_array, to_image, merge_pixels
from steganography.utilities.img_compare import img_cmp_arr
from steganography.utilities.bits import integer_to_binary, binary_to_integer
import random


# TODO: Remove?
def merge_images(carry_image_path, mesg_image_path, secret_key):
    """
    Merge two images. The msegImage will be merged into the carryImage.
    INPUT: carry and message image path
    OUTPUT: A new merged image.
    """
    carry_image = Image.open(carry_image_path)
    message_image = Image.open(mesg_image_path)

    # Ensure carry image is larger than message image
    if not img_cmp_arr(carry_image_path, mesg_image_path):
        raise ValueError('Carry image size is lower than message image size!')

    # Create a new image that will be outputted
    new_image = Image.new(carry_image.mode, carry_image.size)
    new_image_arr = to_array(new_image)

    carry_arr = to_array(carry_image)
    mesg_arr = to_array(message_image)

    for i in range(len(carry_arr[0])):
        new_image_arr[0][i] = carry_arr[0][i]

    random.seed(secret_key)
    for i in range(len(mesg_arr[0])):
        # Check if the pixel count is valid for the second image
        if i < len(mesg_arr[0]):
            random_pixel = random.randint(0, len(carry_arr[0]) - 1)
            carry_pixel = integer_to_binary(carry_arr[0][random_pixel])
            mesg_pixel = integer_to_binary(mesg_arr[0][i])

            # Merge the two pixels and convert it to a integer tuple
            merged_pixel = merge_pixels(carry_pixel, mesg_pixel)

            new_image_arr[0][random_pixel] = binary_to_integer(merged_pixel)

    new_image = to_image(new_image_arr[0], new_image_arr[1])
    new_image.save('./resources/merged.png')

    return new_image


def extract_hidden_image(merged_image_path, mesg_image_path, secret_key):
    """
    Unmerge an image.
    INPUT: The path to the input image.
    OUTPUT: The extracted hidden image.
    """
    merged_img = Image.open(merged_image_path)
    message_image = Image.open(mesg_image_path)

    # Create the new image and load the pixel map
    new_image = Image.new(message_image.mode, message_image.size)
    new_image_arr = to_array(new_image)

    # Tuple used to store the image original size
    original_size = len(new_image_arr[0])

    merged_arr = to_array(merged_img)
    mesg_arr = to_array(message_image)

    random.seed(secret_key)
    for i in range(len(mesg_arr[0])):
        random_pixel = random.randint(0, len(merged_arr[0]) - 1)
        binaryValue = integer_to_binary(merged_arr[0][random_pixel])

        # Extract the last 4 bits (corresponding to the hidden image)
        # Concatenate 4 zero bits because we are working with 8 bit values
        extractedBinary = (binaryValue[4:] + "0000")

        # Convert it to an integer tuple

        extractedInteger = binary_to_integer(extractedBinary)
        if extractedInteger != 0:
            new_image_arr[0][i] = extractedInteger
            original_size = (i + 1)

    hidden_image = to_image(new_image_arr[0], new_image_arr[1])

    hidden_image.save('./resources/unmerged.png')

    return hidden_image