from PIL import Image
import numpy as np
import image_construction as construct
import image_compare as compare

THRESHOLD_CONSTANT = 4 #Number used to scale secret image to test if carry image can contain secret image
# CARRY_IMAGE_FILE = "Images/canyon1.png"
# MESG_IMAGE_FILE = "Images/hello.png"

CARRY_IMAGE_FILE = "C:/Users/cjmal/OneDrive/Desktop/Fall 2019/Crypto/Project/canyon.png"
MESG_IMAGE_FILE = "C:/Users/cjmal/OneDrive/Desktop/Fall 2019/Crypto/Project/hello.png"

def integer_to_binary(value):
    '''
    Convert R or G or B pixel values from integer to binary
    INPUT: An integer tuple (e.g. (220))
    OUTPUT: A string tuple (e.g. ("00101010"))
    '''
    return ('{0:08b}'.format(value))

def binary_to_integer(binary):
    '''
    Convert R or G or B pixel values from binary to integer.
    INPUT: A string tuple (e.g. ("00101010"))
    OUTPUT: Return an int tuple (e.g. (220))
    '''   
    return (int(binary, 2))

def merge_rgb(rgb1, rgb2):
    '''
    Merge two R or G or B pixels using 4 least significant bits.
    INPUT: A string tuple (e.g. ("00101010")),
           Another string tuple (e.g. ("00101010"))
    OUTPUT: An integer tuple with the two RGB values merged 00100010
    '''   
    rgb = (rgb1[:4] + rgb2[:4])
    return rgb

def mergeImages(carryImage_path, mesgImage_path):
    '''
    Merge two images. The msegImage will be merged into the carryImage.
    INPUT: carry and message image path
    OUTPUT: A new merged image.
    '''   
    carry_image = Image.open(carryImage_path)
    message_image = Image.open(mesgImage_path)
    
    # Ensure carry image is larger than message image
    # if not compare.img_cmp_arr(carryImage_path,mesgImage_path):
    #    raise ValueError('Carry image size is lower than message image size!')
    
    # Create a new image that will be outputted
    new_image = Image.new(carry_image.mode, carry_image.size)
    new_image_arr = construct.to_array(new_image)
    
    carry_arr = construct.to_array(carry_image)
    mesg_arr = construct.to_array(message_image)
    
    for i in range(len(carry_arr[0])):
        rgb1 = integer_to_binary(carry_arr[0][i])

        # Use a black pixel as default
        rgb2 = integer_to_binary((0))

        # Check if the pixel count is valid for the second image
        if i < len(mesg_arr[0]):
            rgb2 = integer_to_binary(mesg_arr[0][i])

        # Merge the two pixels and convert it to a integer tuple
        rgb = merge_rgb(rgb1, rgb2)

        new_image_arr[0][i] = binary_to_integer(rgb)
    
    new_image = construct.to_image(new_image_arr[0], new_image_arr[1])
    
    return new_image

def main():
    send_image = mergeImages(CARRY_IMAGE_FILE, MESG_IMAGE_FILE)
    send_image.show()

if __name__ == "__main__":
    main()
