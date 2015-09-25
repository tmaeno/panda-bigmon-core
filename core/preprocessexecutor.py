__author__ = 'podolsky'

import fcntl, sys, urllib2, time
import multiprocessing
from multiprocessing.pool import ThreadPool

urlMaster= "http://aipanda100.cern.ch/preprocess/?mode=master"
urlSlave= "http://aipanda100.cern.ch/preprocess/?mode=slave"
numOfProcesses = 8
timeOutForQuery = 3001 # in seconds


class Counter(object):
    def __init__(self, lock, initval=0):
        self.val = multiprocessing.Value('i', initval)
        self.lock = lock

    def increment(self):
        with self.lock:
            self.val.value += 1

    def decrement(self):
        with self.lock:
            self.val.value -= 1


    def value(self):
        with self.lock:
            return self.val.value


def runPrep(counter,url):
    counter.increment()
    req = urllib2.Request(url)
    urllib2.urlopen(req, timeout = timeOutForQuery)

def initMaster(l):
    global lockMaster
    lockMaster = l

def initSlave(l):
    global lockSlave
    lockSlave = l



if __name__ == '__main__':
    pid_file = '/tmp/bigPandaMonPrep.pid'
    fp = open(pid_file, 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        sys.exit(0)

    lockMaster = multiprocessing.Lock()
    lockSlave = multiprocessing.Lock()


    poolMaster = ThreadPool(initializer=initMaster, initargs=(lockMaster,), processes=1)
    poolSlave = ThreadPool(initializer=initSlave, initargs=(lockSlave,), processes=numOfProcesses)

    counterSlave = Counter( lockSlave, initval=8)
    counterMaster = Counter(lockMaster, initval=1)

    m = multiprocessing.Manager()

# http://stackoverflow.com/questions/25557686/python-sharing-a-lock-between-processes

    runPrep(counterMaster, urlMaster)

    while(True):
        if counterSlave.value() > 0:
            result = poolSlave.apply_async(runPrep, args=(counterSlave, urlSlave))
            print 'slave added'
            counterSlave.decrement()

        if counterMaster.value() > 0:
            result = poolMaster.apply_async(runPrep, args=(counterMaster, urlMaster))
            print 'master added'
            counterMaster.decrement()
        time.sleep(1)
