# coding: utf-8

import os
import copy
import hashlib
from urllib.parse import urlparse

import requests
from selectolax.parser import HTMLParser

from euclid import util


LOCAL_DATA_DIR = 'data'


###################
# Downloader
###################


def download_page(url):
    parsed = urlparse(url)
    name = parsed.netloc + '/' + parsed.path

    response = requests.get(url)
    response.raise_for_status()

    save(name, response.content)
    return response.content


# Save content
def save(name, content):
    uri = hashlib.md5(util.to_bytes(name)).hexdigest()
    dirname, fname = _get_path(uri)
    os.makedirs(dirname)
    with open(os.path.join(dirname, fname), 'wb') as fp:
        fp.write(content)


def _get_path(uri):
    return os.path.join(LOCAL_DATA_DIR, uri[:2]), uri[2:]


###################
# Extractor
###################


# Recursive extract html and convert to dict
def extract(content):

    def _parse(root, output):
        node = copy.deepcopy(root.attributes)

        if root.child:
            children = []
            _parse(root.child, children)
            if children:
                node['children'] = children

        if node:
            # We don't need `id`
            node.pop('id', None)
            output.append(node)

        if root.next:
            _parse(root.next, output)

    output = []
    root = HTMLParser(content).root
    if not root:
        return output
    _parse(root, output)
    return output


def main():
    pass


if __name__ == '__main__':
    main()
