__author__ = 'podolsky'

import fcntl, sys, urllib2, time
from multiprocessing import Pool, Value, Lock

urlMaster= "http://aipanda100.cern.ch/preprocess/?mode=master"
urlSlave= "http://aipanda100.cern.ch/preprocess/?mode=slave"
numOfProcesses = 8
timeOutForQuery = 3001 # in seconds


class Counter(object):
    def __init__(self, initval=0):
        self.val = Value('i', initval)
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1

    def decrement(self):
        with self.lock:
            self.val.value -= 1


    def value(self):
        with self.lock:
            return self.val.value

def func(counter):
    for i in range(50):
        time.sleep(0.01)
        counter.increment()


def runPrep(counter,url):
    counter.increment()
    req = urllib2.Request(url)
    urllib2.urlopen(req, timeout = timeOutForQuery)

if __name__ == '__main__':
    pid_file = '/tmp/bigPandaMonPrep.pid'
    fp = open(pid_file, 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        sys.exit(0)


    poolMaster = Pool(1)
    poolSlave = Pool(processes=numOfProcesses)

    counterSlave = Counter(1)
    counterMaster = Counter(0)


    while(True):
        if counterSlave.value() > 0:
            result = poolSlave.apply_async(runPrep, args=(counterSlave, urlSlave))
            counterSlave.decrement()

        if counterMaster.value() > 0:
            result = poolMaster.apply_async(runPrep, args=(counterMaster, urlMaster))
            counterMaster.decrement()
        time.sleep(1)
