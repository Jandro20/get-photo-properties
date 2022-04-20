#!/usr/bin/env python3

import os
import sys
import getopt
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

def get_set_of_images(path, type_img):
    """ Get the list of images that we will use it """

    if type_img != "":
        images = list(filter(lambda x: type_img in x, os.listdir(path)))
    else:
        images = list(os.listdir(path))

    if images:
        get_metadata(images)
    else:
        print("Empty list of images! Check image folder.")
        exit(1)


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
    TYPE = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:t:", ["output=", "type="])
    except getopt.GetoptError:
        print("Command to use this tool: python get_properties.py -o <path/to/output/file>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("""You can use this command with some options:
    - If you use it with no options, the result will be saved in the same path where the tool is saved.
    - If you specify the output path, "python get_properties.py -o <path>", the result will be saved in <path>self.
    - If you need see this help again, "python get_properties.py -h".
    - If you want specify the type of image to get properties, "python get_properties.py -t
        ["jpg", "jpeg", "png", "raw"]" """)
            sys.exit(0)
        elif opt in ("-o", "--output"):
            PATH = arg
        elif opt in ("-t", "--type"):
            if arg in ["jpg", "jpeg", "png", "raw"]:
                TYPE = str(arg)
            else:
                print("Specified type of image is not supported")
                sys.exit(1)

    # If path is not specified, we will use the path of the tool dir
    if PATH == "":
        PATH = os.path.dirname(os.path.abspath(__file__))

    if TYPE == "":
        print("Parsing all images in ./images")

    if not os.path.exists(PATH):
        print(f"Path selected is not a valid path [{PATH}]")
        sys.exit(2)

    print(f"Path selected is: {PATH}")

    file = PATH+"/result-"+ datetime.now().strftime("%H%M%S") +".txt"
    LOG = open(file, 'w', encoding='utf-8')
    get_set_of_images("./images/", TYPE)
    LOG.close()

    print(f"Completed! File created in {PATH}/result.txt")
