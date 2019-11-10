# -*- coding: cp936 -*-
'''use pydbg, 钩取将数据保存到记事本得函数,将保存内容修改为程序员制定的内容'''
# python27
# window7 32bit
# warnning: before,py2.7.9, not pip, importError Modul utils

import utils, sys
from pydbg import *
from pydbg.define import *


'''
BOOL WINAPI WriteFile(
	_IN_	HANDLE hFile,
	_IN_	LPCVOID lpBuffer,
	_IN_	DWORD nNumberOfBytesToWrite,
	_Out_opt_	LPDWORD lpNumberOfBytesWritten,
	_Inout_opt_	LPOVERLAPPED lpOverlapped
);
'''

dbg = pydbg()
isProcess = False

orgPattern = "love"
repPattern = "fuck"
processName = "notepad.exe"

def replaceString(dbg, args):
	buffer = dbg.read_process_memory(args[1], args[2])

	if orgPattern in buffer:
		print "[APIHooking] before: %s"%buffer
		buffer = buffer.replace(orgPattern, repPattern)
		replace = dbg.write_process_memory(args[1], buffer)
		print "[APIHooking] After: %s"%dbg.read_process_memory(args[1], args[2])

	return DBG_CONTINUE

for(pid, name) in dbg.enumerate_processes():
	if name.lower() == processName:
		isProcess = True
		hooks = utils.hook_container()
		dbg.attach(pid)
		print "Save a process handle in self.h_process of pid [%d]"%pid

		hookAddress = dbg.func_resolve_debuggee("kernel32.dll", "WriteFile")

		if hookAddress:
			hooks.add(dbg, hookAddress, 5, replaceString, None)
			print "Set a breakpoint at the designated address : 0x%08x"%hookAddress
			break
		else:
			print "[Error] : couldnot resolve hook address"
			sys.exit(-1)

	if isProcess:
		print "waiting for accurring debugger event"
		dbg.run()
	else:
		print "[Error] : There is no process [%s]"%processName
		sys.exit(-1)