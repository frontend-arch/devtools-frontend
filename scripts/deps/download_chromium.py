#!/usr/bin/env python
#
# Copyright 2019 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
Used to download a pre-built version of Chrome for running unit tests
"""

import argparse
import os
import shutil
import sys
import urllib
import zipfile


def parse_options(cli_args):
    parser = argparse.ArgumentParser(description='Download Chromium')
    parser.add_argument('url', help='download URL')
    parser.add_argument('target', help='target directory')
    parser.add_argument('path_to_binary', help='path to binary inside of the zip archive')
    parser.add_argument('build_number', help='build number to find out whether we need to re-download')
    return parser.parse_args(cli_args)


def download_and_extract(options):
    BUILD_NUMBER_FILE = os.path.join(options.target, 'build_number')
    EXPECTED_BINARY = os.path.join(options.target, options.path_to_binary)
    # Check whether we already downloaded pre-built Chromium of right build number
    if os.path.exists(BUILD_NUMBER_FILE):
        with open(BUILD_NUMBER_FILE) as file:
            build_number = file.read().strip()
            if build_number == options.build_number:
                assert os.path.exists(EXPECTED_BINARY)
                return

    # Remove previous download
    if os.path.exists(options.target):
        shutil.rmtree(options.target)

    # Download again and save build number
    filehandle, headers = urllib.urlretrieve(options.url)
    zip_file = zipfile.ZipFile(filehandle, 'r')
    zip_file.extractall(path=options.target)
    os.chmod(EXPECTED_BINARY, 0o555)
    with open(BUILD_NUMBER_FILE, 'w') as file:
        file.write(options.build_number)


if __name__ == '__main__':
    OPTIONS = parse_options(sys.argv[1:])
    download_and_extract(OPTIONS)
