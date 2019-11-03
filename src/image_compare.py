from PIL import Image

THRESHOLD_CONSTANT = 5 #Number used to scale secret image to test if carry image can contain secret image
# CARRY_IMAGE_FILE = "../Images/canyon.png"
# MESG_IMAGE_FILE = "../Images/hello.png"

#This tests x and y values of THRESHOLD_CONSTANT * Message
#This is good for presentation as in, user knows what dimensions the picture has to be
def img_cmp_dimension(carry, message):

    carry_im = Image.open(carry)
    mesg_im = Image.open(message)

    carr_width = carry_im.size[0]   #x
    carr_length = carry_im.size[1]  #y

    mesg_width = mesg_im.size[0]    #x
    mesg_length = mesg_im.size[1]   #y

    #We can increase or decrease our threshold constant
    if (carr_width > (THRESHOLD_CONSTANT*(mesg_width)) and 
        carr_length > (THRESHOLD_CONSTANT*(mesg_length))):
        return True
    else:
        return False

#This tests each image in array format
#Provides feedback given lengths of array
#Good since dimensions doesn't really matter when hiding an image,
#   we need to know if we have enough pixels to hide the image, not necessarily
#   the dimensions
def img_cmp_arr(carry, message):

    carry_im = Image.open(carry)
    mesg_im = Image.open(message)

    carry_arr = list(carry_im.getdata())
    mesg_arr = list(mesg_im.getdata())

    carry_size = len(carry_arr)
    mesg_size = len(mesg_arr)

    if (carry_size > (THRESHOLD_CONSTANT*(mesg_size))):
        return True
    else:
        return False

#specifies required dimensions of message given carry (based on THRESHOLD_CONSTANT)
def req_mesg_size(carry):

    carry_img = Image.open(carry)

    carry_img_size = carry_img.size
    req_message_size = (carry_img.size[0]/THRESHOLD_CONSTANT, carry_img.size[1]/THRESHOLD_CONSTANT)

    #print(carry_img.size)
    print("Carry Image size given: ", carry_img_size)
    print("Required message size given carry: ", req_message_size)


#For Testing Purposes
# def main():
#     print(img_cmp_dimension(CARRY_IMAGE_FILE, MESG_IMAGE_FILE)) #dimensional testing
#     print(img_cmp_arr(CARRY_IMAGE_FILE, MESG_IMAGE_FILE)) #array size testing
#     req_mesg_size(CARRY_IMAGE_FILE)

# if __name__ == '__main__':
#     main()