import time
import JSDB

print "yea"
test = JSDB.JSDB()
print "baby"
test.openSession()
time.sleep(10)
#sendContinue(None)
#time.sleep(5)
#sendContinue(None)
#time.sleep(5)
test.sendStepNext()
time.sleep(5)
test.sendContinue(None)
time.sleep(5)
test.stopSession()
