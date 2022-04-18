#!/usr/bin/env python3

import os
import sys
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
    LOG = open("log.txt", 'w')
    get_set_of_images("./images/")
    LOG.close()
