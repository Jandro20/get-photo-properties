#!/usr/bin/env python3

import os
import sys
import getopt
from PIL import Image
from PIL.ExifTags import TAGS

def get_set_of_images(path):
    """ Get the list of images that we will use it """

    images = list(filter(lambda k: '.jpg' in k, os.listdir(path)))
    get_metadata(images)

def get_metadata(images):
    """ Obtain the metadata from images (list) and write it in LOG file"""

    # Properties that we don't need it
    excludes = ['PrintImageMatching', 50898, 50899, 'MakerNote', 34864]

    for nimage in images:

        # Open the image with PIL library
        image = Image.open(f"./images/{nimage}")

        # Extracting the metadata from the image
        exifdata = image.getexif()

        LOG.write(f"------------ Name: {nimage} ----------------\n")

        # Loop into all metadata tags that exist in the current image
        for tagid in exifdata:

            tagname = TAGS.get(tagid, tagid)

            # We filter all tags that we don't want to log it
            if tagname not in excludes:

                # passing the tagid to get its respective value
                value = exifdata.get(tagid)

                LOG.write(f"{tagname:27}: {value}\n")

        LOG.write("\n\n")

if __name__ == "__main__":

    PATH = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:", ["output="])
    except getopt.GetoptError:
        print("Command to use this tool: python get_properties.py -o <path/to/output/file>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("""You can use this command with some options:
    - If you use it with no options, the result will be saved in the same path where the tool is saved.
    - If you specify the output path, "python get_properties.py -o <path>", the result will be saved in <path>self.
    - If you need see this help again, "python get_properties.py -h".""")
            sys.exit(0)
        elif opt in ("-o", "--output"):
            PATH = arg

    if PATH == "":
        PATH = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(PATH):
        print(f"Path selected is not a valid path [{PATH}]")
        sys.exit(2)

    print(f"Path selected is: {PATH}")

    file = PATH+"/result.txt"
    LOG = open(file, 'w', encoding='utf-8')
    get_set_of_images("./images/")
    LOG.close()

    print(f"Completed! File created in {PATH}/result.txt")
