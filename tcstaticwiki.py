#!env/bin/python3

import os, sys
import pathlib
import commonmark

CMARK = "/usr/bin/cmark"
BASE = "https://tonycolston.com"
OUTPUT_DIR = "output"
VARS = {
    "sitename" : "tonycolston.com"
}

def action_blogindex():
    pass

def action_social():
    pass

def action_misc():
    pass

ACTIONS = {
    "$blogindex" : action_blogindex,
    "$social" : action_social,
    "$misc" : action_misc
}

# take a filename and return
# the markdown data and frontmatter
def getfiledata(filename):
    front = {}
    rest = ""
    front_matter  = False

    inf = open(filename,"r")
    for ln,line in enumerate(inf):
        if front_matter == False:
            if line.startswith("---"):
                front_matter = True
                continue

            rest = rest + line
        else:
            if line.startswith("---"):
                front_matter = False
                continue

            tmp = line.split(":")

            if len(tmp)==1:
                # skip weird lines
                continue

            key = tmp[0].strip()
            value = tmp[1].strip()

            if key=="":
                pass
            else:
                front[key] = value

    inf.close()

    return (front,rest)

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

    # get the data from file and the front matter key/values
    (front,data) = getfiledata(os.path.join(_dir,_filename))

    if "draft" in front:
        draft = front["draft"].lower()
        if draft == "true":
            return
    
    # get the data for the markdown translated    
    final_data = commonmark.commonmark(data)

    # write the translated markdown to disk
    # get rid of the .md and replace it with .html
    sfilename = _filename.split(".md")
    final_filename = os.path.join(out_dir,sfilename[0]+".html")
    outf = open(final_filename,"w")
    outf.write(final_data)
    outf.close()

def handle_html_file(_dir,_filename):
    print("handle html")


def build_blog():
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

    build_blog()