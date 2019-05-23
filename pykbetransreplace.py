import re
from chardet.universaldetector import UniversalDetector
import win_unicode_console
import in_place

# Imports the Google Cloud client library
from google.cloud import translate
# File Parsing
import fileinput

import os
import sys
import stat
import errno
import shutil
import time
import subprocess
import csv

import inplace

#root = 'D:\Scratch\PyKBETrans\Input_2.5.0'
root = 'D:\Scratch\PyKBETrans\Input_8'

commentSlashes = "//"
commentNumbers = "#"
commentBegin = "/*"
commentEnd = "*/"

LF = b'\n'
CR = b'\r'
CRLF = b'\r\n'

detector = UniversalDetector()
# Instantiates a client
translate_client = translate.Client()

srcLang = 'auto'  # zh-CN
destLang = 'en'  # en

asciiEncoding = 'ascii'
chineseEncoding = 'GB2312'
chineseEncodingTwo = 'gb2312'
chineseSuperSetEncoding = 'gbk'
alternateChineseEncoding = 'HZ-GB-2312'
cpEncoding = 'cp1252'
extendedUnixEncoding = 'EUC-TW'
latinEncoding = 'ISO-8859-1'
windowsEncoding = 'Windows-1254'
utfEncoding = 'utf-8'

encodingMode = 'strict'
encodingModeReplace = 'replace'

fileIterations = 0
lineIterations = 0

#lineRange = [105, 107]
lineRange = []

continueWritingAfterMaxIterations = True
skipSpecialEncodedFiles = False
deleteOutputFolderOnRun = False
detectSourceLanguage = True
supersetEncoding = True
setEncodingModeReplace = True
replaceFirstCapitalizations = False

fileIterator = 0
lineIterator = 0

patterns = ('.cpp', '.h', '.cs', '.py', '.xml', '.def', '.md')

failedTranslations = ''
failedToTranslate = False

failedWrites = ''
failedToWrite = False

lineEnding = LF

currentDir = os.getcwd()
win_unicode_console.enable()
osSep = os.linesep
normSep = '\n'

target = srcLang
if setEncodingModeReplace:
	encodingMode = encodingModeReplace

defaultEncoding = utfEncoding

# list of cjk codepoint ranges
# tuples indicate the bottom and top of the range, inclusive
cjk_ranges = [
	(0x4E00, 0x62FF),
	(0x6300, 0x77FF),
	(0x7800, 0x8CFF),
	(0x8D00, 0x9FCC),
	(0x3400, 0x4DB5),
	(0x20000, 0x215FF),
	(0x21600, 0x230FF),
	(0x23100, 0x245FF),
	(0x24600, 0x260FF),
	(0x26100, 0x275FF),
	(0x27600, 0x290FF),
	(0x29100, 0x2A6DF),
	(0x2A700, 0x2B734),
	(0x2B740, 0x2B81D),
	(0x2B820, 0x2CEAF),
	(0x2CEB0, 0x2EBEF),
	(0x2F800, 0x2FA1F)
]

ranges = [
	{"from": ord(u"\u3300"), "to": ord(u"\u33ff")},  # compatibility ideographs
	{"from": ord(u"\ufe30"), "to": ord(u"\ufe4f")},  # compatibility ideographs
	{"from": ord(u"\uf900"), "to": ord(u"\ufaff")},  # compatibility ideographs
	{"from": ord(u"\U0002F800"), "to": ord(u"\U0002fa1f")},  # compatibility ideographs
	{"from": ord(u"\u30a0"), "to": ord(u"\u30ff")},  # Japanese Kana
	{"from": ord(u"\u2e80"), "to": ord(u"\u2eff")},  # cjk radicals supplement
	{"from": ord(u"\u4e00"), "to": ord(u"\u9fff")},
	{"from": ord(u"\u3400"), "to": ord(u"\u4dbf")},
	{"from": ord(u"\U00020000"), "to": ord(u"\U0002a6df")},
	{"from": ord(u"\U0002a700"), "to": ord(u"\U0002b73f")},
	{"from": ord(u"\U0002b740"), "to": ord(u"\U0002b81f")},
	{"from": ord(u"\U0002b820"), "to": ord(u"\U0002ceaf")}  # included as of Unicode 8.0
]


def iscjkChar(char):
	return any([range["from"] <= ord(char) <= range["to"] for range in ranges])


