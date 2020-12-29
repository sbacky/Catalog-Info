#!/usr/bin/env python3

from PIL import Image
import os, sys, re

'''
Invocation ---> converter.py "dir|newDir|size|rotate|ext"

Examples:
    1.) convert images at dir be resizing to 600 x 400, rotating 180 degrees,
    changes image format to jpeg, and saves them to newDir.

    >>> converter.py "/path/to/images|/path/to/rotatedImages|600,400|180|jpeg"
    ------------------------------------------------
    2.) convert images at dir by rotating them 90 degrees and saving them to
    newDir.

    >>> converter.py "/path/to/images|/path/to/rotatedImages||90|"
    ------------------------------------------------
    3.) convert images at newDir by changing the image format to jpg and saving
    them back to dir.

    >>> converter.py "/path/to/images||||jpg"
    ------------------------------------------------
'''

def oneByOne():
    '''Changes convert() method to go through all images one by one.'''
    cont = "n"
    while cont.lower().strip() != "y":
        cont = input("Would you like to continue to the next file? ['y'/'n'/'q'] ... ")
        if cont == 'q':
            sys.exit(0)

def convert(dir, newDir, size, rotate, extension):
    '''Converts images in dir to size, rotate, and extension specifications.'''
    jpgForms = ["jpeg", "jpg"]
    images = os.listdir(dir)

    for image in images:
        # Check for any files not wanting to be processed
        if image.startswith(".") or image.endswith(extension):
            continue

        pattern = r"\.tiff"
        ext = ".{}".format(extension)
        match = re.search(pattern, image)
        if not match:
            continue
        newImage = re.sub(pattern, ext, image)
        # Get full path to unprocessed image
        unPath = os.path.join(dir, image)
        # Get full path to processed image
        prPath = os.path.join(newDir, newImage)
        # create instance of image at path called im
        im = Image.open(unPath)
        # If convert to jpeg, make sure image in RGB mode
        if im.mode != 'RGB' and extension.lower().strip() in jpgForms:
            im = im.convert('RGB')
        # if size or extension is null, set them accordingly
        if size == ('null', 'null'):
            size = im.size
        if extension == "null":
            extension = im.format

        im.rotate(rotate).resize(size).save(fp=prPath, format=extension)

        os.remove(unPath)
        # Unhash to go through images one by one
        #oneByOne()

    return "Successfully converted images at: {}".format(dir)

def main():
    dir, newDir, size, rotate, extension = sys.argv[1].split("|")

    # Check for empty inputs and fill them accordingly
    if newDir == "":
        newDir = dir
    if size == "":
        size = ('null', 'null')
    else:
        # Convert size to tuple
        try:
            num1, num2 = size.split(",")
        except ValueError:
            print("size: {}, has either to many or to little values to unpack".format(size))
            print("format size: |num1,num2|")
            sys.exit(22)
        try:
            size = (int(num1), int(num2))
        except ValueError:
            print("Values for size must contain only integers")
            print("example: |num1,num2| ---> |600,400|")
            sys.exit(23)
        # Check to ensure size is a tuple and that it is not empty
        if len(size) != 2 or type(size) != tuple:
            if type(size) != tuple:
                print("{} is not acceptable format\nPlease format size: |num1,num2|".format(size))
                sys.exit(20)
            print("size has length: {}\nPlease ensure size is a tuple formatted as: |num1,num2|".format(size))
            sys.exit(21)

    if rotate == "":
        rotate = "0"
    try:
        rotate = int(rotate)
    except ValueError:
        print("rotate: {}, must be an integer".format(rotate))
        print("example: |size| ---> |90|")
        sys.exit(30)

    if extension == "":
        extension = "null"

    try:
        os.path.isdir(dir)
        os.path.isdir(newDir)
    except TypeError:
        print("Please pass a directory to get started.")
        print("Invocation: converter.py dir|newDir|size|rotate|ext")
        sys.exit(1)
    except Exception as e:
        print("Please fix error in parameter format: {}".format(e))
        sys.exit(101)

    # Check to make sure dir and newDir exist
    if os.path.isdir(dir) != True:
        print("{} is not a vaid directory\nPlease pass a valid directory to get started".format(dir))
        sys.exit(10)
    if os.path.isdir(newDir) != True:
        print("{} is not a vaid directory\nPlease pass a valid directory to get started".format(newDir))
        sys.exit(11)

    # Check to ensure rotate is an integer less than 360 or above 0
    if rotate >= 360 or rotate < 0:
        print("rotate: {}, is above 360 or below 0\nPlease input a value that is less than 360 or greater than or equal to 0".format(rotate))
        sys.exit(31)

    # Check to ensure extension is type string that doesnt begins with (.)
    if extension.startswith(".") or type(extension) != str:
        if type(extension) != str:
            print("extension was type: {}\nPlease pass an extension of type str".format(extension))
            sys.exit(40)
        print("{} extension should NOT start with (.)\nPlease enter an extension without (.)".format(extension))
        sys.exit(41)

    #convert(dir, newDir, size, rotate, extension)
    try:
        convert(dir, newDir, size, rotate, extension)
        sys.exit(0)
    except Exception as e:
        print("Error in convert(): {}".format(e))
        sys.exit(101)

if __name__ == "__main__":
    main()
