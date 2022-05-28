#!/bin/bash

CMARK=/usr/bin/cmark
HEAD=`pwd`

echo "HEAD is ${HEAD}"

${CMARK} index.md --to html > index.html
${CMARK} content/2022/04/resume.md --to html > content/2022/04/resume.html