def is_cjk(character):
	""""
    Checks whether character is CJK.

        >>> is_cjk(u'\u33fe')
        True
        >>> is_cjk(u'\uFE5F')
        False

    :param character: The character that needs to be checked.
    :type character: char
    :return: bool
    """
	return any([start <= ord(character) <= end for start, end in
				[(4352, 4607), (11904, 42191), (43072, 43135), (44032, 55215),
				 (63744, 64255), (65072, 65103), (65381, 65500),
				 (131072, 196607)]
				])


def lcfc(strToTest):
	# strToTest = strToTest.encode(defaultEncoding)
	for c in strToTest:
		if u'\u4e00' <= c <= u'\u9fff':
			return True
	return False


def abcdef(strToTest):
	for n in re.findall(r'[\u4e00-\u9fff]+', strToTest):
		print('n: ' + n)


def lineContainsForeignCharacters(strToTest):
	if strToTest.find('[\u4e00-\u9fff]+'):
		return True
	return False


def isCjk(char):
	char = ord(char)
	for bottom, top in cjk_ranges:
		if char >= bottom and char <= top:
			print('YUPPPP')
			return True
	return False


def cjk_substrings(string):
	i = 0
	while i < len(string):
		if iscjkChar(string[i]):
			start = i
			while iscjkChar(string[i]):
				i += 1
				yield string[start:i]
		i += 1


def containsChineseCharacter(strToTest):
	for c in strToTest:
		if iscjkChar(c):
			print('got em')
			return True
		print(c)
	return False


def translate(m):
	block = m.group().encode(utfEncoding)
	print('block = ' + block)
	return 'empty barren'


def getTabString(count):
	str = ''
	for _ in range(count):
		str += '\t'
	return str


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

def replaceUnixCodes(strToCheck):
	strToCheck = strToCheck.replace("&#39;", "'")
	strToCheck = strToCheck.replace("&gt;", ">")
	strToCheck = strToCheck.replace("&lt;", "<")
	strToCheck = strToCheck.replace("&quot;", "'")
	strToCheck = strToCheck.replace("&amp;", "&")
	return strToCheck


def replacementsCustom(strToCheck):
	strToCheck = strToCheck.replace("#Include;", "#include")
	strToCheck = strToCheck.replace("#Define", "#define")
	strToCheck = strToCheck.replace("#If", "#if")
	strToCheck = strToCheck.replace("#Ifndef", "#ifndef")
	strToCheck = strToCheck.replace("#Endif	", "#endif")
	strToCheck = strToCheck.replace("#Elif", "#elif")
	strToCheck = strToCheck.replace("#Else", "#else")
	return strToCheck


def replaceBrokenComments(strToCheck):
	strToCheck = strToCheck.replace("/ /", "//")
	return strToCheck


