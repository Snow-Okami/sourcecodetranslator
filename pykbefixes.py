import win_unicode_console
import in_place

import os
import sys
import stat
import errno
import shutil

root = 'D:\Scratch\PyKBETrans\Input_9'

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

			with in_place.InPlace(currentFile, errors='replace') as file:
				for line in file:
					replacementLine = line
					currentLineNumber += 1
					if '?//' in replacementLine:
						replacementLine = replacementLine.replace('?//', '//')
						replacementIterator += 1
					if '??//' in replacementLine:
						replacementLine = replacementLine.replace('??//', '//')
						replacementIterator += 1
					if '???//' in replacementLine:
						replacementLine = replacementLine.replace('???//', '//')
						replacementIterator += 1
					if '????//' in replacementLine:
						replacementLine = replacementLine.replace('????//', '//')
						replacementIterator += 1
					if '?????//' in replacementLine:
						replacementLine = replacementLine.replace('?????//', '//')
						replacementIterator += 1
					if '??????//' in replacementLine:
						replacementLine = replacementLine.replace('??????//', '//')
						replacementIterator += 1
					if '????????????//' in replacementLine:
						replacementLine = replacementLine.replace('????????????//', '//')
						replacementIterator += 1
					if '????bool' in replacementLine:
						replacementLine = replacementLine.replace('????bool', '//')
						replacementIterator += 1
					if '?????int' in replacementLine:
						replacementLine = replacementLine.replace('?????int', '//')
						replacementIterator += 1
					if '?????CListCtrl' in replacementLine:
						replacementLine = replacementLine.replace('?????CListCtrl', '//')
						replacementIterator += 1
					if '/*?' in replacementLine:
						replacementLine = replacementLine.replace('/*?', '/*')
						replacementIterator += 1

					if '&#39;' in replacementLine:
						replacementLine = replacementLine.replace('&#39;', "'")
						replacementIterator += 1
					if '&gt;' in replacementLine:
						replacementLine = replacementLine.replace('&gt;', '/*')
						replacementIterator += 1
					if '&quot;' in replacementLine:
						replacementLine = replacementLine.replace('&quot;', "'")
						replacementIterator += 1

					#Reg Expression: .*[*?]//
					replacementTotal += replacementIterator
					lineTotal += lineIterator
					file.write(replacementLine)
					lineIterator += 1

				print('Processed Lines: ' + str(lineIterator))
				print('Replaced: ' + str(replacementIterator))

print('Processed Lines Total: ' + str(lineTotal))
print('Replaced Total: ' + str(replacementIterator))