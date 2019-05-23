import win_unicode_console
import in_place

import os
import sys
import stat
import errno
import shutil

#root = 'D:\Scratch\PyKBETrans\Input_9'
root = 'D:\Scratch\___KBE__\ouroboros-2.5.0'
#root = 'D:\Scratch\PyKBETrans\Input_Ouro_Change_1'

runFinalReplacements = False
fileIterations = 0

totalReplacements = 0
totalLines = 0

fileIterator = 0
lineIterator = 0

ignorePatterns = True

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
		shouldContinue = (name.lower().endswith(patterns) and not ignorePatterns) or ignorePatterns
		if shouldContinue:
			currentLineNumber = 0
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
					if 'namespace KBEngine' in replacementLine:
						replacementLine = replacementLine.replace('namespace KBEngine', 'namespace Ouroboros')
						replacementIterator += 1
					if 'KBEngine' in replacementLine:
						replacementLine = replacementLine.replace('KBEngine', 'Ouroboros')
						replacementIterator += 1
					if 'kbengine' in replacementLine:
						replacementLine = replacementLine.replace('kbengine', 'ouroboros')
						replacementIterator += 1
					if 'KBENGINE' in replacementLine:
						replacementLine = replacementLine.replace('KBENGINE', 'OUROBOROS')
						replacementIterator += 1
					if 'KBEvent' in replacementLine:
						replacementLine = replacementLine.replace('KBEvent', 'OBEvent')
						replacementIterator += 1
					if 'kbeversion' in replacementLine:
						replacementLine = replacementLine.replace('kbeversion', 'ouroversion')
						replacementIterator += 1
					if 'kbemalloc' in replacementLine:
						replacementLine = replacementLine.replace('kbemalloc', 'ouromalloc')
						replacementIterator += 1
					if 'KBCMD' in replacementLine:
						replacementLine = replacementLine.replace('KBCMD', 'OBCMD')
						replacementIterator += 1
					if 'kbcmd' in replacementLine:
						replacementLine = replacementLine.replace('kbcmd', 'obcmd')
						replacementIterator += 1
					if 'kbemain' in replacementLine:
						replacementLine = replacementLine.replace('kbemain', 'ouromain')
						replacementIterator += 1
					if 'kbeMain' in replacementLine:
						replacementLine = replacementLine.replace('kbeMain', 'ouroMain')
						replacementIterator += 1
					if 'KBEMAIN' in replacementLine:
						replacementLine = replacementLine.replace('KBEMAIN', 'OUROMAIN')
						replacementIterator += 1
					if 'KBEKey' in replacementLine:
						replacementLine = replacementLine.replace('KBEKey', 'OUROKey')
						replacementIterator += 1
					if 'kbekey' in replacementLine:
						replacementLine = replacementLine.replace('kbekey', 'ourokey')
						replacementIterator += 1
					if 'KBE_' in replacementLine:
						replacementLine = replacementLine.replace('KBE_', 'OURO_')
						replacementIterator += 1
					if 'kbemachine' in replacementLine:
						replacementLine = replacementLine.replace('kbemachine', 'ouromachine')
						replacementIterator += 1
					if 'KBEComps' in replacementLine:
						replacementLine = replacementLine.replace('KBEComps', 'OUROComps')
						replacementIterator += 1
					if 'KBEMachines' in replacementLine:
						replacementLine = replacementLine.replace('KBEMachines', 'OUROMachines')
						replacementIterator += 1
					if 'kbe_' in replacementLine:
						replacementLine = replacementLine.replace('kbe_', 'ouro_')
						replacementIterator += 1
					if '_kbe' in replacementLine:
						replacementLine = replacementLine.replace('_kbe', '_ouro')
						replacementIterator += 1
					if 'KBE' in replacementLine and runFinalReplacements and not blockFinalReplacement:
						replacementLine = replacementLine.replace('KBE', 'OURO')
						replacementIterator += 1
					if 'kbe' in replacementLine and runFinalReplacements and not blockFinalReplacement:
						replacementLine = replacementLine.replace('kbe', 'ouro')
						replacementIterator += 1

					#SAFEGAURDS
					if 'kbegine' in replacementLine:
						replacementLine = replacementLine.replace('kbegine', 'ouroboros')
						replacementIterator += 1
					if 'blacourorry' in replacementLine:
						replacementLine = replacementLine.replace('blacourorry', 'blackberry')
						replacementIterator += 1
					if 'Blacourorry' in replacementLine:
						replacementLine = replacementLine.replace('Blacourorry', 'Blackberry')
						replacementIterator += 1
					if 'looourohind' in replacementLine:
						replacementLine = replacementLine.replace('looourohind', 'lookbehind')
						replacementIterator += 1

					#COPYRIGHT
					if '// Copyright 2008-2018 Yolo Technologies, Inc. All Rights Reserved. https://www.comblockengine.com' in replacementLine:
						replacementLine = replacementLine.replace('// Copyright 2008-2018 Yolo Technologies, Inc. All Rights Reserved. https://www.comblockengine.com', '// 2017-2019 Rotten Visions, LLC. https://www.rottenvisions.com')
						replacementIterator += 1

					file.write(replacementLine)
					lineIterator += 1

					totalReplacements += replacementIterator
					totalLines += lineIterator

				print('Processed lines: ' + str(lineIterator))
				print('Replaced: ' + str(replacementIterator))

print('Total Processed lines: ' + str(totalLines))
print('Total Replaced: ' + str(totalReplacements))
