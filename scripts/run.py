#!/usr/bin/env python3

import requests, os, sys, re, json

'''
Structure of file:
name
weight (in lbs)
description

Structure of dictionary:
{"name": "Test Fruit", "weight": 100, "description": "This is the description of
my test fruit", "image_name": "icon.sheet.png"}

Example:
{"name": "Watermelon", "weight": 500, "description": "Watermelon is good for
relieving heat, eliminating annoyance and quenching thirst. It contains a lot of
water, which is good for relieving the symptoms of acute fever immediately. The
sugar and salt contained in watermelon can diuretic and eliminate kidney
inflammation. Watermelon also contains substances that can lower blood
pressure.", "image_name": "010.jpeg"}
'''
class catalog_info:
    def __init__(self, name, weight, description, image_name):
        self.name = name
        self.weight = weight
        self.description = description
        self.image_name = image_name
        self.post = {}

    def check_values(self):
        try:
            int(self.weight)
        except ValueError:
            match = re.search(r"\D+", self.weight)
            if not match:
                msg = "Error Code [12]: Invalid value for weight {}. \
                Weight can be just an integer or an integer followed by \
                lbs".format(self.weight)
                return False, msg
            self.weight = re.sub(r"\D+", "", self.weight)
        if type(self.description) != str or type(self.image_name) != str or type(self.name) != str:
            msg = "Error Code [12]: These variables must be strings:\nname: {}\ndescription: {}\n \
            image_name: {}".format(self.name, self.description, self.image_name)
            return False, msg
        return True, self.weight

    def set_post(self):
        check, var = self.check_values()
        if not check:
            return var
            sys.exit(12)
        self.post["name"] = self.name
        self.post["weight"] = int(var)
        self.post["description"] = self.description
        self.post["image_name"] = self.image_name
        return self.post

def get_files(dir):
    '''Returns list of paths to files at directory passed.'''
    fullList = os.listdir(dir)
    fileList = []
    pattern = r"\.[a-zA-Z]+"
    for file in fullList:
        match = re.search(pattern, file)
        if not match:
            continue
        fileList.append(file)

    fileList.sort()
    if len(fileList) < 1:
        return "No images in directory: {}".format(dir)
        sys.exit(0)
    # Create list of paths to images
    pathList = []
    for f in fileList:
        fullPath = os.path.join(dir, f)
        pathList.append(fullPath)

    return pathList

def setInfo(image_path, txt_path):
    '''Return a list of dictionaries of info from image and text files.'''
    # Get list of texts and images files
    pathTxtList = get_files(txt_path)
    pathImageList = get_files(image_path)
    if len(pathTxtList) < 1 or len(pathImageList) < 1:
        print("Error Code [13]: No files in {} or {} directories.".format(image_path, txt_path))
        sys.exit(13)
    imageList = []
    for imagePath in pathImageList:
        image = os.path.basename(imagePath)
        imageList.append(image)
    imageList.sort()

    postList = []
    while len(pathTxtList) > 0 and len(imageList) > 0:
        image_name = imageList.pop(0)
        txtPath = pathTxtList.pop(0)
        txt = open(txtPath, "r")
        name = txt.readline().strip()
        weight = txt.readline().strip()
        description = txt.read().strip()
        txt.close()
        p = catalog_info(name, weight, description, image_name)
        post = p.set_post()
        postList.append(post)
    return postList

def uploadInfo(post):
    '''Upload info stored in dictionary to url http://35.202.145.247/fruits.'''
    url = "http://35.202.145.247/fruits/"
    js = json.dumps(post)
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    response = requests.post(url, data=js, headers=headers)
    print("url: {}\n".format(response.request.url))
    print("body: {}\n".format(response.request.body))
    print("status code: {}".format(response.status_code))

def main():
    image_path, txt_path = sys.argv[1].split("|")
    postList = setInfo(image_path, txt_path)
    for pt in postList:
        uploadInfo(pt)

if __name__ == "__main__":
    main()