def replaceFirstWordCpp(strToCheck):
	if strToCheck.strip().startswith('TypeDef'):
		strToCheck = strToCheck.replace('TypeDef', 'typedef')
	elif strToCheck.strip().startswith('typeDef'):
		strToCheck = strToCheck.replace('typeDef', 'typedef')
	elif strToCheck.strip().startswith('Typedef'):
		strToCheck = strToCheck.replace('Typedef', 'typedef')
	elif strToCheck.strip().startswith('Static'):
		strToCheck = strToCheck.replace('Static', 'static')
	elif strToCheck.strip().startswith('Struct'):
		strToCheck = strToCheck.replace('Struct', 'struct')
	elif strToCheck.strip().startswith('Bool'):
		strToCheck = strToCheck.replace('Bool', 'bool')
	elif strToCheck.strip().startswith('Char'):
		strToCheck = strToCheck.replace('Char', 'char')
	elif strToCheck.strip().startswith('Int'):
		strToCheck = strToCheck.replace('Int', 'int')
	elif strToCheck.strip().startswith('Int8'):
		strToCheck = strToCheck.replace('Int8', 'int8')
	elif strToCheck.strip().startswith('Int16'):
		strToCheck = strToCheck.replace('Int16', 'int16')
	elif strToCheck.strip().startswith('Int32'):
		strToCheck = strToCheck.replace('Int32', 'int32')
	elif strToCheck.strip().startswith('Int64'):
		strToCheck = strToCheck.replace('Int64', 'int64')
	elif strToCheck.strip().startswith('Uint'):
		strToCheck = strToCheck.replace('Uint', 'uint')
	elif strToCheck.strip().startswith('Uint8'):
		strToCheck = strToCheck.replace('Uint8', 'uint8')
	elif strToCheck.strip().startswith('Uint8_t'):
		strToCheck = strToCheck.replace('Uint8_t', 'uint8_t')
	elif strToCheck.strip().startswith('Uint16'):
		strToCheck = strToCheck.replace('Uint16', 'uint16')
	elif strToCheck.strip().startswith('Uint32'):
		strToCheck = strToCheck.replace('Uint32', 'uint32')
	elif strToCheck.strip().startswith('Uint64'):
		strToCheck = strToCheck.replace('Uint64', 'uint64')
	elif strToCheck.strip().startswith('Std::'):
		strToCheck = strToCheck.replace('Std::', 'std::')
	elif strToCheck.strip().startswith('Float'):
		strToCheck = strToCheck.replace('Float', 'float')
	elif strToCheck.strip().startswith('Const'):
		strToCheck = strToCheck.replace('Const', 'const')
	elif strToCheck.strip().startswith('If'):
		strToCheck = strToCheck.replace('If', 'if')
	elif strToCheck.strip().startswith('Else'):
		strToCheck = strToCheck.replace('Else', 'else')
	elif strToCheck.strip().startswith('While'):
		strToCheck = strToCheck.replace('While', 'while')
	elif strToCheck.strip().startswith('Case'):
		strToCheck = strToCheck.replace('Case', 'case')
	elif strToCheck.strip().startswith('Extern'):
		strToCheck = strToCheck.replace('Extern', 'extern')
	elif strToCheck.strip().startswith('Default'):
		strToCheck = strToCheck.replace('Default', 'default')
	elif strToCheck.strip().startswith('Currpos'):
		strToCheck = strToCheck.replace('Currpos', 'currpos')
	elif strToCheck.strip().startswith('Return'):
		strToCheck = strToCheck.replace('Return', 'return')
	elif strToCheck.strip().startswith('Continue'):
		strToCheck = strToCheck.replace('Continue', 'continue')
	elif strToCheck.strip().startswith('Break'):
		strToCheck = strToCheck.replace('Break', 'break')
	elif strToCheck.strip().startswith('Extra'):
		strToCheck = strToCheck.replace('Extra', 'extra')
	return strToCheck


def replaceFirstWordPy(strToCheck):
	return strToCheck


def replaceFirstWordOuro(strToCheck):
	return strToCheck


def replaceFirstWordCSharp(strToCheck):
	return strToCheck


def removeSign(signToCheck, strToCheck):
	if strToCheck.startswith(signToCheck):
		strToCheck = strToCheck.replace(signToCheck, "")
	return strToCheck


def startsWith(signToCheck, strToCheck):
	if strToCheck.startswith(signToCheck):
		return True
	return False


def startsWithAtSign(strToCheck):
	if strToCheck.startswith('@'):
		return True
	return False


def startsWithASlash(strToCheck):
	if strToCheck.startswith('/'):
		return True
	return False


def wasLowerBefore(beforeStr, afterStr):
	firstNonWhitespaceCharacterIndexBefore = len(beforeStr) - len(beforeStr.lstrip())
	firstNonWhitespaceCharacterIndexAfter = len(afterStr) - len(afterStr.lstrip())
	if afterStr[firstNonWhitespaceCharacterIndexAfter].isupper() and beforeStr[
		firstNonWhitespaceCharacterIndexBefore].islower():
		return True
	return False


def upperFirstLetter(strToCheck):
	firstNonWhitespaceCharacterIndex = len(strToCheck) - len(strToCheck.lstrip())
	return capitalize(strToCheck, firstNonWhitespaceCharacterIndex)


def lowerFirstLetter(strToCheck):
	firstNonWhitespaceCharacterIndex = len(strToCheck) - len(strToCheck.lstrip())
	newStr = strToCheck[:firstNonWhitespaceCharacterIndex] + strToCheck[
		firstNonWhitespaceCharacterIndex].lower() + strToCheck[firstNonWhitespaceCharacterIndex + 1:]
	return newStr


# return lowerize(strToCheck, firstNonWhitespaceCharacterIndex)

def capitalize(s, ind):
	split_s = list(s)
	for i in range(ind):
		try:
			split_s[i] = split_s[i].upper()
		except IndexError:
			print(f"Sorry, index is not in range! ({i})")
	return "".join(split_s)


def lowerize(s, ind):
	split_s = list(s)
	print(str(ind) + " index")
	for i in range(ind):
		try:
			split_s[i] = split_s[i].lower()
		except IndexError:
			print(f"Sorry, index is not in range! ({i})")
	return "".join(split_s)


