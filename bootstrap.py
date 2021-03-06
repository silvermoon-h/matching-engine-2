#!/usr/bin/env python

# This script simply downloads waf to the current directory

from __future__ import print_function
import os, sys, stat, hashlib, subprocess

WAFRELEASE = "waf-1.9.7"
WAFURLS    = ["http://ftp.waf.io/pub/release/" + WAFRELEASE,
              "http://www.freehackers.org/~tnagy/release/" + WAFRELEASE]
SHA256HASH = "c7f9d47cc56559a4755088026dff2475726a9e0b110555ef5ae5aeddb21dfb4f"

if os.path.exists("waf"):
    wafver = subprocess.check_output(['./waf', '--version']).decode()
    if WAFRELEASE.split('-')[1] == wafver.split(' ')[1]:
        print("Found 'waf', skipping download.")
        sys.exit(0)

try:
    from urllib.request import urlopen, URLError
except:
    from urllib2 import urlopen, URLError

waf = None

for WAFURL in WAFURLS:
    try:
        print("Downloading {}...".format(WAFURL))
        waf = urlopen(WAFURL).read()
        break
    except URLError:
        print("Download failed.")

if not waf:
    print("Could not download {}.".format(WAFRELEASE))

    sys.exit(1)

if SHA256HASH == hashlib.sha256(waf).hexdigest():
    with open("waf", "wb") as wf:
        wf.write(waf)

    os.chmod("waf", os.stat("waf").st_mode | stat.S_IXUSR)
    print("Checksum verified.")
else:
    print("The checksum of the downloaded file does not match!")
    print(" - got:      {}".format(hashlib.sha256(waf).hexdigest()))
    print(" - expected: {}".format(SHA256HASH))
    print("Please download and verify the file manually.")

    sys.exit(1)
