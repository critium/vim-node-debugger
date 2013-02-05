#
#
# TODO: Need to switch to using select to make JSDBListen.
# TODO: Push events into stack, POP them when displayed to user.
#
import json
import select
import socket
import vim
from threading import Thread
from copy import deepcopy

class JSDB:
  marker  = 'Content-Length:'
  markEnd = '\r\n\r\n'
  head    = marker + ' $len' + markEnd
  req     = '{"seq":0,"type":"request","command":"scope","arguments":{"number":0,"frameNumber":0,"inlineRefs":true}}'
  sockMap = {
    'socket'   : None,
    't_listen' : None,
    'isDebug'  : True
  }
  port = 5858
  req  = {
  'seq'     : -1,
  'type'    : 'request',
  'command' : 'scope'
  # , 'arguments':{
  #   'number'      : 0,
  #   'frameNumber' : 0,
  #   'inlineRefs'  : 'true'
  #   }
  }
  ignoreNodeJSBrk = True
  nodeJSScriptName = 'node.js'
  ignoreConsoeBrk = True
  consoleScriptName = 'console.js'
  responses = []
  responseBuffer = ''
  selectTimeout = 0

  def openSession(self):
    print "opening debug session"
    dbsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dbsock.settimeout(2.0)
    dbsock.connect(('127.0.0.1', self.port))
    self.sockMap['socket'] = dbsock
    self.startListener()

  def stopSession(self):
    dbsock = self.sockMap['socket']
    self.sockMap['isDebug'] = False
    self.sockMap['t_listen'].join()

    dbsock.shutdown(socket.SHUT_RDWR)
    dbsock.close()

  # below follows the socket listener
  def startListener(self):
    thr = Thread(target=self.listenFunc,args=())
    thr.start()
    self.sockMap['t_listen'] = thr

  def listenFunc(self):
    dbsock = self.sockMap['socket']
    fragment = ''
    response = ''
    #waiting for new message
    while self.sockMap['isDebug']:
      #fragment= dbsock.recv(len(marker), socket.MSG_PEEK)
      fragment= dbsock.recv(1024)
      if not fragment: break
      if self.parse(fragment):
        break;

    ## Sockets from which we expect to read
    #inputs = [ dbsock ]
    ## Sockets to which we expect to write
    #outputs = [ ]

    #print 'creating select object'
    #readable, writable, exceptional = select.select(inputs, outputs, inputs, self.selectTimeout)
    #keepWhile = True;
    #while keepWhile:
      #if not (readable):
        #print 'timed out, do some other work here'
        #keepWhile = False
        #continue
      #print 'consuming readable object'
      #for s in readable:
        #print 'one readable'
        #if s is dbsock:
          #print 'sock found'

          #fragment= s.recv(1024)
          #if fragment:
            ## A readable client socket has data
            #print 'received "%s" from' % (fragment)
            #self.parse(fragment)
          #else:
            ## Interpret empty result as closed connection
            #print 'closing socket after reading no data'
            ## Stop listening for input on the connection
            #if s in outputs:
              #outputs.remove(s)
            #inputs.remove(s)
            #s.close()

  def parse(self, msg):
    # 'im going to parse the input message, look for content length, and jsonify it'
    #print '\n\n\n\n++M'+msg+'++'
    result = False;
    responseBuffer = self.responseBuffer
    responseBuffer += msg
    idxMark = responseBuffer.find(self.marker)
    # print '++IM' + str(idxMark)

    if idxMark >= 0:
      idxSet = responseBuffer.find(self.markEnd, idxMark)
      # print '++IS' + str(idxSet)

      if idxSet >= 0:
        idxMarkEnd = idxMark + len(self.marker)
        idxSetEnd  = idxSet + len(self.markEnd)
        msgLen     = int(responseBuffer[idxMarkEnd:idxSet] )
        idxMsgEnd  = idxSetEnd + msgLen
        print str(idxMarkEnd) + ' ' + str(idxSetEnd) + ' ' + str( msgLen ) + ' ' + str(idxMsgEnd) + ' ' + str(len(responseBuffer))

        # need to wait for the next chunk if msgend is > buffer
        if idxMsgEnd <= len(responseBuffer):
          # only process msg if len > 0
          if msgLen > 0:
            msg = responseBuffer[idxSetEnd:idxMsgEnd]
            print '-----\n' + msg + '\n-----\n'
            # convert to json object and send to processor
            self.processResponse(json.loads(msg))
            result = True;

          # reset the buffer
          responseBuffer = responseBuffer[idxMsgEnd:]

    return result;

  def processResponse(self, json):
    print 'called by parse, im going to process the json that it creates'
    isEvent = json['type'] == 'event'
    if isEvent:
      isBreak = json['event'] == 'break'
      if isBreak:
        scriptName = str (json['body'] [ 'script' ] [ 'name' ])
        lineNo = str (json['body'] [ 'script' ] [ 'lineOffset' ])
        #self.command('b testdebug.js')
        #self.command(r'syntax match %s "\%%%dl.\+"' % (group_name, line_number))

        ## if ignoring console brks, send step out
        #isNodeJS = scriptName == nodeJSScriptName
        #if isNodeJS and ignoreNodeJSBrk:
          ##sendStepOut()
          #self.sendContinue(None)

        ## if ignoring console brks, send step out
        #isConsoleJS = scriptName == consoleScriptName
        #if isConsoleJS and ignoreConsoeBrk:
          ##sendStepOut()
          #self.sendContinue(None)

  # below follows the actual debugger commands
  def setBreakpoints(self):
    print 'im going to read your directory and set breakpoints based on that'

  def sendStepOut(self):
    arguments = {
      "stepaction": "out"
    }
    self.sendContinue(self, arguments)

  def sendStepIn(self):
    arguments = {
      "stepaction": "in"
    }
    self.sendContinue(self, arguments)

  def sendStepNext(self):
    arguments = {
      "stepaction": "next"
    }
    self.sendContinue(arguments)

  def sendEval(self, script):
    raise NotImplementedError("give me some time to implmement it!!!")

  def sendLookup(self, handles):
    raise NotImplementedError("give me some time to implmement it!!!")

  def sendBacktrace(self, fromFrame, toFrame):
    raise NotImplementedError("give me some time to implmement it!!!")

  def sendFrame(self):
    raise NotImplementedError("give me some time to implmement it!!!")

  def sendScope(self):
    raise NotImplementedError("give me some time to implmement it!!!")

  def sendScripts(self):
    raise NotImplementedError("give me some time to implmement it!!!")

  def sendSource(self):
    raise NotImplementedError("give me some time to implmement it!!!")

  def sendSetBreak(self):
    raise NotImplementedError("give me some time to implmement it!!!")

  def sendChangeBreak(self):
    raise NotImplementedError("give me some time to implmement it!!!")

  def sendClearBreak(self):
    raise NotImplementedError("give me some time to implmement it!!!")

  def sendExceptionBreak(self):
    raise NotImplementedError("give me some time to implmement it!!!")

  def sendDisconnect(self):
    req = getReg('request', 'disconnect')
    self.sendCmd(self, req);

  def sendListBreakpoints(self):
    raise NotImplementedError("give me some time to implmement it!!!")

  def saveBreakpointToFile(self):
    raise NotImplementedError("give me some time to implmement it!!!")

  def readBreakpointFromFile(self):
    raise NotImplementedError("give me some time to implmement it!!!")

  def sendCmd(self, cmd):
    dbsock = self.sockMap['socket']
    body = json.dumps(cmd)
    message = self.head.replace('$len', str(len(body))) + body
    print message
    dbsock.send(message)

  def getReq(self, typ, command):
    newReq = deepcopy(self.req)
    newReq['seq'] = newReq['seq'] + 1
    newReq['type'] = typ
    newReq['command'] = command
    print 'Current Seq' + str(newReq['seq'])
    return newReq

  def sendContinue(self, args):
    req = self.getReq('request', 'continue')
    if args is not None:
      req['arguments'] = args
    self.sendCmd(req)

  def normalCommand(self, command):
    self.command('normal ' + command)

  def command(self, command):
    vim.command(command)

  def setLinesHighlighting(self, line_numbers, group_name):
    for line_number in line_numbers:
      self.command(r'syntax match %s "\%%%dl.\+"' % (group_name, line_number))

