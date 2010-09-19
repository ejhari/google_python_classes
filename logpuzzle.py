#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++
  host = re.findall('_(\w+.\w+.com)', filename)
  aa, url, i = [], [], 0
  f = open(filename, 'r')
  text = f.read()
 
  if filename == 'animal_code.google.com':
    groups=re.findall(r'GET\s(\S+/puzzle/\S+.jpg)\sHTTP', text)   
    k = None
  elif filename == 'place_code.google.com':
    groups=re.findall(r'GET\s(\S+/puzzle/\w+.\w+.(\w+).jpg)\sHTTP', text)   
    k = lambda x: x[-1]
  
  aa = list(set(groups))
  aa = sorted(aa, key = k) 
  
  while i < len(aa): 
    if filename == 'animal_code.google.com':
      url.append('http://' + host[0] + aa[i])
    elif filename == 'place_code.google.com':
      url.append('http://' + host[0] + aa[i][0])
    i+=1
  
  return url  
  ###
 
def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  i, tmp = 0, ''
  
  os.mkdir(dest_dir)
  os.chdir(dest_dir)
  
  while i < len(img_urls): 
    if urllib.urlretrieve(img_urls[i], filename='img'+str(i)): 
      print 'Retrieving image {0}... '.format(i)
    i+=1

  i, h = 0, open('index.html','w')
  
  while i < len(img_urls):
    tmp += '<img src="img' + str(i) + '"/>'
    i+=1
  
  h.write(tmp)
  h.close()
  ### 

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])
 
  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