def everythingAfter(strToTest, afterStr):
	strElements = strToTest.split(afterStr)
	if len(strElements) > 1:
		return strElements[1]
	return strToTest


def everythingBefore(strToTest, afterStr):
	return strToTest.split(afterStr)[0]


def splitString(strToTest, afterStr, index):
	return strToTest.split(afterStr)[index]


def getChinese(context):
	# context = context.decode("utf-8") # convert context from str to unicode
	filtrate = re.compile(u'[\u4e00-\u9fff]+')  # non-Chinese unicode range
	context = filtrate.sub(r'', context)  # remove all non-Chinese characters
	# context = context.encode("utf-8") # convert unicode back to str
	return str(context)


def containsComments(strToTest):
	if '//' in strToTest or '#' in strToTest or '/*' in strToTest or '*/' in strToTest or "'''" in strToTest:
		return True
	return False


def findFirstIndexOf(strToTest, strToFind):
	index = strToTest.find(strToFind)
	if index >= 0:
		return index
	return -1

def containsChineseCharacter(strToTest):
	if re.search(u'[\u4e00-\u9fff]', strToTest):
		return True
	return False

def containsChineseChar(strToTest):
	for i in strToTest:
		if ord(i) >= 0x4e00 and ord(i) <= 0x9fff:
			return True
	return False

def getAllChineseInString(strToTest):
	for n in re.findall(r'[\u4e00-\u9fff]+', strToTest):
		return n

def restoreOldLeadingFormatting(oldStr):
	return oldStr[:-len(oldStr.lstrip())]


def fileNameEndsWith(strToTest, fileExtension):
	return strToTest.endswith(fileExtension)

