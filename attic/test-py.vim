"
" Javascript Debuffer vim-javascript-debugger
"

let current_dir = expand("<sfile>:h")
python import sys
exe 'python sys.path.insert(0, r"' . current_dir . '")'
"python import VimPdb


function! JSDBInitialize()
  call JSDBInitialize_py()
endfunction

function! JSDBInitialize_py()
python << EOF
import vim
import threading
import time
import re

def jsStartDebug():
  global jsDb;
EOF
endfunction
