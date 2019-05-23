from chardet.universaldetector import UniversalDetector
import win_unicode_console

import os
import shutil
import errno
import re
import sys
import codecs

root = 'D:\Scratch\PyKBETrans\ToEncode'
newRoot = 'D:\Scratch\PyKBETrans\Encoded'

toEncoding = 'utf-8'
chineseEncoding = 'GB2312'
superSetEncoding = 'gbk'

deleteOutputFolderOnRun = True

fileIterator = 0
lineIterator = 0

fileIterations = 0

failedFiles = ''

patterns = ('.cpp', '.h', '.cs', '.py', '.xml', '.def', '.md')

detector = UniversalDetector()

currentDir = os.getcwd()
win_unicode_console.enable()

def getEncodingType(currentFile):
	detector.reset()
	tempFile = open(currentFile, 'rb')
	for line in tempFile:
		detector.feed(line)
		if detector.done:
			break
	detector.close()
	return detector.result['encoding']

def correctSubtitleEncoding(filename, newFilename, encoding_from, encoding_to='UTF-8'):
	with open(filename, 'r', encoding=encoding_from) as fr:
		with open(newFilename, 'w', encoding=encoding_to) as fw:
			for line in fr:
				fw.write(line[:-1] + '\n')

def createIfNotExists(filepath):
	if not os.path.exists(os.path.dirname(filepath)):
		try:
			os.makedirs(os.path.dirname(filepath))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

if deleteOutputFolderOnRun:
	if not os.path.exists(os.path.dirname(newRoot)):
		shutil.rmtree(newRoot)
		os.makedirs(newRoot)

for path, subdirs, files in os.walk(root):
	for name in files:
		if fileIterations != 0:
			if fileIterator >= fileIterations:
				break
		fileIterator = + 1
		if name.lower().endswith(patterns):
			currentFile = os.path.join(path, name)
			newFilePath = currentFile.replace(root, newRoot)
			createIfNotExists(newFilePath)
			currentDetectedEncoding = getEncodingType(currentFile)
			if currentDetectedEncoding is chineseEncoding:
				currentDetectedEncoding = superSetEncoding
			try:
				correctSubtitleEncoding(currentFile, newFilePath, currentDetectedEncoding, toEncoding)
			except:
				failedFiles += currentFile + '\n'
				continue
			print('Encoding: ' + currentFile + ' [' + str(currentDetectedEncoding) + '] To: ' + newFilePath + ' [' + toEncoding + ']')
