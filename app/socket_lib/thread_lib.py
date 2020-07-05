import threading
import time
import inspect
import ctypes
import os
from client_for_inner import socket_connect_END
#=======================================================================================
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        print("stop : 0----------")
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        print("stop : !=1----------")
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
#----------------------------------------------------------------------------------------
def stop_thread(th):
    print("Stoped thread "+str(th.ident))
    _async_raise(th.ident, SystemExit)
#----------------------------------------------------------------------------------------
def stop_thread_safe(port): #safely stop old thread
    esc = []
    esc.append("ESC;END")
    socket_connect_END(port, esc, len(esc))
#========================================================================================