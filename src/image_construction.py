from PIL import Image
import numpy as np

CARRY_IMAGE_FILE = "Images/canyon.png"
MESG_IMAGE_FILE = "Images/hello.png"

def to_array(img):
    image = Image.open(img)

    image_arr = np.array(image)

    shape = image_arr.shape

    flat_arr = image_arr.ravel()

    return flat_arr, shape

def to_image(arr, img_shape):
    matrix = np.matrix(arr)

    reform_matrix = np.asarray(matrix).reshape(img_shape)

    new_img = Image.fromarray(reform_matrix, 'RGB')

    return new_img

def main():
    # #carry_arr = to_array(CARRY_IMAGE_FILE)
    # mesg = Image.open(MESG_IMAGE_FILE)

    # mesg_arr_pixels = list(mesg.getdata())
    # #print(mesg_arr_pixels)
    # #mesg_arr = np.array(mesg_arr_pixels, dtype=np.uint8)

    # new_img = Image.new('1', (mesg.size[0], mesg.size[1]))

    # new_img.putdata(mesg_arr_pixels)

    # #reconstruct_image = to_image(mesg_arr_pixels, mesg.size[0], mesg.size[1])
    mesg = MESG_IMAGE_FILE 

    mesg_arr = to_array(mesg)

    new_image = to_image(mesg_arr[0], mesg_arr[1])

    new_image.show()

if __name__ == "__main__":
    main()