def sniff(filename):
	newline = LF
	with open(filename, 'rb') as f:
		content = f.read()
		if CRLF in content:
			newline = 'CRLF'
		elif LF in content:
			newline = 'LF'
		elif CR in content:
			newline = 'CR'
	return newline

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
			detector.reset()
			file = open(currentFile, 'rb')
			for line in file:
				detector.feed(line)
				if detector.done:
					break
			detector.close()
			newEncoding = detector.result['encoding']
			if skipSpecialEncodedFiles:
				if newEncoding != chineseEncoding or newEncoding != utfEncoding:
					continue
			if newEncoding is not None:
				# We get a LookupError: unknown encoding: EUC-TW if this type of encoding is detected
				if newEncoding == extendedUnixEncoding:
					newEncoding = chineseEncoding
				if supersetEncoding and newEncoding == chineseEncoding:
					newEncoding = chineseSuperSetEncoding
				#if newEncoding == asciiEncoding or newEncoding == utfEncoding:
					#newEncoding = chineseSuperSetEncoding
				if newEncoding == windowsEncoding or newEncoding == alternateChineseEncoding or newEncoding == extendedUnixEncoding:
					newEncoding = utfEncoding
			else:
				newEncoding = defaultEncoding

			lineEnding = sniff(currentFile)
			normSep = lineEnding

			print('Scanning File: ', file.name, 'with encoding:', newEncoding)

			with in_place.InPlace(currentFile, encoding=newEncoding, errors=encodingMode) as file:
				for line in file:
					currentLineNumber += 1
					if lineRange:
						if currentLineNumber < lineRange[0]:
							file.write(line)
							continue
						if currentLineNumber > lineRange[1]:
							file.write(line)
							continue
					if lineIterations != 0 and lineIterator >= lineIterations:
						if continueWritingAfterMaxIterations:
							file.write(line)
							continue
						else:
							break
					translated = False
					translatedString = ''
					untranslatedString = line
					finalWrittenLine = line
					preTranslatedString = ''
					beforeTranslationSubString = ''
					beforeTranslationFullSubString = ''
					afterTranslationSubString = ''
					afterTranslationSubStringComplete = ''
					finalBefore = ''
					finalAfter = ''
					indentedSpace = ''
					failedToTranslate = False
					inLineCommentConvert = False

					if containsChineseCharacter(line):
						if currentLineNumber == lastLineNumberTranslated:
							continue
						sourceLanguage = srcLang
						if detectSourceLanguage:
							detectedLang = translate_client.detect_language([line])
							sourceLanguage = detectedLang[0]['language']
						preTranslatedString = line
						rawTranslite = line
						mustBeTranslated = line

						removalIndex = findFirstIndexOf(line, preTranslatedString)
						toTranslate = line

						if containsComments(line):
							containsCommentMarker = True
						if '//' in mustBeTranslated:
							rawTranslite = everythingAfter(mustBeTranslated, '//')
							print(rawTranslite)
							removalIndex = findFirstIndexOf(mustBeTranslated, '//')
							print(str(removalIndex) + " index")
							beforeTranslationSubString = line.split('//', 1)[0]
							print('Sub ' + beforeTranslationSubString)
						if '/*' in mustBeTranslated:
							rawTranslite = everythingAfter(mustBeTranslated, '/*')
							removalIndex = findFirstIndexOf(line, '/*')
							beforeTranslationSubString = line.split('/*', 1)[0]
							if '*/' in mustBeTranslated:
								toTranslate = everythingBefore(rawTranslite, '*/')
								finalBefore = everythingBefore(mustBeTranslated, '/*') + '/*'
								finalAfter = '*/' + everythingAfter(mustBeTranslated, '*/')
								inLineCommentConvert = True
						if '#' in mustBeTranslated:
							rawTranslite = everythingAfter(mustBeTranslated, '#')
							removalIndex = findFirstIndexOf(line, '#')
							beforeTranslationSubString = line.split('#', 1)[0]
						if "'''" in mustBeTranslated:
							rawTranslite = everythingAfter(mustBeTranslated, "'''")
							removalIndex = findFirstIndexOf(line, "'''")
							beforeTranslationSubString = line.split("'''", 1)[0]
						beforeTranslationFullSubString = line[:removalIndex]

						try:
							if sourceLanguage is not destLang:
								result = translate_client.translate(toTranslate, source_language=sourceLanguage,
																	format_='text', target_language=destLang)
								translatedString = result['translatedText']
						except:
							translatedString = line

						translated = True
						# Capitalizations take place from translation, so this should stop this - this makes comments lowercase however though
						if replaceFirstCapitalizations and wasLowerBefore(mustBeTranslated, translatedString):
							translatedString = lowerFirstLetter(translatedString)
						# Only replace these first words if it is in an effected file type
						if fileNameEndsWith(currentFile, '.cpp') or fileNameEndsWith(currentFile, '.h'):
							translatedString = replaceFirstWordCpp(translatedString)
						if fileNameEndsWith(currentFile, '.def') or fileNameEndsWith(currentFile, '.xml'):
							translatedString = replaceFirstWordOuro(translatedString)
						if fileNameEndsWith(currentFile, '.py'):
							translatedString = replaceFirstWordPy(translatedString)
						if fileNameEndsWith(currentFile, '.cs'):
							translatedString = replaceFirstWordCSharp(translatedString)
						translatedString = replaceUnixCodes(translatedString)
						translatedString = replaceBrokenComments(translatedString)
						translatedString = replacementsCustom(translatedString)
						# Remove newline and see if line ends with a backslash
						containsNewLine = False
						'''if '\n \n' in line or '\n\n' in line:
							containsNewLine = True'''
						if re.search("(\\r|)\\n$", translatedString):
							removedNewline = re.sub("(\\r|)\\n$", "", translatedString)
							if removedNewline[-1:] is "\\":
								translatedString = re.sub("(\\r|)\\n$", "", translatedString)
						translatedStringFull = translatedString
						if inLineCommentConvert:
							translatedStringFull = finalBefore + translatedString + finalAfter
						if '????//'in translatedStringFull:
							translatedString = translatedString.replace('????//', '//')
							print('replaced')
						if '?????//' in translatedStringFull:
							translatedString = translatedString.replace('?????//', '//')
						finalWrittenLine = restoreOldLeadingFormatting(line) + translatedStringFull + (normSep if containsNewLine else '')
						# print('Translated[' + sourceLanguage + ']: ' + untranslatedString + ' To: ' + translatedString)
						print('(' + str(lineIterator) + ')[' + sourceLanguage + ']: To: ' + finalWrittenLine)
						time.sleep(0.15)
					try:
						file.write(finalWrittenLine)
					except Exception as e:
						file.write(line)
						print('Failed to Write: ', currentLineNumber)
						print(e)
						failedWrites += '%i | %s \n' % (currentLineNumber, currentFile)
						failedToWrite = True
						continue
					lineIterator += 1
				print('Processed lines: ' + str(lineIterator))
				if failedToTranslate:
					print('-----FAILED TRANSLATIONS-----')
					print(failedTranslations)
				if failedToWrite:
					print('-----FAILED WRITES-----')
					print(failedWrites)