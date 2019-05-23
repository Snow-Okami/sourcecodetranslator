'''
Currently this file is broken.
A method of renaming the folders FIRST must happen for the files to be able to name themselves
A method of finding the number of occurrences (of a rename) as well as the individual occurrences and their placements needs to happen
'''
import win_unicode_console
import in_place

import os
import sys
import stat
import errno
import shutil
from shutil import move

root = 'D:\Scratch\PyKBETrans\Input_Renaming_1'

runFinalReplacements = False
fileIterations = 0

replacementTotal = 0
lineTotal = 0

fileIterator = 0
lineIterator = 0

patterns = ('.cpp', '.h', '.cs', '.py', '.xml', '.def', '.md')

currentDir = os.getcwd()
win_unicode_console.enable()
osSep = os.linesep
normSep = '\n'

def createIfNotExists(filepath):
	if not os.path.exists(os.path.dirname(filepath)):
		try:
			os.makedirs(os.path.dirname(filepath))
		except OSError as exc:  # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

def remove_readonly(fn, path, excinfo):
	try:
		os.chmod(path, stat.S_IWRITE)
		fn(path)
	except Exception as exc:
		print("Skipped:", path, "because:\n", exc)

def forceRename(src, dst):
	try:
		os.rename(src, dst)
	except WindowsError:
		os.remove(src)
		os.rename(src, dst)

for path, subdirs, files in os.walk(root):
	for name in files:
		if fileIterations != 0:
			if fileIterator >= fileIterations:
				break
		fileIterator = + 1
		if name.lower().endswith(patterns):
			currentLineNumber = 0
			lastLineNumberTranslated = 0
			currentFile = os.path.join(path, name)

			replacementIterator = 0
			blockFinalReplacement = False

			#IGNORE THESE
			if 'kbe/res/scripts/common' in currentFile:
				continue
			if 'ouro/res/scripts/common' in currentFile:
				continue
			if 'assets/logs' in currentFile:
				continue
			if 'idea' in currentFile:
				continue
			if 'kbe/bin/server/logs' in currentFile:
				continue
			if 'ouro/bin/server/logs' in currentFile:
				continue
			if 'kbe/src/lib/dependencies' in currentFile:
				continue
			if 'ouro/src/lib/dependencies' in currentFile:
				continue
			if 'interpreters' in currentFile:
				continue
			if 'ouro/src/_objs' in currentFile:
				continue
			if 'kbe/src/_objs' in currentFile:
				continue
			if 'kbe\tools\server\webconsole\static\js' in currentFile:
				continue
			if 'ouro\tools\server\webconsole\static\js' in currentFile:
				continue

			#FINAL IGNORES
			if 'kbe/src/lib/python/Doc' in currentFile:
				blockFinalReplacement = True
			if 'ouro/src/lib/python/Doc' in currentFile:
				blockFinalReplacement = True
			if 'kbe/src/lib/python/Lib' in currentFile:
				blockFinalReplacement = True
			if 'ouro/src/lib/python/Lib' in currentFile:
				blockFinalReplacement = True
			if 'kbe/res/scripts/common' in currentFile:
				blockFinalReplacement = True
			if 'ouro/res/scripts/common' in currentFile:
				blockFinalReplacement = True
			if 'assets/logs' in currentFile:
				blockFinalReplacement = True

			print('Scanning File: ', currentFile)

			if 'kbcmd' in currentFile:
				newFileName = currentFile.replace('kbcmd', 'obcmd')
				forceRename(currentFile, newFileName)
				replacementIterator += 1
				print('Replaced: ', currentFile)

print('Processed Files Total: ' + str(lineTotal))
print('Replacement Total: ' + str(replacementIterator))