# not system-wide but simple thread interface with
# limited functionality utilities for PyArmCalc

import _thread as thread
import queue, sys

threadQueue = queue.Queue(maxsize=0)    # infinite size

# in main thread

def threadChecker(widget, delayMsecs=100, perEvent=1):
    for i in range(perEvent):
        try:
            callback, args = threadQueue.get(block=False)
        except queue.Empty:
            break
        else:
            callback(*args)
    widget.after(delayMsecs,
                 lambda: threadChecker(widget, delayMsecs, perEvent))
    
# in a new thread

def threaded(action, args):
    try:
        gen = action(*args)
        for i in gen:
            func, args = i
            threadQueue.put((func, args))
    except:
        threadQueue.put((print, (sys.exc_info(), )))

def startThread(action, args):
    thread.start_new_thread(
        threaded, (action, args))
