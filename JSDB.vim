"
" vimjsdb.vim
"
" Author:
"

"
" Initialization code
"

function! JSDBInit()
  let current_dir = expand("<sfile>:h")
  python import sys
  exe 'python sys.path.insert(0, r"' . current_dir . '")'

  call JSDBInit_py()
endfunction


function! JSDBInit_py()
python << EOF
import socket               # Import socket module
import JSDB

reload(JSDB)
jsdebug = JSDB.JSDB()

EOF
endfunction

function! JSDBStart()
python << EOF
jsdebug.openSession()
EOF
endfunction

function! JSDBStop()
python << EOF
jsdebug.stopSession()
EOF
endfunction

function! JSDBStep()
python << EOF
jsdebug.sendStepNext()
EOF
endfunction

function! JSDBContinue()
python << EOF
jsdebug.sendContinue(None)
EOF
endfunction

function! JSDBListen()
python << EOF
jsdebug.listenFunc()
EOF
endfunction
