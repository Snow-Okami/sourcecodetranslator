# Python Source Code Translator (PYSCT)
========

## Homepage

http://rottenvisions.com

## What is PYSCT?

A simple set of python scripts that re-encode files to the proper encoding first, and then to another language using google cloud translation

## Setup

Open a command line prompt. You can use [Pycharm](https://www.jetbrains.com/pycharm/) to have an all in one set up. I use Pycharm but also [Cmder](http://cmder.net/) on Windows. Omit the '-m' if your python path does not require it.

**Install Chardet for Encoding Detection**

`python -m pip install chardet`

**Install Google Translate**

`python -m pip install google-cloud-translate`

After doing this, go to Google and make a cloud translation account if you don't already have one. This is easier if you already have a Google account.

[Cloud Translation](https://cloud.google.com/translate/)
[Cloud Translate API Key](https://console.cloud.google.com/apis/credentials)

**Set Google Translate Key and Environment Values**

`set GOOGLE_APPLICATION_CREDENTIALS=C:\PATH\TO\JSON-KEY\JsonKey-12345678.json`

See Google [quickstart](https://cloud.google.com/translate/docs/quickstart) for detailed instructions.

**Running the Scripts**

To encode the files or directory, simply move the files to the ToEncode Folder. Once encoded, move the files to the ToTranslate folder. Alternatively you can simply make the newRoot variable in the pyencode script the ToTranslate path.

Be sure to change the paths in both files to the actual location on your system that the PYSCT sits. You can see a simple example already there. These variables are the root and newRoot at the top of each script.

To translate, do the same as above, but with the ToTranslate and Translated folder. After translation has been completed it will dump all the 'Failed Translations' to the console. These will be files that will need manual clean up. Usually just the line number (it will tell you) fails, rather than the entire file.

There are many variables that you can change to alter the behavior of the scripts. Some of the following:

- patterns: These are the file types to look for, usually ending in '.xxx'. For example for C# files you would put in '.cs'
- fileIterations: How many iterations to do on the files contained. For example a value of 1 will only process 1 file. A value of 0 means it will process all.
- lineIterations: How many iterations to do on the lines of a contained file. For example a value of 1 will only process 1 line. A value of 0 means it will process all.

- skipSpecialEncodedFiles: if the encoding is special (not utf8 or gbk / gb2313) then skip it
- deleteOutputFolderOnRun: clears the output folder each time the script is run
- detectSourceLanguage: uses chardet to detect the encoding of a file
- supersetEncoding: using gbk encoding on gbxxxx encodings which is the super set encoding type that contains all characters
- setEncodingModeReplace: sets encoding mode to replace when reading a file for the first time
- replaceFirstCapitalizations: if a translated line started with a lowercase and then the translation turned it capital, it will revert it back to lower case

**FREE TRANSLATION WITH NO GOOGLE ACCOUNT NEEDED** - These scripts can be used without the requirement of google cloud translate. The only issue with this is there is a limit to how many characters Google will let your IP address request. This limit is not known by me currently but others have suggested it is 15,000 characters. I believe the limit has been changed (as others have stated as well) to 5000 characters. The error looks strange and isn't verbose in the least. It will tell you Google Error 401. You can overcome this limitation by getting a program like [Windscribe](https://windscribe.com/) or [TunnelBear](https://www.tunnelbear.com/) to use a [VPN](https://en.wikipedia.org/wiki/Virtual_private_network) or [Proxy](https://en.wikipedia.org/wiki/Proxy_server). This will allow you to switch to a different IP with the limit cleared until it fills again. This can become quite tedious and very time consuming in finding the last file translated and removing it from the input folder. I *highly* recommend signing up for a Google Cloud account instead. I believe they only char per *million* translation requests which is far under what is needed for most code bases.

**Install Python Google Translate**

`python -m pip install googletrans`

**Manual Translation**

This can be achieved very quickly by downloading and installing the [Atom](https://ide.atom.io/) IDE. With Atom, install a plugin called [Atom Translator](https://atom.io/packages/atom-translator). With this plugin you must input an API key which you get from signing up with a Google translation API account. With this simply double click the code to be translated and use the hot-key it comes with (or edit the plugin files to change this) [ctrl-alt-t] and wait a second or two. It should replace the text with the translation, allowing for very quick and painless translations.

**Finding Remaining Chinese Characters**

Using Atom with the Regex option checked in the Find in project box, use the following to find different types of characters:

**Regex Chinese Characters:**

`[\u4e00-\u9fff]+`

**Regex Non ASCII characters:**

`[^\x00-\x7F]`

**KBE NOTES** - These scripts aren't fool proof. In the case of KBEngine, the guiconsole folder from the original source code, must replace the one translated by PYSCT. This isn't a big issue because as of now, this contains no needed translations. The reason this must be done is because the formatting of these files using the very particular [MFC](https://msdn.microsoft.com/en-us/library/d06h2x6e.aspx) (Microsoft Foundation Classes) gets garbled. It usually produces spaces instead of indents as well as other encoding / spacing issues that breaks the project.

After translating, on Windows simply go to the translation folder and copy it over the KBE source folder. Windows will prompt you to replace or skip the files that will overwrite the original KBE files; click replace. Once replacement has taken place, use an IDE to check for errors (I recommend [Visual Studio](https://visualstudio.microsoft.com/) for this project) letting Intellisense do the hard work for you. Also do note when compiling KBE, you need many of the C++ modules, as well as the CLR and MFC & ATL packages for x86 and x64. These can be installed via the Visual Studio Installer (by going to Install / Uninstall Programs -> Microsoft Visual Studio -> Modify)

**New Files**

pykbetransreplace - This file used like the others will do the replacements INPLACE. It requires the InPlace python addon [InPlace](https://pypi.org/project/in-place/) This should be the new preferred script as it is more foolproof than the copy method. It will ONLY replace lines with Chinese (mainly comments) and preserve everything else. This still requires for guiconsole to be replaced. They may be solved by putting some methods in place to skip some files that are sensitive to change. The main files here are the rc and window files.

pykbefixes - This issues fixes that are caused by any of the translation scripts.

pykbenamechange - This script will rename all names contained in scripts to a new name

pykbefilerenamer - This script will attempt to rename files to the new file names it contains. It currently does NOT work. Use [Bulk-Rename](https://www.bulkrenameutility.co.uk/Main_Intro.php) for now to do any renaming. The script can be made to work if a method is incorporated to properly rename folders WHILE there are files still contained in them.

Below is a list of problem areas that may need to be looked at if the project fails to compile.

**Update 5/22/2019 Fixes**

src/lib/network/bundle.h
~525, 531 -> extra */))
lib/common/platform.h
~634 -> ?//
src/lib/client_lib/clientobjectbase.h
~504 -> ?//
src/lib/network/http_utility.h
~41 -> ??//
src/lib/db_mysql/entity_table_mysql.cpp
~43 -> */ :
src/lib/client_lib/clientobjectbase.h
~1240 -> ?//
src/server/baseapp/entity_remotemethod.cpp
~45 -> */ )
src/lib/client_lib/entity.h
~208 -> //   bool isControlled_

**Replacement Paths (Problematic Areas)**

kbe\src\lib\network\common.h
kbe\src\lib\pyscript\pickler.h
kbe\src\lib\pyscript\scriptobject.h
kbe\src\lib\math\math.h
kbe\src\lib\network\bundle.h
kbe\src\lib\network\message_handler.h
kbe\src\lib\entitydef\method.h
kbe\src\lib\entitydef\common.h
kbe\src\lib\entitydef\property.h
kbe\src\lib\server\components.h
kbe\src\lib\entitydef\entity_macro.h
kbe\src\lib\server\serverconfig.h
kbe\src\lib\pyscript\py_gc.h
kbe\src\lib\db_mysql\entity_table_mysql.cpp (Line 1588)
kbe\src\lib\navigation\navigation_tile_handle.cpp
kbe\src\lib\db_mysql\entity_table_mysql.cpp
kbe\src\lib\pyscript\vector3.cpp
kbe\src\lib\pyscript\vector4.cpp
kbe\src\lib\server\telnet_handler.cpp

kbe\src\server\cellapp\witness.cpp
kbe\src\server\cellapp\moveto_point_handler.cpp
kbe\src\server\cellapp\clients_remote_entity_method.h


**Special Manual Edits**

kbe\src\server\dbmgr\dbtasks.cpp: (g_kbeSrvConfig.interfacesAddrs().size() > 0 && !needCheckPassword_)) /*Automatically  create an account when a third party processes successfully*/
kbe\src\server\cellapp\entity.cpp[3229]: if (pobj->isDestroyed() && !pobj->hasFlags(ENTITY_FLAGS_DESTROYING) /* Allows to be  called during destruction*/)

PYSCT was developed to translate source code from other languages. Feel free to fork or request pulls to update / improve the scripts. I am not experienced in python so the script is far from perfect. It went through many iterations based on the KBE code base and uses some functions to get around some issues (such as capitalization from the Google translations) that presented themselves.
