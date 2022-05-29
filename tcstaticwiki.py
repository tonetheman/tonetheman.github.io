#!/usr/bin/python3

import os, sys
import pathlib

CMARK = "/usr/bin/cmark"
BASE = "https://tonycolston.com"
OUTPUT_DIR = "output"
VARS = {
    "sitename" : "tonycolston.com"
}

def recursfiles(head_directory):
    for f in os.scandir(head_directory):
        if f.is_dir():
            recursfiles(os.path.join(head_directory,f.name))
        else:
            print("FILE:",head_directory,f.name)
            if f.name.endswith(".md"):
                print("markdown file!")

def recursefiles_withpurpose(head_directory, outlist):
    for f in os.scandir(head_directory):
        if f.is_dir():
            recursefiles_withpurpose(os.path.join(head_directory,f.name),outlist)
        else:
            if f.name.endswith(".md"):
                outlist.append((head_directory,f.name))
            elif f.name.endswith(".html"):
                outlist.append((head_directory,f.name))


def build_index():
    os.system(CMARK + " index.md --to html > index.tmp")
    os.system("cat templates/html_header.txt index.tmp templates/html_footer.txt > index.html")
    os.system("rm -f index.tmp")

def handle_markdown_file(_dir,_filename):
    print("handle markdown")
    
    # convert to a Path to split later
    p = pathlib.Path(_dir)

    # something is wrong if this fails!
    assert(p.parts[0]=="content") # always there!
    
    # this is the most forked up python
    # i have written in a long time
    # p.parts[1:]  does not include the content dir where this file is located
    # make a new tuple of output_dir + the shape in the content directory
    # then use * to apply it? or open the tuple... whatever that syntax is named
    out_dir = pathlib.Path(*((OUTPUT_DIR,) + p.parts[1:]))

    # make the dir in the output area if needed
    if not out_dir.exists():
        out_dir.mkdir(parents=True)



def handle_html_file(_dir,_filename):
    print("handle html")


def build_blog_index():
    files_to_work_on = []
    recursefiles_withpurpose("content",files_to_work_on)
    
    for (_dir,_name) in files_to_work_on:
        # print("working on",_dir,_name)
        if _name.endswith(".md"):
            handle_markdown_file(_dir,_name)
        elif _name.endswith(".html"):
            handle_html_file(_dir,_name)





if __name__ == "__main__":
    for i in range(len(sys.argv)):
        arg = sys.argv[i]
        if arg=="--build-index-only":
            build_index()

    build_blog_index()