import cv2
import requests
from mss import mss

TOLERANCE = 10

# threshold and rgb image
def isWhite(rgb_val):
    if rgb_val[0] <= (rgb_val[1] + TOLERANCE) and rgb_val[0] >= (rgb_val[1] - TOLERANCE) and rgb_val[0] > 220:
        return True
    else:
        return False

def demon_status(imagepath):

    image = cv2.imread(imagepath)

    first_digit = -1
    second_digit = -1

    # 569 751, 569 758, 590 751, 590 758
    image_demon = image[751:758+1, 570:590+1].copy()
    height, width, channels = image_demon.shape

    for x in range(0, width):
        for y in range(0, height):
                if isWhite(image_demon[y,x]):
                    image_demon[y,x] = [ 255, 255, 255 ]
                else:
                    image_demon[y,x] = [ 0, 0, 0]

    # debug output
    
    cv2.imwrite("output/demon.png", image_demon)

    # check first digit from left. if no digit detected, raid started
    for pattern in range(1, 10):
        sum = 0
        pattern_image = cv2.imread("pattern/" + str(pattern) + ".png")
        height_p, width_p, channels_p = pattern_image.shape
        for x in range(0, width_p):
            for y in range(0, height_p):
                sum += pattern_image[y,x][0] ^ image_demon[y, x][0] 
        # if every pixel was identical, the sum has to be zero
        if sum == 0:
            first_digit = pattern
            break

    # now check the second digit

    #if first_digit == 1:
    #    offset = 3
    #else:
    #    offset = 5
    offset = 5

    for pattern in range(1, 10):
        sum = 0
        pattern_image = cv2.imread("pattern/" + str(pattern) + ".png")
        height_p, width_p, channels_p = pattern_image.shape
        for x in range(0, width_p):
            for y in range(0, height_p):
                sum += pattern_image[y,x][0] ^ image_demon[y, x+offset+1][0]
        # if every pixel was identical, the sum has to be zero
        if sum == 0:
            second_digit = pattern
            break

    if first_digit == -1 and second_digit == -1: # raid started
        return -1
    elif first_digit != -1 and second_digit == -1:
        return first_digit
    else:
        return int(str(first_digit) + str(second_digit))


def angel_status(imagepath):

    # original image
    image = cv2.imread(imagepath)

    first_digit = -1
    second_digit = -1

    # 434 751, 434 758, 454 751, 454 758
    image_angel = image[751:758+1, 434:454+1].copy()
    height, width, channels = image_angel.shape

    for x in range(0, width):
        for y in range(0, height):
                if isWhite(image_angel[y,x]):
                    image_angel[y,x] = [ 255, 255, 255 ]
                else:
                    image_angel[y,x] = [ 0, 0, 0]

    # debug output
    
    cv2.imwrite("output/angel.png", image_angel)

    # check first digit from left. if no digit detected, raid started
    for pattern in range(1, 10):
        sum = 0
        pattern_image = cv2.imread("pattern/" + str(pattern) + ".png")
        height_p, width_p, channels_p = pattern_image.shape
        for x in range(0, width_p):
            for y in range(0, height_p):
                sum += pattern_image[y,x][0] ^ image_angel[y, x][0]
        # if every pixel was identical, the sum has to be zero
        if sum == 0:
            first_digit = pattern
            break

    # now check the second digit

    #if first_digit == 1:
    #    offset = 3
    #else:
    #    offset = 5
    offset = 5

    for pattern in range(0, 10):
        sum = 0
        pattern_image = cv2.imread("pattern/" + str(pattern) + ".png")
        height_p, width_p, channels_p = pattern_image.shape
        for x in range(0, width_p):
            for y in range(0, height_p):
                sum += pattern_image[y,x][0] ^ image_angel[y, x+offset+1][0]
        # if every pixel was identical, the sum has to be zero
        if sum == 0:
            second_digit = pattern
            break

    if first_digit == -1 and second_digit == -1: # raid started
        return -1
    elif first_digit == -1 and second_digit != -1:
        return second_digit
    else:
        return int(str(first_digit) + str(second_digit))

def detect_raid_angel(imagepath):

    # original image
    image = cv2.imread(imagepath)

    # 434 751, 434 758, 454 751, 454 758
    image_angel = image[751:758+1, 434:454+1].copy()
    height, width, channels = image_angel.shape

    for x in range(0, width):
        for y in range(0, height):
                if isWhite(image_angel[y,x]):
                    image_angel[y,x] = [ 255, 255, 255 ]
                else:
                    image_angel[y,x] = [ 0, 0, 0]

    # check first digit from left. if no digit detected, raid started
    sum = 0
    pattern_image = cv2.imread("pattern/angel_raid.png")
    height_p, width_p, channels_p = pattern_image.shape
    for x in range(0, width_p):
        for y in range(0, height_p):
            sum += pattern_image[y,x][0] ^ image_angel[y, x][0]
    # if every pixel was identical, the sum has to be zero
    return sum == 0

def binarize(imagepath):
    # original image
    image = cv2.imread(imagepath)

    height, width, channels = image.shape

    for x in range(0, width):
        for y in range(0, height):
                if isWhite(image[y,x]):
                    image[y,x] = [ 255, 255, 255 ]
                else:
                    image[y,x] = [ 0, 0, 0]
    return image
    
def detect_raid_demon(imagepath):

    # original image
    image = cv2.imread(imagepath)
    pattern_image = cv2.imread("pattern/demons_raid.png")
    height_p, width_p, channels_p = pattern_image.shape


    # 569 751, 569 758, 590 751, 590 758
    image_demon = image[751:751+height_p, 570:570+width_p].copy()
    height, width, channels = image_demon.shape

    for x in range(0, width):
        for y in range(0, height):
                if isWhite(image_demon[y,x]):
                    image_demon[y,x] = [ 255, 255, 255 ]
                else:
                    image_demon[y,x] = [ 0, 0, 0]

    # debug output
    
    cv2.imwrite("output/demon.png", image_demon)

    # check first digit from left. if no digit detected, raid started
    sum = 0
    for x in range(0, width_p):
        for y in range(0, height_p):
            sum += pattern_image[y,x][0] ^ image_demon[y, x][0]
    # if every pixel was identical, the sum has to be zero
    return sum == 0

if __name__ == "__main__":
    for i in range(1, 9):
        print("image" + str(i) + ":")
        print(demon_status("samples/image" + str(i) + ".jpg"))
        print(angel_status("samples/image" + str(i) + ".jpg"))
        print("-------------------------")