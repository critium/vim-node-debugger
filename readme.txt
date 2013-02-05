Attempting to copy how vimpdb does debugger.

What works:
1. If you invoke JSDB, and run testfile.js in debug mode, it you can perform cont, step, etc.


What needs work:
1. Need to translate that back into what is shown in VIM.
1.1 Find the buffer where the debug point is.  If exists, open it and highlight the line.
1.2 Sane mappings for cont, next and step.  Currently only invokable by calling the methods themselves.
1.3 PROFIT!!!
