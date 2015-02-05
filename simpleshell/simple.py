#!/usr/bin/env python

import sys
import os

#f = open("script.gdb", "w")
#gdb_script = """
#set logging file gdb_out
#set logging overwrite off
#set verbose off
#set confirm off
#b *0x08048a63
#r <  test
#set logging on
#print "======="
#x/20x $ebp - 0x54
#x/s $ebp - 0x54
#set logging off
#quit
#"""
#f.write(gdb_script)
#f.close()

f = open("test", "w")
f.write("login\n")
f.write("admin\n")
f.write(chr(0x56)*20)
f.close()


exec_gdb = "gdb -q simpleshell -x script.gdb"
os.system(exec_gdb)
