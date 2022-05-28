#!/usr/bin/python3

import os, sys

CMARK = "/usr/bin/cmark"
BASE = "https://tonycolston.com"

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

def build_index():
    os.system(CMARK + " index.md --to html > index.tmp")
    os.system("cat templates/html_header.txt index.tmp templates/html_footer.txt > index.html")
    os.system("rm -f index.tmp")

def build_blog_index():
    files_to_work_on = []
    recursefiles_withpurpose("content",files_to_work_on)
    outf = open("./blog.tmp","w")
    
    for (_dir,_name) in files_to_work_on:
        print("working on",_dir,_name)
        # TODO: get front matter?

        # TODO: common mark this file into html

        # write the information out
        # to index file we are creating
        outf.write("something cool to read: {0} {1}".format(_dir,_name))
        outf.write("[something cool]({0}/{1}/{2})".format(BASE,_dir,_name))

    outf.close()

    # TODO: cmark the tmp file
    os.system(CMARK + " blog.tmp --to html > blog.tmp2")

    # take the file we wrote with the list of stuff
    # tack on the header and footer and put it in blog directory
    os.system("cat templates/html_header.txt ./blog.tmp2 templates/html_footer.txt > blog/index.html")
    
    # clean up
    # os.system("rm -f ./blog.tmp")
    # os.system("rm -f ./blog.tmp2")


if __name__ == "__main__":
    for i in range(len(sys.argv)):
        arg = sys.argv[i]
        if arg=="--build-index-only":
            build_index()

    build_blog_index()