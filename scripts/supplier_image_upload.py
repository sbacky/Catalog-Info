#!/usr/bin/env python3

import requests, os, sys, re

def get_files(dir):
    '''Returns list of paths to images to be processed at directory passed.'''
    # Check to make sure dir exists
    if os.path.isdir(dir) != True:
        print(
            "Error Code [10]: {} is not a vaid directory\nPlease pass a valid \
            directory to get started".format(dir)
        )
        sys.exit(10)
    # Create list of images and check to make sure list is not empty
    fullList = os.listdir(dir)
    imageList = []
    pattern = r"\.jpeg"
    for file in fullList:
        match = re.search(pattern, file)
        if not match:
            continue
        imageList.append(file)

    imageList.sort()
    if len(imageList) < 1:
        return "No images in directory: {}".format(dir)
        sys.exit(0)
    # Create list of paths to images
    pathList = []
    for image in imageList:
        fullPath = os.path.join(dir, image)
        pathList.append(fullPath)

    return pathList

def post_images(full_path):
    '''Upload image to Fruit catalog website at URL:
    https://35.202.145.247/media/images and returns status_code of request.'''
    url = "http://localhost/upload/"
    with open (full_path, 'rb') as opened:
        r = requests.post(url, files={'file': opened})

    status_code = r.status_code
    if not r.ok:
        return (False, status_code)
    return (True, status_code)

def main():
    dir = sys.argv[1]
    pathList = get_files(dir)
    s = 0
    f = 0
    con_f = 0
    for full_path in pathList:
        status, status_code = post_images(full_path)
        filename = os.path.basename(full_path)
        if not status:
            print(
                "POST failed for file {} with status code: \
                {}".format(filename, status_code)
            )
            f += 1
            con_f += 1
        else:
            print(
                "POST succeded for file {} with status code: \
                {}".format(filename, status_code)
            )
            s += 1
            con_f = 0
        if con_f == 3:
            print("Error Code [40]: Too many POST's failed, check connection")
            sys.exit(40)

    total = s + f
    half = total // 2
    return "COMPLETE! {}/{} POST's were uploaded successfully".format(s, total)
    sys.exit(0)

if __name__ == "__main__":
    main()
