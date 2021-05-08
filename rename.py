#dependencies: pip install pysaucenao, and python 3.6+, and pip install google_trans_new
#theres a 30second wait for every 5 searches, and max 200 searches per day
#a simple option is to store all the done pics into a different folder, so every day you can just run the program in the same folder until the folder is empty

import os, time, asyncio, shutil, google_trans_new, re

from google_trans_new import google_translator  
translator = google_translator()

from pysaucenao import SauceNao
sauce = SauceNao(
    api_key="6abae4a7dfbbc5702649866d477a4307d847c400",
)

def fileRename(f, d, e): #f: filename including extension, d: new filename, e: extension
    try:
        os.rename(f, d+e)
    except FileExistsError:
        fileRenameAppend (f, d, e, 1)

def fileRenameAppend(f, d, e, n): #appends a number to the end of the filename if filename already exists
    try:
        os.rename(f, d+"("+str(n)+")"+e)
    except FileExistsError:
        fileRenameAppend (f, d, e, n+1)

async def searchImage(): #runs through every file in current directory, wherever this py file is. Doesnt go up or down into other folders
    newDirectory = os.path.join(os.getcwd(), "renamedpics") #we're going to move files into this folder for organization purposes
    try:
        os.mkdir(newDirectory)
    except FileExistsError:
        pass
    for filename in os.listdir(os.getcwd()):
        filePath = os.path.join(os.getcwd(), filename)
        if (os.path.isdir(filePath) == False):
            with open(filePath, 'rb') as f:
                name, ext = os.path.splitext(filename)
#note: what extensions am i missing here? test to see if gifs work
                if (ext == ".jpg") or (ext == ".png") or (ext == ".jpeg") or (ext == ".webp"):
                    results = await sauce.from_file(f)
                    if (results.short_remaining == 0): #api limiter every 30sec
                        print ("sleeping for 30sec")
                        time.sleep(30)
                    if (results.long_remaining == 0):
                        print ("done with the 200 daily limit, please run me again tmrw")
                        break
                    if (results):
#also possible: check for non alphanumeric, THEN translate those characters only. That way romaji stays the same. 
                        translationResult = translator.translate(results[0].title)
                        translationResult = re.sub("[<|:|>|/|\\\|*|?|\"| |\|]", "", translationResult)
                        print (translationResult)

                        fileRename(filename, translationResult, ext)
                        filePath = os.path.join (os.getcwd(), translationResult+ext)
                        futureFilePath = os.path.join (newDirectory, translationResult+ext)
                        
                        i=0
                        while (os.path.isfile(futureFilePath)): #while futureFilePath exists, we increase and append i to the filename until it passes
                            i += 1
                            futureFilePath = os.path.join (newDirectory, translationResult+"("+str(i)+")"+ext)
                        if i>0:
                            filePath = os.path.join (os.getcwd(), translationResult+"("+str(i)+")"+ext)
                            os.rename(translationResult+ext, translationResult+"("+str(i)+")"+ext)
                        os.path.normpath(filePath)
                        shutil.move(filePath, newDirectory)
                    else:
                        print ("no results for " + filename)
                        shutil.move(filePath, newDirectory)
                else:
                    print (filename + " is not an image")

loop = asyncio.get_event_loop()
loop.run_until_complete(searchImage())
loop.close()