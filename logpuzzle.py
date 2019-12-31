#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U;
Windows NT 5.1; en-US; rv:1.8.1.6)
Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import urllib.request
import argparse


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    paths = []
    full_urls = []

    # For the host and site names
    url = filename.split("_")
    # Search specific file for all url matches using regex pattern
    with open(filename, "r") as f:
        matches = re.findall(r"GET \S+puzzle\S+ HTTP", f.read())
    # Get just the path of the match without all the extra
    for match in matches:
        if match[4:-5] not in paths:
            paths.append(match[4:-5])
    # Sort by the second word in path if given
    if len(paths[0].split("p-")[-1].split("-")) == 2:
        paths.sort(key=lambda x: x.split("-")[-1][0:-4])
    else:
        paths.sort(key=lambda x: x.split("/")[-1][0:-4])
    # Piece them back into a proper url
    for path in paths:
        full_urls.append("https://" + url[1] + path.split("puzzle")[0] +
                         "puzzle/" + path.split("/")[-1])
    # Return list of urls to be printed or downloaded
    return full_urls


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    img_names = []
    # Check if directory exists; create if not and change to it
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
        os.chdir(dest_dir)
    # If directory exits make sure to change to that directory
    else:
        os.chdir(dest_dir)
    # Print line saying which url is being retrieved
    # and do retrieve that url with urllib
    for index, url in enumerate(img_urls):
        print("Retrieving: " + url)
        urllib.request.urlretrieve(url, "img" + str(index))
        img_names.append("img" + str(index))
    # Create index.html file that will be displaying the file's pictures
    with open("index.html", "w") as f:
        f.write("<html>\n<body>")
        for img in img_names:
            f.write("<img src='" + img + "'>")
        f.write("<body>\n<html>")


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
