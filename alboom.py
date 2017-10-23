#!/usr/bin/env python

import sys
import os
import signal
import argparse
import re
from bottle import template
import shutil

cwd = os.path.dirname(os.path.abspath(__file__)) + '/'
print cwd

def copyrecursively(source_folder, destination_folder):
    for root, dirs, files in os.walk(source_folder):
	for item in files:
	    src_path = os.path.join(root, item)
	    dst_path = os.path.join(destination_folder, src_path.replace(source_folder, ""))
	    if os.path.exists(dst_path):
		if os.stat(src_path).st_mtime > os.stat(dst_path).st_mtime:
		    shutil.copy2(src_path, dst_path)
	    else:
		shutil.copy2(src_path, dst_path)
	for item in dirs:
	    src_path = os.path.join(root, item)
	    dst_path = os.path.join(destination_folder, src_path.replace(source_folder, ""))
	    if not os.path.exists(dst_path):
		os.mkdir(dst_path)

def main():
    tplPath = cwd + 'templates/basic/'
    dest = cwd + 'output/'

    copyrecursively(tplPath, dest)
  
    with open(tplPath + 'index.html', "rb") as f:
	tpl = f.read()

    my_dict={
	'title': 'alboom',
	'pics': [{"src": ".", "alt": "1"}, {"src": ".", "alt": "2"}]
    }
    print my_dict['pics'][0]
    tplParsed = template(tpl, **my_dict)
    
    f = open('output/index.html', 'w')
    f.write(tplParsed)

# ---------------------------------------------------------

def signal_handler(signal, frame):
    print '\nYou pressed Ctrl+C!'
    sys.exit(0)

if __name__ == "__main__":
    # sys.excepthook = exception_handler

    try:
        main()

    except KeyboardInterrupt:
        signal.signal(signal.SIGINT, signal_handler)
        signal.pause()


